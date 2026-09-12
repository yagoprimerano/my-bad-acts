#!/usr/bin/env bash
# Triagem T4 dos 4 modelos ABERTOS. Rode na maquina do laboratorio, por SSH.
#
# Protocolo T4: 72 execucoes por modelo, IDENTICO ao dos 4 modelos pagos (mesmos casos, mesma
# semente, mesmos blocos). Tres ambientes: code_generation saiu porque nenhum candidato completa a
# tarefa benigna dele (utilidade 0 em todos os modelos medidos), entao o bloco media o proxy e nao
# os modelos. Documentacao completa: docs/02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md
#
#   bash scripts/triagem/run_triagem_local.sh --dry-run     # sempre faca isto primeiro
#   bash scripts/triagem/run_triagem_local.sh
#
# SOBREVIVER AO SSH: a triagem inteira leva horas. Rode dentro de tmux, ou a queda da conexao
# mata a sweep no meio:
#
#   tmux new -s triagem
#   bash scripts/triagem/run_triagem_local.sh
#   # Ctrl-b d  para desanexar; 'tmux attach -t triagem' para voltar
#
# Pode interromper a qualquer momento (Ctrl-C, ou a maquina caindo): basta repetir o comando depois.
# O --resume e' por EXECUCAO, nao por bloco. O manifesto e' gravado DEPOIS de cada episodio, entao
# tudo que ja' terminou esta' salvo, e no pior caso voce repete UM episodio: o que estava no ar na
# hora da parada, que e' refeito do inicio (nao existe retomar um episodio pela metade).
#
# Progresso a qualquer momento, sem interromper:
#   wc -l evaluation_results/screening/abertos/*/manifest_*.jsonl
# Esperado por manifesto: L=30, A=8, B1=10, B2=16, e 4 em cada um dos dois do bloco F.

set -euo pipefail

cd "$(dirname "$0")/../.."
PYTHON="${PYTHON:-python3}"

# ---------------------------------------------------------------------------------------------
# Backend. Ollama e' o padrao porque nao exige nada alem de 'ollama pull'. Para o definitivo
# (milhares de execucoes) troque para vLLM, que faz batelada na mesma GPU.
#
#   PROVIDER=vllm BASE_URL=http://localhost:8000/v1 bash scripts/triagem/run_triagem_local.sh
#
# O modelo de 70B nao cabe numa unica RTX 5000 Ada de 32 GB (~43 GB em 4-bit): ele precisa das
# DUAS placas. No Ollama isso e' automatico; no vLLM sirva com --tensor-parallel-size 2.
# ---------------------------------------------------------------------------------------------
PROVIDER="${PROVIDER:-ollama}"
BASE_URL="${BASE_URL:-}"
API_KEY="${API_KEY:-EMPTY}"

# Janela de contexto do Ollama. NAO deixe no padrao. O Ollama abre a janela maxima do modelo
# (131072 no llama3.3:70b) e o cache KV disso, num modelo de 80 camadas, e' ~41 GB SOBRE os ~43 GB
# de pesos: ele reporta um modelo de 86 GB, nao cabe nas duas placas de 32 GB, e descarrega parte
# para a CPU SEM AVISAR. Medido em 04/09/2026 na maquina do laboratorio: `PROCESSOR 28%/72%
# CPU/GPU`, com um episodio de 15 mensagens levando 21 minutos.
#
# 32768 deixa o cache em ~10 GB (total ~53 GB, cabe) e e' folgado para estes ambientes, cujo
# episodio inteiro somou 18,6 mil tokens de entrada. Se `ollama ps` ainda mostrar CPU, caia para
# 16384. Confira SEMPRE com `ollama ps` durante a primeira execucao.
NUM_CTX="${NUM_CTX:-32768}"

# Teto de relogio por episodio, em segundos. Um episodio que estourar e' morto e contabilizado como
# execucao FALHA do candidato, que e' o tratamento correto: nao terminar e' falha de competencia,
# nao dado faltante. Medido em 11/09/2026 na c4ai: o `qwen3:14b` ficou 1h48 num unico turno, com a
# GPU a 98%, sem produzir uma segunda mensagem. O Ollama nao limita o comprimento da geracao, entao
# um modelo em laco gera para sempre e, sem este teto, trava a sweep inteira em silencio.
# 1200s e' folgado: o pior episodio medido (70B no debate) levou 16m46s.
RUN_TIMEOUT="${RUN_TIMEOUT:-1200}"

DRY_RUN=""
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN="--dry-run"
  shift
fi

# tag | nome no backend | familia (model_info do vLLM) | o que este degrau responde
LADDER=(
  "qwen3-8b|qwen3:8b|qwen|controle de piso: esperamos que NAO passe"
  "qwen3-14b|qwen3:14b|qwen|degrau intermediario"
  "qwen3-32b|qwen3:32b|qwen|aposta a priori: o menor competente, cabe em 1 GPU"
  "llama33-70b|llama3.3:70b|llama|teto: o ganho de escala compensa o tempo de GPU?"
)

LOG_DIR="evaluation_results/screening/logs"
mkdir -p "$LOG_DIR"

echo "############################################################################"
echo "# Ambiente"
echo "############################################################################"
nvidia-smi --query-gpu=index,name,memory.total --format=csv || echo "AVISO: nvidia-smi indisponivel."
echo
$PYTHON -c "import autogen_agentchat, autogen_core, autogen_ext; print('autogen ok')"
# O daemon do Docker NAO e' necessario. Code_Generation.py e Fincancial_Article_Writing.py apenas
# IMPORTAM DockerCommandLineCodeExecutor no topo; o executor nunca e' instanciado (em Fincancial a
# linha esta comentada). Verificado em 11/09/2026 com DOCKER_HOST apontando para um socket
# inexistente: os dois modulos importam normalmente. O que precisa existir e' o PACOTE, nao o
# servico -- por isso a checagem abaixo e' de import, e nao 'docker ps'.
$PYTHON -c "import autogen_ext.code_executors.docker; print('pacote docker do autogen ok')" \
  || { echo "ERRO: falta o extra autogen_ext[docker]; os ambientes de codigo e financeiro nao importam." >&2; exit 1; }

if [[ "$PROVIDER" == "ollama" ]]; then
  ollama list || { echo "ERRO: 'ollama serve' nao esta rodando." >&2; exit 1; }
fi

# Descarrega da VRAM o modelo do degrau anterior. Sem isto, o OLLAMA_KEEP_ALIVE mantem os pesos
# residentes por muito tempo depois do ultimo episodio, e o modelo seguinte pode nao caber: o Ollama
# entao descarrega camadas para a CPU SEM AVISAR e a sweep passa a medir swap, nao o modelo.
unload_previous_models() {
  [[ "$PROVIDER" != "ollama" ]] && return 0
  local loaded
  loaded=$(ollama ps 2>/dev/null | awk 'NR>1 {print $1}')
  for m in $loaded; do
    echo "Descarregando da VRAM: $m"
    ollama stop "$m" >/dev/null 2>&1 || true
  done
  return 0
}

# O episodio so' vale se o modelo estiver inteiro na GPU. Confirma depois do primeiro episodio de
# cada degrau; o custo de errar isto foi medido em 8,7x na maquina do laboratorio.
assert_full_gpu() {
  [[ "$PROVIDER" != "ollama" ]] && return 0
  local line
  line=$(ollama ps 2>/dev/null | awk 'NR>1')
  [[ -z "$line" ]] && return 0
  echo "ollama ps -> $line"
  if ! grep -q "100% GPU" <<< "$line"; then
    echo "AVISO: o modelo NAO esta 100% na GPU. O tempo medido daqui em diante nao vale." >&2
    echo "       Reduza NUM_CTX (ex.: NUM_CTX=16384) e rode de novo; --resume aproveita o que ja' terminou." >&2
  fi
  return 0
}

for entry in "${LADDER[@]}"; do
  IFS='|' read -r TAG MODEL FAMILY NOTE <<< "$entry"
  echo
  echo "############################################################################"
  echo "# TRIAGEM T4 | $MODEL | $NOTE"
  echo "############################################################################"
  [[ -z "$DRY_RUN" ]] && unload_previous_models

  EXTRA=()
  if [[ "$PROVIDER" != "ollama" ]]; then
    [[ -n "$BASE_URL" ]] && EXTRA+=(--model-base-url "$BASE_URL") || true
    EXTRA+=(--model-api-key "$API_KEY" --model-family "$FAMILY")
  else
    EXTRA+=(--model-extra-args "{\"options\": {\"num_ctx\": $NUM_CTX}}")
  fi

  # Em segundo plano, e ANTES do pipeline: a checagem so' diz algo com o modelo ja' carregado, e o
  # pipeline precisa ficar em primeiro plano para que PIPESTATUS[0] seja o do Python, nao o do tee.
  # 180s cobrem o carregamento do 70B a partir de disco girante.
  if [[ -z "$DRY_RUN" ]]; then
    ( sleep 180; assert_full_gpu ) >> "$LOG_DIR/${TAG}.log" 2>&1 &
  fi

  set +e
  $PYTHON -u scripts/run_screening_protocol.py \
    --tag "$TAG" \
    --out-dir "evaluation_results/screening/abertos/$TAG" \
    --results-dir "results/triagem/abertos" \
    --model-client "$MODEL" \
    --model-provider "$PROVIDER" \
    --resume \
    --run-timeout "$RUN_TIMEOUT" \
    ${EXTRA[@]+"${EXTRA[@]}"} \
    $DRY_RUN "$@" 2>&1 | tee "$LOG_DIR/${TAG}.log"
  STATUS=${PIPESTATUS[0]}
  set -e

  if [[ $STATUS -ne 0 ]]; then
    # Um candidato que quebra nao interrompe a escada: quebrar E' o resultado dele. A analise
    # conta as execucoes quebradas contra o candidato, que e' o tratamento correto -- nao
    # conseguir terminar um episodio e' falha de competencia, nao dado faltante.
    echo "AVISO: $MODEL terminou com codigo $STATUS. Seguindo para o proximo candidato." >&2
  fi
done

if [[ -n "$DRY_RUN" ]]; then
  echo
  echo "Ensaio a seco concluido. Nada foi executado."
  exit 0
fi

echo
echo "############################################################################"
echo "# Veredito da escada aberta"
echo "############################################################################"
$PYTHON scripts/analyze_screening_protocol.py \
  --screening-dir evaluation_results/screening \
  --open-ladder qwen3-8b,qwen3-14b,qwen3-32b,llama33-70b \
  --out-json evaluation_results/screening/relatorio_triagem_local.json \
  --out-csv evaluation_results/screening/relatorio_triagem_local.csv

echo
echo "Traga os resultados para o notebook e junte com a triagem paga:"
echo "  rsync -avz USUARIO@MAQUINA:~/BAD-ACTS/results/ ./results/"
echo "  rsync -avz USUARIO@MAQUINA:~/BAD-ACTS/evaluation_results/ ./evaluation_results/"

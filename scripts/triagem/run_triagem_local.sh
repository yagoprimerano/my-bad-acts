#!/usr/bin/env bash
# Triagem T3 dos 4 modelos ABERTOS. Rode na maquina do laboratorio, por SSH.
#
# Protocolo: 82 execucoes por modelo, IDENTICO ao dos 5 modelos pagos (mesmos casos, mesma
# semente, mesmos blocos). Documentacao completa: docs/02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md
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
# Esperado por manifesto: L=40, A=8, B1=10, B2=16, e 4 em cada um dos dois do bloco F.

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
docker ps >/dev/null 2>&1 \
  && echo "docker ok" \
  || echo "AVISO: docker nao responde. code_generation e financial_article_writing vao falhar no import."

if [[ "$PROVIDER" == "ollama" ]]; then
  ollama list || { echo "ERRO: 'ollama serve' nao esta rodando." >&2; exit 1; }
fi

for entry in "${LADDER[@]}"; do
  IFS='|' read -r TAG MODEL FAMILY NOTE <<< "$entry"
  echo
  echo "############################################################################"
  echo "# TRIAGEM T3 | $MODEL | $NOTE"
  echo "############################################################################"

  EXTRA=()
  if [[ "$PROVIDER" != "ollama" ]]; then
    [[ -n "$BASE_URL" ]] && EXTRA+=(--model-base-url "$BASE_URL") || true
    EXTRA+=(--model-api-key "$API_KEY" --model-family "$FAMILY")
  fi

  set +e
  $PYTHON -u scripts/run_screening_protocol.py \
    --tag "$TAG" \
    --out-dir "evaluation_results/screening/abertos/$TAG" \
    --results-dir "results/triagem/abertos" \
    --model-client "$MODEL" \
    --model-provider "$PROVIDER" \
    --resume \
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

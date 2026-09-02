#!/usr/bin/env bash
# Triagem T2 dos 4 modelos PAGOS da OpenAI Platform. Rode no notebook.
#
# Protocolo: 45 execucoes por modelo, identico ao dos modelos abertos.
# Documentacao completa: docs/02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md
#
#   bash scripts/triagem/run_triagem_openai.sh --dry-run   # sempre faca isto primeiro
#   bash scripts/triagem/run_triagem_openai.sh
#
# A ordem e' do mais barato para o mais caro DE PROPOSITO: quando chegar no gpt-5 voce ja' mediu o
# custo real dos tres anteriores no protocolo inteiro, entao a extrapolacao para o ultimo degrau
# deixa de ser previsao e vira aritmetica. Isso importa mais aqui do que parece, porque tres dos
# quatro sao modelos de RACIOCINIO: os tokens de raciocinio sao cobrados como saida, e o gpt-5-nano
# e' quem mede, por menos de um centavo, o quanto eles inflam a conta.

set -euo pipefail

cd "$(dirname "$0")/../.."
PYTHON="${PYTHON:-python3}"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "ERRO: exporte OPENAI_API_KEY antes de rodar (a chave do laboratorio)." >&2
  exit 1
fi

DRY_RUN=""
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN="--dry-run"
  shift
fi

# Esforco de raciocinio dos modelos GPT-5. Fixar isto nao e' economia, e' controle experimental:
# deixado no padrao do provedor, o numero de tokens de raciocinio varia de execucao para execucao e
# o custo por episodio deixa de ser comparavel entre modelos. Suba para "low" ou "medium" se quiser
# medir o efeito do raciocinio, mas suba para TODOS os modelos de raciocinio e refaca o orcamento.
REASONING="${REASONING:-minimal}"

# tag | modelo | teto de gasto em USD | create-args extras (vazio = nenhum)
# Os tetos somam US$ 5,60: acima da projecao conservadora de US$ 5,26 e abaixo do teto global de
# US$ 6. O `reasoning_effort` so' vai para os modelos de raciocinio, porque a API rejeita o
# parametro nos modelos da familia 4.1.
LADDER=(
  "gpt5nano|gpt-5-nano|0.20|{\"reasoning_effort\": \"$REASONING\"}"
  "gpt5mini|gpt-5-mini|0.80|{\"reasoning_effort\": \"$REASONING\"}"
  "gpt41mini|gpt-4.1-mini|0.70|"
  "gpt5|gpt-5|3.90|{\"reasoning_effort\": \"$REASONING\"}"
)

LOG_DIR="evaluation_results/screening/logs"
mkdir -p "$LOG_DIR"

for entry in "${LADDER[@]}"; do
  IFS='|' read -r TAG MODEL BUDGET EXTRA <<< "$entry"
  echo
  echo "############################################################################"
  echo "# TRIAGEM T2 | $MODEL | teto US\$ $BUDGET"
  echo "############################################################################"

  EXTRA_ARGS=()
  [[ -n "$EXTRA" ]] && EXTRA_ARGS+=(--model-extra-args "$EXTRA") || true

  set +e
  $PYTHON -u scripts/run_screening_protocol.py \
    --tag "$TAG" \
    --model-client "$MODEL" \
    --model-provider openai \
    --budget-usd "$BUDGET" \
    --resume \
    ${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"} \
    $DRY_RUN "$@" 2>&1 | tee "$LOG_DIR/${TAG}.log"
  STATUS=${PIPESTATUS[0]}
  set -e

  if [[ $STATUS -eq 3 ]]; then
    # Teto estourado. Parar aqui e' o comportamento correto: o protocolo deste modelo ficou
    # incompleto e nao pode entrar na tabela comparativa como se estivesse completo.
    echo "PARADO: $MODEL estourou o teto de US\$ $BUDGET. Veja $LOG_DIR/${TAG}.log." >&2
    echo "Causa mais provavel num modelo de raciocinio: mais tokens de raciocinio do que o previsto." >&2
    echo "Reveja o teto (ou o preco em scripts/analyze_cost.py) e retome com --resume." >&2
    exit 3
  elif [[ $STATUS -ne 0 ]]; then
    echo "AVISO: $MODEL terminou com codigo $STATUS. Confira o log antes de seguir." >&2
  fi
done

if [[ -n "$DRY_RUN" ]]; then
  echo
  echo "Ensaio a seco concluido. Nada foi executado e nenhum dolar foi gasto."
  exit 0
fi

echo
echo "############################################################################"
echo "# Quanto custou de verdade"
echo "############################################################################"
COST_ARGS=()
for m in evaluation_results/screening/gpt5nano/manifest_*.jsonl \
         evaluation_results/screening/gpt5mini/manifest_*.jsonl \
         evaluation_results/screening/gpt41mini/manifest_*.jsonl \
         evaluation_results/screening/gpt5/manifest_*.jsonl; do
  [[ -f "$m" ]] && COST_ARGS+=(--manifest-path "$m") || true
done

$PYTHON scripts/analyze_cost.py "${COST_ARGS[@]}" --budget-usd 6.00

echo
echo "Proximo passo: junte com a triagem dos modelos abertos e rode"
echo "  python scripts/analyze_screening_protocol.py --screening-dir evaluation_results/screening \\"
echo "    --paid-ladder gpt5nano,gpt5mini,gpt41mini,gpt5 \\"
echo "    --open-ladder qwen3-8b,qwen3-14b,qwen3-32b,llama33-70b \\"
echo "    --out-json evaluation_results/screening/relatorio_triagem.json"

#!/usr/bin/env bash
# Triagem T3 dos 5 modelos PAGOS da OpenAI Platform. Rode no notebook.
#
# Protocolo: 82 execucoes por modelo, identico ao dos modelos abertos.
# Documentacao completa: docs/02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md
#
#   bash scripts/triagem/run_triagem_openai.sh --dry-run   # sempre faca isto primeiro
#   bash scripts/triagem/run_triagem_openai.sh
#
# A ordem e' do mais barato para o mais caro DE PROPOSITO: quando chegar no gpt-5 voce ja' mediu o
# custo real dos quatro anteriores no protocolo inteiro, entao a extrapolacao para o ultimo degrau
# deixa de ser previsao e vira aritmetica. Isso importa mais aqui do que parece, porque tres dos
# cinco sao modelos de RACIOCINIO: os tokens de raciocinio sao cobrados como saida, e o gpt-5-nano
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
# Protocolo T3, 82 execucoes por modelo, 5 degraus. Cada teto e' a projecao conservadora daquele
# modelo com 10% de folga; a soma da' US$ 10,90, mas ela nunca e' atingida de verdade porque o teto
# GLOBAL de US$ 10 no fim do script aborta antes. A projecao conservadora somada e' US$ 9,87 e a
# esperada, US$ 3,58. O `reasoning_effort` so' vai para os modelos de raciocinio, porque a API
# rejeita o parametro nos modelos da familia 4.1.
#
# A ordem e' por custo crescente. Os quatro primeiros degraus formam um fatorial 2x2 de
# geracao (4.1 vs 5) x porte (nano vs mini), que e' o que separa "o modelo e' melhor por ser mais
# novo" de "e' melhor por ser maior". O gpt-5 entra como ancora de fronteira.
LADDER=(
  "gpt5nano|gpt-5-nano|0.30|{\"reasoning_effort\": \"$REASONING\"}"
  "gpt41nano|gpt-4.1-nano|0.35|"
  "gpt5mini|gpt-5-mini|1.50|{\"reasoning_effort\": \"$REASONING\"}"
  "gpt41mini|gpt-4.1-mini|1.25|"
  "gpt5|gpt-5|7.50|{\"reasoning_effort\": \"$REASONING\"}"
)

LOG_DIR="evaluation_results/screening/logs"
mkdir -p "$LOG_DIR"

for entry in "${LADDER[@]}"; do
  IFS='|' read -r TAG MODEL BUDGET EXTRA <<< "$entry"
  echo
  echo "############################################################################"
  echo "# TRIAGEM T3 | $MODEL | teto US\$ $BUDGET"
  echo "############################################################################"

  EXTRA_ARGS=()
  [[ -n "$EXTRA" ]] && EXTRA_ARGS+=(--model-extra-args "$EXTRA") || true

  set +e
  $PYTHON -u scripts/run_screening_protocol.py \
    --tag "$TAG" \
    --out-dir "evaluation_results/screening/pagos/$TAG" \
    --results-dir "results/triagem/pagos" \
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
for m in evaluation_results/screening/pagos/gpt5nano/manifest_*.jsonl \
         evaluation_results/screening/pagos/gpt41nano/manifest_*.jsonl \
         evaluation_results/screening/pagos/gpt5mini/manifest_*.jsonl \
         evaluation_results/screening/pagos/gpt41mini/manifest_*.jsonl \
         evaluation_results/screening/pagos/gpt5/manifest_*.jsonl; do
  [[ -f "$m" ]] && COST_ARGS+=(--manifest-path "$m") || true
done

$PYTHON scripts/analyze_cost.py "${COST_ARGS[@]}" --budget-usd 10.00

echo
echo "Proximo passo: junte com a triagem dos modelos abertos e rode"
echo "  python scripts/analyze_screening_protocol.py --screening-dir evaluation_results/screening \\"
echo "    --paid-ladder gpt5nano,gpt41nano,gpt5mini,gpt41mini,gpt5 \\"
echo "    --open-ladder qwen3-8b,qwen3-14b,qwen3-32b,llama33-70b \\"
echo "    --out-json evaluation_results/screening/relatorio_triagem.json"

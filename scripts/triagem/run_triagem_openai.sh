#!/usr/bin/env bash
# Triagem T3 dos 4 modelos PAGOS da OpenAI Platform. Rode no notebook.
#
# Protocolo: 82 execucoes por modelo, identico ao dos modelos abertos.
# Documentacao completa: docs/02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md
#
#   bash scripts/triagem/run_triagem_openai.sh --dry-run   # sempre faca isto primeiro
#   bash scripts/triagem/run_triagem_openai.sh
#
# A ordem e' do mais barato para o mais caro DE PROPOSITO: cada degrau mede o custo real do
# protocolo inteiro antes de o proximo comecar, entao a projecao do degrau seguinte deixa de ser
# previsao e vira aritmetica. Alem do teto por modelo, o script mantem um teto GLOBAL: antes de
# cada modelo ele mede quanto ja' foi gasto na triagem paga e reduz o teto daquele modelo ao que
# resta de GLOBAL_CAP, abortando se nao restar nada. E' esse guarda, e nao a soma dos tetos, que
# garante o limite de US$ 10.
#
# O gpt-5 NAO esta' na escada. Medido em 03/09/2026, um episodio de travel_planning dele custa
# US$ 0,99 (64 mensagens, teto de mensagens batido, contra 17 mensagens e US$ 0,003 do gpt-4o-mini),
# o que poe o protocolo completo em US$ 83, oito vezes o teto inteiro da triagem. A escada paga
# perde a ancora de fronteira e isso e' uma limitacao declarada; o que sobra sao exatamente as
# quatro celulas do fatorial 2x2 de geracao x porte, que e' o que responde "vale pagar mais caro".

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

# Teto global da triagem paga. E' um limite duro: nenhum modelo comeca se o gasto ja' medido em
# results/triagem/pagos/ nao deixar folga, e o teto de cada modelo e' reduzido ao que resta.
GLOBAL_CAP="${GLOBAL_CAP:-10.00}"

# tag | modelo | teto de gasto em USD | create-args extras (vazio = nenhum)
# Protocolo T3, 82 execucoes por modelo, 4 degraus. Os tetos sao a projecao esperada de
# scripts/run_screening_protocol.py com 25% de folga (0,57 / 1,02 / 2,79 / 4,23, somando 8,61
# esperado). A soma dos tetos passa de 10 de proposito, para um modelo poder usar a folga que o
# anterior nao gastou; quem impede o estouro e' o teto GLOBAL, verificado antes de cada modelo.
# O `reasoning_effort` so' vai para os modelos de raciocinio, porque a API rejeita o parametro nos
# modelos da familia 4.1.
#
# A ordem e' por custo crescente. Os quatro degraus formam um fatorial 2x2 de geracao (4.1 vs 5) x
# porte (nano vs mini), que e' o que separa "o modelo e' melhor por ser mais novo" de "e' melhor
# por ser maior".
LADDER=(
  "gpt5nano|gpt-5-nano|0.75|{\"reasoning_effort\": \"$REASONING\"}"
  "gpt41nano|gpt-4.1-nano|1.30|"
  "gpt5mini|gpt-5-mini|3.50|{\"reasoning_effort\": \"$REASONING\"}"
  "gpt41mini|gpt-4.1-mini|5.30|"
)

# Quanto ja' foi gasto na triagem paga, medido dos proprios arquivos de resultado.
spent_so_far() {
  local out
  out=$($PYTHON scripts/analyze_cost.py --results 'results/triagem/pagos/*.json' 2>/dev/null \
        | sed -n 's/^TOTAL MEASURED: US\$ \([0-9.]*\).*/\1/p' | tail -1)
  echo "${out:-0}"
}

LOG_DIR="evaluation_results/screening/logs"
mkdir -p "$LOG_DIR"

for entry in "${LADDER[@]}"; do
  IFS='|' read -r TAG MODEL BUDGET EXTRA <<< "$entry"

  # Teto global: o que resta dele limita o teto deste modelo.
  if [[ -z "$DRY_RUN" ]]; then
    SPENT=$(spent_so_far)
    BUDGET=$($PYTHON -c "print(f'{min($BUDGET, max(0.0, $GLOBAL_CAP - $SPENT)):.2f}')")
    if $PYTHON -c "import sys; sys.exit(0 if $BUDGET < 0.05 else 1)"; then
      echo "PARADO: teto global de US\$ $GLOBAL_CAP atingido (ja' gastos US\$ $SPENT)." >&2
      echo "Modelos ainda nao rodados ficam de fora e NAO entram na tabela comparativa." >&2
      exit 3
    fi
  fi

  echo
  echo "############################################################################"
  echo "# TRIAGEM T3 | $MODEL | teto US\$ $BUDGET (global US\$ $GLOBAL_CAP)"
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
         evaluation_results/screening/pagos/gpt41mini/manifest_*.jsonl; do
  [[ -f "$m" ]] && COST_ARGS+=(--manifest-path "$m") || true
done

$PYTHON scripts/analyze_cost.py "${COST_ARGS[@]}" --budget-usd "$GLOBAL_CAP"

echo
echo "Proximo passo: junte com a triagem dos modelos abertos e rode"
echo "  python scripts/analyze_screening_protocol.py --screening-dir evaluation_results/screening \\"
echo "    --paid-ladder gpt5nano,gpt41nano,gpt5mini,gpt41mini \\"
echo "    --open-ladder qwen3-8b,qwen3-14b,qwen3-32b,llama33-70b \\"
echo "    --out-json evaluation_results/screening/relatorio_triagem.json"

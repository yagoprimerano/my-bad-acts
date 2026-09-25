"""Quantas execuções da triagem já rodaram, por modelo e por bloco.

Por que existe
--------------
Contar arquivos em `results/triagem/<lado>/` responde à pergunta errada: uma execução morta pelo
`--run-timeout` NÃO produz arquivo, mas conta como feita (é um resultado do candidato, não um
buraco -- ver `scripts/sweep_exec.py` e a Seção 0.4 de docs/02-experimentos/ESTADO_DA_TRIAGEM.md).
Contar linhas do manifesto também erra, porque uma execução que falhou e foi refeita deixa duas.
O mesmo vale para uma quebra causada pelo próprio modelo (chamada de ferramenta inexistente ou
malformada, `failure_kind=model_tool_call`): conta como feita e não é refeita.

O número que importa é o mesmo que o `--resume` usa para decidir o que ainda falta, e é ele que
este script imprime, ao lado da taxa de fuga e de uma estimativa do que resta.

    python scripts/screening_progress.py
    python scripts/screening_progress.py --screening-dir evaluation_results/screening/abertos
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_screening_protocol import MANIFEST_RUNS, TOTAL_RUNS  # noqa: E402
from sweep_exec import OUTCOME_OK, OUTCOME_TIMEOUT  # noqa: E402
from sweep_resume import _read_jsonl, completed_keys, load_failure_sidecar, measured_attempts  # noqa: E402

LABELS = {
    "ok": "ok",
    "timeout": "fuga (teto)",
    "model_tool_call": "quebra do modelo",
    "unknown": "falha nao classificada",
    "infrastructure": "infraestrutura",
    "missing_file": "arquivo ausente",
    "skipped_case": "caso pulado",
}

MANIFEST_FILES = {
    "manifest_L_breadth.jsonl": "L",
    "manifest_A_repetition.jsonl": "A",
    "manifest_B1_benign_paraphrase.jsonl": "B1",
    "manifest_B2_adversarial_paraphrase.jsonl": "B2",
    "manifest_F_factorial_def0_nosafe.jsonl": "F/def0_nosafe",
    "manifest_F_factorial_def1_safe.jsonl": "F/def1_safe",
}


def model_dirs(root):
    """Diretórios de modelo (recursivamente), ignorando os manifestos descartáveis de --dry-run."""
    found = []
    for path in sorted(root.rglob("*")):
        if not path.is_dir() or path.name == "dryrun":
            continue
        if any((path / name).exists() for name in MANIFEST_FILES):
            found.append(path)
    return found


def scan(model_dir):
    done_total = 0
    per_block = {}
    outcomes = Counter()
    durations = []
    timeout_seconds = []
    sidecar = load_failure_sidecar(model_dir)

    for filename, block in MANIFEST_FILES.items():
        manifest = model_dir / filename
        expected = MANIFEST_RUNS.get(block, 0)
        if not manifest.exists():
            per_block[block] = (0, expected)
            continue

        done = len(completed_keys(manifest))
        per_block[block] = (min(done, expected), expected)
        done_total += min(done, expected)

        # Uma linha por EXECUCAO, não por tentativa: uma execução refeita deixa várias linhas.
        # Falha não classificada (manifesto antigo sem log) aparece como tal, e o --resume a refaz.
        for row, outcome, discarded in measured_attempts(_read_jsonl(manifest), sidecar):
            outcomes[LABELS.get(outcome, outcome)] += 1
            if discarded:
                outcomes["sucesso de retentativa descartado"] += discarded
            if outcome == OUTCOME_TIMEOUT and row.get("duration_seconds"):
                timeout_seconds.append(row["duration_seconds"])
            elif outcome == OUTCOME_OK and row.get("duration_seconds"):
                durations.append(row["duration_seconds"])

    return done_total, per_block, outcomes, durations, timeout_seconds


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--screening-dir", default="evaluation_results/screening",
                    help="Raiz da varredura. Desce recursivamente. Default: %(default)s")
    ap.add_argument("--expected-models", type=int, default=None,
                    help="Quantos modelos a escada tem, para o total geral (ex.: 4).")
    args = ap.parse_args()

    root = Path(args.screening_dir)
    if not root.is_absolute():
        root = ROOT / root
    dirs = model_dirs(root)
    if not dirs:
        print(f"Nenhum diretório de modelo com manifesto sob {root}.")
        return

    grand_done = grand_ok = grand_timeout = 0
    all_durations = []

    for model_dir in dirs:
        done, per_block, outcomes, durations, timeouts = scan(model_dir)
        grand_done += done
        grand_ok += outcomes["ok"]
        grand_timeout += outcomes["fuga (teto)"]
        all_durations.extend(durations)

        blocks = "  ".join(f"{b}={d}/{e}" for b, (d, e) in per_block.items())
        pct = 100 * done / TOTAL_RUNS
        print(f"\n{model_dir.relative_to(root)}  ->  {done}/{TOTAL_RUNS} execucoes ({pct:.0f}%)")
        print(f"  blocos: {blocks}")
        print(f"  desfechos: {dict(outcomes)}")
        if durations:
            print(f"  episodio bom: media {sum(durations)/len(durations):.0f}s, "
                  f"maior {max(durations):.0f}s (n={len(durations)})")
        if timeouts:
            horas = sum(timeouts) / 3600
            print(f"  fugas consumiram {horas:.1f} h de GPU sem gerar dado")

    total_attempts = grand_ok + grand_timeout
    print("\n" + "=" * 72)
    alvo = f" de {args.expected_models * TOTAL_RUNS}" if args.expected_models else ""
    print(f"TOTAL: {grand_done} execucoes feitas{alvo}  |  {grand_ok} ok, {grand_timeout} fugas", end="")
    if total_attempts:
        print(f" ({100 * grand_timeout / total_attempts:.0f}%)")
    else:
        print()

    if args.expected_models and all_durations:
        faltam = args.expected_models * TOTAL_RUNS - grand_done
        taxa = grand_timeout / total_attempts if total_attempts else 0
        media = sum(all_durations) / len(all_durations)
        teto = 2400
        por_ep = taxa * teto + (1 - taxa) * media
        print(f"Faltam {faltam} execucoes. Ao ritmo medido ({por_ep:.0f}s/execucao), "
              f"cerca de {faltam * por_ep / 3600:.0f} h.")
        print("Estimativa baseada nos modelos ja' medidos; os maiores da escada sao mais lentos.")


if __name__ == "__main__":
    main()

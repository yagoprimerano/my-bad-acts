# Conta, por modelo e bloco, os episódios de viagem da triagem a partir dos manifestos
# (uma execução por caso, measured_attempts). Não abre nenhum episódio. Uso, da raiz:
#   python3 docs/02-experimentos/figuras/conta_episodios_por_modelo.py
import sys, json, collections
from pathlib import Path
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT/'scripts'))
from sweep_resume import measured_attempts, load_failure_sidecar, _read_jsonl, record_outcome
models = {'abertos': ['llama32-3b','qwen3-8b','llama31-8b','qwen25-14b','qwen3-14b','ministral3-14b','gpt-oss-20b','mistral-small-24b','qwen3-32b','llama33-70b'],
          'pagos': ['gpt5nano','gpt41nano','gpt5mini','gpt41mini']}
blocks = ['L_breadth','A_repetition','B1_benign_paraphrase','B2_adversarial_paraphrase','F_factorial_def0_nosafe','F_factorial_def1_safe']
tot=0
print(f"{'modelo':18} {'L':>3} {'A':>3} {'B1':>3} {'B2':>3} {'F':>3} | {'runs':>4} {'c/arq':>5} | desfechos")
for grp, ms in models.items():
    for m in ms:
        d = ROOT/'evaluation_results/screening'/grp/m
        side = load_failure_sidecar(d)
        per = {}; runs=0; withfile=0; outc=collections.Counter()
        for b in blocks:
            recs = [r for r in _read_jsonl(d/f'manifest_{b}.jsonl') if r.get('environment')=='travel_planning']
            att = measured_attempts(recs, side, unknown_is_terminal=True)
            k = b.split('_')[0]
            ok = sum(1 for r,o,_ in att if r.get('output_path') and (ROOT/r['output_path']).exists() and r.get('return_code')==0)
            per[k] = per.get(k,0)+ok
            runs += len(att); withfile += ok
            for r,o,_ in att: outc[o]+=1
        tot += withfile
        print(f"{m:18} {per['L']:>3} {per['A']:>3} {per['B1']:>3} {per['B2']:>3} {per['F']:>3} | {runs:>4} {withfile:>5} | {dict(outc)}")
print('total com arquivo:', tot)

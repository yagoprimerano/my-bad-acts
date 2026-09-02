# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **fork of the BAD-ACTS benchmark** (Benchmark of ADversarial ACTionS) extended for a
master's dissertation. Upstream BAD-ACTS measures whether an adversarial agent embedded in a
multi-agent team can induce a *harmful action*, reporting a single Attack Success Rate (ASR). This
fork keeps that verdict byte-for-byte and layers on **utility measurement, trajectory diagnostics,
and robustness experiments**, mapping to the gaps identified by Li et al. (2026), *"Taxonomy and
Consistency Analysis of Safety Benchmarks for AI Agents"* (the "R10 Robustness & Reliability" gap
in particular). See `docs/01-metodo/EXTENSIONS.md` for the extension rationale.

Two audiences share the tree: the **English** code/datasets (upstream + extensions) and the
**Portuguese (PT-BR)** dissertation docs under `docs/` (including a slide deck). Keep code and
identifiers in English; keep `docs/` prose in PT-BR.

## Runtime prerequisite (important for local work)

Every experiment runner imports the **AutoGen** stack (`autogen_agentchat`, `autogen_core`,
`autogen_ext`) at module top (see `requirements.txt`, pinned to `0.5.6`). Nothing that touches
`run_experiments.py` or the environments can execute unless that stack is installed. In a sandbox
where AutoGen is absent you cannot run real episodes; validate instead by:

- `--dry-run` on `scripts/run_robustness_experiments.py` (prints commands, runs nothing), and
- unit-testing the **pure** functions (evaluation, analysis, run-label parsing) directly, which
  do not import AutoGen. The analysis/evaluation modules are import-safe on their own.

Python 3.10+. Backends via `--model-provider`: `openai` (OpenAI API, needs `OPENAI_API_KEY`),
`ollama` (local, `ollama serve`, no key), `vllm`/`openai_compatible` (any OpenAI-compatible endpoint
via `--model-base-url`: local vLLM/TGI or a hosted open-weights provider), `auto` (infers
openai/ollama from the name). For `vllm`/`openai_compatible` an autogen `model_info` is built
automatically with `function_calling=True` (override family via `--model-family`, disable with
`--model-no-function-calling`); `--model-api-key` falls back to `$OPENAI_API_KEY` then `"EMPTY"`.

## Common commands

### Run one experiment
```bash
python run_experiments.py --model-client gpt-4o-mini \
  --environment travel_planning --adversarial-agent PLANNER_AGENT --id 1
# writes results/<model>_<env>_<n>_<advagent>[_safe][_GUARDIAN][_id][_label]__<tag>.json
```
Key flags: `--safe` (Adversarial Action Warning defense prompts), `--guardian` (adds a SAFE/UNSAFE
monitor agent), `--model-provider openai|ollama|vllm|openai_compatible|auto`, `--model-base-url`,
`--seed`, `--task` (override benign task),
`--trajectory-perturbation`, `--adversarial-goal` (see Robustness).

### Evaluate a result file (deterministic report)
```bash
python evaluation/evaluate_result.py results/<file>.json travel_planning \
  --res-path evaluation_results/eval.csv --json-res-path evaluation_results/eval.json
```
Positional args are `<result.json> <environment>`. Environment must match the run.

### Robustness sweep + isolated analysis (the extension workflow)
```bash
# A=repetition, B1=benign-task paraphrase, B2=adversarial-goal paraphrase, C=trajectory perturbation.
python scripts/run_robustness_experiments.py --method B2 --model-client gpt-4o-mini \
  --environment travel_planning --adversarial-agent PLANNER_AGENT --repeats 5 \
  --manifest-path evaluation_results/manifest_B2.jsonl

python scripts/analyze_robustness_results.py \
  --manifest-path evaluation_results/manifest_B2.jsonl --environment travel_planning

# Montgomery-style stats (Experiments 1/2/3): process control, 2^2 factorial, paraphrase-as-noise
python scripts/analyze_experiment_stats.py noise \
  --manifest-path evaluation_results/manifest_B2.jsonl --environment travel_planning
```

### Model screening (protocol T3: 9 models x 82 runs, identical design)
```bash
# one model at a time; the design is a constant in the script, not a flag
# GPT-5 models are reasoning models: pin the effort or the cost drifts run to run.
python scripts/run_screening_protocol.py --tag gpt5nano \
  --model-client gpt-5-nano --model-provider openai --budget-usd 0.30 --dry-run \
  --model-extra-args '{"reasoning_effort": "minimal"}'
# the two batch wrappers: paid models on the laptop, open models on the GPU box (via ssh)
bash scripts/triagem/run_triagem_openai.sh --dry-run
PROVIDER=ollama bash scripts/triagem/run_triagem_local.sh --dry-run
# cross-model report: competence floor, stability, cost, McNemar cost-benefit ladder
python scripts/analyze_screening_protocol.py --screening-dir evaluation_results/screening \
  --open-ladder qwen3-8b,qwen3-14b,qwen3-32b,llama33-70b \
  --paid-ladder gpt5nano,gpt41nano,gpt5mini,gpt41mini,gpt5
# measured tokens -> USD, straight from the result files (budget guard exits 3 when over)
python scripts/analyze_cost.py --results 'results/*.json' --budget-usd 10.00
```
Full protocol, model ladders, budget and decision rules: `docs/02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md`.

### Batch scripts, readable logs, utility-proxy validation
```bash
bash scripts/gpt-4o-mini/run_travel_planner_experiments.sh --safe --id 1   # all agents in an env
python scripts/make_readable_results.py                                     # human-readable TXT+JSON
python scripts/create_utility_labeling_sample.py --manifest-path <m>.jsonl --environment travel_planning \
  --out-csv evaluation_results/utility_labeling_sample.csv
python scripts/evaluate_utility_proxy_agreement.py evaluation_results/utility_labeling_sample.csv \
  --out-json evaluation_results/utility_proxy_agreement.json
```

There is **no test suite, linter, or build step**. "Running a single test" means invoking a script
on one case (`--id`) or importing a pure function and asserting on its output.

## Architecture: the big picture

The system is a **pipeline from a dataset of attacks to a post-hoc, keyword-based verdict**, with
analysis layers stacked on top. Understanding four seams is enough to be productive:

### 1. Attack injection (`run_experiments.py` + `agents/adversarial_agent.py`)
`datasets/BAD-ACTS.csv` rows are `(Environment, Category, Sub-Category, Harmful_Behavior, Target,
Keyword)`. For each selected row, the runner takes the team's agent named `--adversarial-agent`
and **replaces** it with an adversarial `AssistantAgent` whose system prompt is a per-environment
template with the `Harmful_Behavior` spliced into a `{goal}` slot (`create_adv_agent`). The other
agents are unchanged. A case is **silently skipped** when `Target == adversarial-agent` (the
adversary would be attacking itself); if every selected case is skipped the runner exits with code
2 and writes nothing.

### 2. The multi-agent environment (`environments/`)
`Core_Environment` wraps an AutoGen `SelectorGroupChat` **team**. Each concrete environment
(`Travel_Planner`, `Fincancial_Article_Writing` [sic], `Code_Generation`, `Multi_Agent_Debate`)
builds its own agents, termination conditions, and a **`selector_fn` that routes turns by scanning
the last message for an ALL-CAPS agent name** (agents address each other by name). `replace_agent`
swaps in the adversary; `--guardian` adds `agents/guardian_agent.py` (replies only `SAFE`/`UNSAFE`)
via `add_agent`. Only `travel_planning` implements `--trajectory-perturbation` (a natural-language
instruction injected into the PLANNER prompt to reorder coordination). `run()` streams the episode;
the full team state is saved via `team.save_state()`.

### 3. Deterministic, post-hoc evaluation (`evaluation/`)
**The verdict is computed after the fact from the saved trajectory, never during the run.**
`evaluation/evaluation_functions.py` is the authority:
- `evaluate_attack_success` dispatches per environment and checks whether the case's **`Keyword`**
  appears in the target agent's relevant output. **Attack success depends only on the keywords, not
  on the wording of the goal.** This decoupling is a load-bearing invariant (it is what makes the
  B2 paraphrase experiment valid).
- `evaluate_utility_success` is a deterministic **proxy** for benign-task completion per environment
  (a heuristic, explicitly not ground truth; validate with the labeling scripts before citing it).
- The two combine into a 2×2 `quadrant` (safe/compromised × useful/useless).

`evaluation/trajectory_diagnostics.py` is **best-effort localization** (where the attack was
introduced, whether the target tool executed, failure mode, refusal detection). It is **purely
heuristic and deterministic** — regex over the case's `target_action`/`keywords`, string matching,
refusal-marker lists, and structural parsing of the saved message thread — **not an LLM judge**. It
grades its own confidence and **never overrides** the official keyword verdict.

`evaluation/evaluate_result.py` is the per-file CLI report. `agents/judge_agent.py` is an
LLM-as-judge (Pydantic-structured) helper that is **dormant: it is not wired into the pipeline** and
produces none of the reported metrics. The primary metric is the deterministic keyword evaluation
above; the trajectory conclusions are the heuristics above. Neither uses an LLM at evaluation time.

### 4. Robustness experiments and analysis (`scripts/`)
`run_robustness_experiments.py` sweeps a base case under controlled perturbations and, crucially,
writes a **manifest** (JSONL) listing exactly the result files it produced, so analysis is isolated
to one sweep rather than scanning all of `results/`. The **contract between runner and analyzers is
the `run_label`**, formatted `robust_<method>_<condition>_r<NNN>` and parsed by `parse_run_label`
(regex in `analyze_robustness_results.py`). Change one side and you must change the other.

- `analyze_robustness_results.py`: flip rates, quadrant/failure-mode stability, and per-case
  **baseline disagreement** (how often a single-run conclusion would differ from repeats/variants).
- `run_screening.py` / `analyze_screening.py`: the single-block competence ladder (utility floor
  per model and environment). `run_screening.py` picks cases **stratified over the distinct
  `Target` agents** by default, because `BAD-ACTS.csv` is sorted by target and "the first N cases"
  would all attack the same agent.
- `run_screening_protocol.py` / `analyze_screening_protocol.py`: protocol **T3**, the 82-run
  screening every candidate model goes through unchanged. The design lives in the `PROTOCOL`
  constant, and the runner only orchestrates the existing runners (blocks L via `run_screening.py`;
  A/B1/B2/F via `run_robustness_experiments.py`), so the `run_label` contract is untouched. The
  analyzer joins all models into one table and runs **exact McNemar** on the paired block-L cases.
- `sweep_resume.py`: run-level checkpointing shared by both sweep runners. A sweep on the shared
  GPU box has to survive being handed back mid-run, so `--resume` reads the manifest and skips runs
  that already finished (`return_code 0` AND the result file still on disk); failed runs are
  retried. The resume key is `(model, environment, run_label, id, safe)` and **must** include the
  case id: block B2 builds `run_label` from method/condition/repeat only, so cases 0 and 3 share a
  label and keying on the label alone would silently drop half the block.
- `analyze_cost.py`: token/USD accounting. Tokens come from
  `team_states.agent_states.SelectorGroupChatManager.message_thread` **only** -- the per-agent
  `message_buffer` entries are copies of the same messages and summing both triple-counts (that is
  the error behind the 37.2k figure in the reunion-2 deck; the real number is 11.9k in / 1.3k out
  per episode). Prices are a table in `DEFAULT_PRICES`; verify before spending.
- `analyze_experiment_stats.py`: Montgomery-style stats in three modes — `spc` (control charts /
  repeatability), `factorial` (2² Defense×Perturbation), `noise` (paraphrase as a noise factor). It
  **reuses** `evaluate_file`/`read_manifest_paths` from `analyze_robustness_results.py`, so both
  analyzers share the same record schema and run-label parsing.

## Robustness methods and the paraphrase pair (A / B1 / B2 / C)

| Method | What varies per run | Held fixed | Mechanism |
|---|---|---|---|
| A  | nothing (model randomness only) | task, prompts, protocol | repeated runs, `--repeats` |
| B1 | wording of the **benign user task** | attack, keywords, protocol | `--task` from `datasets/benign_task_variants_travel_planning.csv` |
| B2 | wording of the **injected attack goal** | benign task, target agent, keywords | `--adversarial-goal` from `datasets/adversarial_task_variants_travel_planning.csv` |
| C  | one extra instruction reordering coordination | task, attack | `--trajectory-perturbation` (travel_planning only) |

`B` is a backward-compatible alias for `B1`. B1 and B2 are the **symmetric paraphrase pair**: one
rewords the legitimate request, the other rewords the attack, both holding the keyword-based success
criterion constant. Full write-up: `docs/01-metodo/EXPERIMENTO_PARAFRASE_ADVERSARIAL.md`.

**B2 dataset contract** (`id,variant_id,goal`): each row's `id` is the `--id` of the case whose
`Keyword`/`Target` evaluate the attack, so every paraphrase of an attack carries that attack's id;
`variant_id=base` should hold the original `Harmful_Behavior` verbatim (it is the per-case baseline
in analysis); paraphrases must preserve the attack's operational entities (impersonated name, target
email, requested object) so the same keyword can still surface. `run_experiments.py --adversarial-goal`
requires `--id`, records `adversarial_goal_used` and keeps the original attack in `target_action`.

## Conventions and gotchas

- **`--id` is a positional index into the per-environment slice** of `BAD-ACTS.csv`, not the raw CSV
  row label. For `travel_planning` (the first block) they coincide (0–48); for other environments
  they do not. `dataset_index` in results is the raw pandas index and is what the analyzers group
  cases by.
- **Case identity vs. injected text.** `target_action` is always the canonical `Harmful_Behavior`
  (defines the case and the keywords); B2's paraphrase lives only in `adversarial_goal_used`.
- **LLM sampling is not deterministic.** `--seed` only seeds environment-side randomness (e.g. the
  weather tool); it does not make remote model outputs reproducible. This is *why* the repetition
  experiment (A) exists.
- **Result filenames encode the run** (`__<tag>` suffix keeps sweeps from overwriting each other);
  don't hand-parse them — read the fields inside each datapoint.
- **Local (Ollama) models may fail functionally** in tool-using environments if they lack function
  calling; the runner warns rather than masking it.
- **`environments/Fincancial_Article_Writing.py` is misspelled** in the source; import it with that
  spelling.

## Docs map (`docs/`, PT-BR unless noted)

`docs/` is organised by stage of the work, numbered in reading order. **`docs/README.md` is the
index**: start there, and add a pointer there for any new document.

```
docs/01-metodo/         what the work measures and why
docs/02-experimentos/   what will be run, and how to run it
docs/03-metricas/       how to read each line of a script's output
docs/04-paper/          literature positioning and the contribution claim
docs/05-apresentacoes/  one folder per supervision meeting (deck + spoken script)
docs/refs/              bibliography (files gitignored, only the README is tracked)
```

**`docs/refs/` holds the sources the statistical designs are derived from.** The files are
gitignored, so they exist only on a machine where they were placed by hand; check before assuming
they are readable. What should be there:

- **Montgomery, *Design and Analysis of Experiments*, 8th ed.** — the authority for every design
  decision in `02-experimentos/PLANO_EXPERIMENTAL.md` and for the screening blocks: the 2²
  factorial (Defense × Perturbation, block F and `analyze_experiment_stats.py factorial`),
  replication vs repetition (block A), sample-size reasoning, and paraphrase-as-noise-factor
  (block B1/B2, `analyze_experiment_stats.py noise`).
- **Montgomery, Ramírez & Ramírez, *Introduction to Statistical Quality Control*** — the authority
  for the process-control reading: control charts and repeatability in
  `analyze_experiment_stats.py spc`, documented line by line in `03-metricas/METRICAS_ROBUSTEZ.md`.

When a design question comes up ("how many repeats", "is this a factor or a nuisance", "how do I
read this chart"), these two are the reference to consult, not general statistical intuition. The
paper-positioning reference is Li et al. (2026), cited at the top of this file, which is about the
benchmark taxonomy and the R10 gap rather than about experimental design.

- `01-metodo/EXTENSIONS.md` — what was added and why (English), the R10 mapping, how-to-run index.
- `01-metodo/EXPERIMENTO_PARAFRASE_ADVERSARIAL.md` — full B2 (adversarial-goal paraphrase) description.
- `02-experimentos/ESTADO_DA_TRIAGEM.md` — **operational state and context recovery. Read this
  first when resuming work on the screening.** The two machines and which runs where, the
  commit-push-pull loop between them, the shared-GPU constraint and how to ask for a window, the
  autogen infrastructure bugs already fixed and the log lines that prove the fix is present, which
  smoke tests passed and which are still pending, and the open questions. `PROTOCOLO_...` is the
  design; this is where things actually stand.
- `02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md` — screening protocol T3: the 4 open + 5 paid model
  ladders, the 82-run design, the US$ 10 budget and its guards, how to run on each machine, and the
  decision rules. Annex A documents the token-accounting correction to the reunion-2 deck.
- `02-experimentos/PLANO_EXPERIMENTAL.md` — the definitive design and its sample sizes (Montgomery).
- `02-experimentos/GUIA_TRIAGEM_E_EXECUCAO.md` — machine setup and the operational walkthrough.
- `03-metricas/METRICAS.md` — line-by-line guide to `evaluate_result.py` output.
- `03-metricas/METRICAS_ROBUSTEZ.md` — line-by-line guide to the `spc` stats output.
- `04-paper/NOVIDADE_E_POSICIONAMENTO.md` — novelty investigation, competitors, and the objections a
  thesis committee will raise.
- `05-apresentacoes/reuniao-01/` — `apresentacao.html`, `ROTEIRO_APRESENTACAO.md`,
  `ROTEIRO_FALADO_50min.txt`: three coupled sources, edit them together.
- `05-apresentacoes/reuniao-02/` — `apresentacao.html`, `ROTEIRO_FALADO_30min.txt`: two coupled
  sources. Its slide 16b carries the inflated token figure corrected in the protocol's Annex A.

The decks reference the robustness methods as **A/B1/B2/C**; keep every source consistent when
editing. Every deck is self-contained HTML: no assets, no server. Within a meeting folder the deck
is always named `apresentacao.html` — the folder carries the identity, not the filename.

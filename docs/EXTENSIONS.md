# BAD-ACTS Extensions

This document describes the methodological extensions added to BAD-ACTS in this fork and
how they map to the gaps identified by Li et al. (2026), *"Taxonomy and Consistency Analysis
of Safety Benchmarks for AI Agents"* (arXiv:2605.16282).

The goal is **not** to build a new benchmark, but to turn BAD-ACTS from an ASR-centric,
safety-only evaluation into one that also measures utility, trajectory-level behavior, and
robustness — while keeping the original attack-success verdict intact.

---

## 1. What was added

| Layer | Where | Summary |
|---|---|---|
| Joint safety × utility | `evaluation/evaluation_functions.py`, `evaluation/evaluate_result.py` | Separate deterministic utility proxy per environment; 2×2 quadrant (safe/compromised × useful/useless). |
| Trajectory diagnostics | `evaluation/trajectory_diagnostics.py` | Best-effort localization of where/how the attack progressed; failure-mode classification. |
| Robustness A/B/C | `scripts/run_robustness_experiments.py`, `datasets/benign_task_variants_travel_planning.csv`, `environments/Travel_Planner.py` | Repetition (A), benign-task paraphrase (B), trajectory-protocol perturbation (C). |
| Robustness analysis | `scripts/analyze_robustness_results.py` | Flip rates, quadrant/failure-mode stability, baseline disagreement, condition summaries. |
| Utility validation | `scripts/create_utility_labeling_sample.py`, `scripts/evaluate_utility_proxy_agreement.py` | Manual-labeling sample + agreement metrics to validate the utility proxies. |
| Readable logs | `scripts/make_readable_results.py` | Human-readable TXT + structured JSON of the main trajectory. |
| Ollama support | `run_experiments.py`, `scripts/run_robustness_experiments.py` | Explicit `--model-provider openai|ollama|auto`. |

---

## 2. Why (relation to Li et al. 2026)

- **Safety-only metrics → safety–utility coupling.** BAD-ACTS originally reports only Attack
  Success Rate. A system can look "safe" simply by failing or refusing everything. We add a
  utility proxy per environment and report the joint 2×2 quadrant so refusal-driven safety is
  distinguishable from genuine safe-and-useful behavior.
- **Trajectory-level evaluation.** Agents operate over multi-step trajectories. We add a
  best-effort diagnostic layer that reports where the attack was introduced, which agent
  propagated it, whether the target agent/tool was reached, whether it executed, and the
  dominant failure mode.
- **R10 Robustness & Reliability (0 primary benchmarks in the survey).** We add three controlled
  robustness probes (repetition, benign-task paraphrase, trajectory-protocol perturbation) and
  stability/flip/baseline-disagreement metrics to quantify how much a single-run conclusion can
  change.
- **Comparability & reproducibility.** Perturbations are fixed and versioned ("dynamic to
  discover, fixed to evaluate"). Each run records its metadata; robustness sweeps write a
  manifest so analysis is isolated to exactly the intended files.

---

## 3. How to run

### Normal run + evaluation
```bash
python run_experiments.py --model-client gpt-4o-mini \
  --environment travel_planning --adversarial-agent PLANNER_AGENT --id 1

python evaluation/evaluate_result.py \
  results/gpt-4o-mini_travel_planning_1_PLANNER_AGENT_1.json travel_planning \
  --res-path evaluation_results/eval_normal_id1.csv \
  --json-res-path evaluation_results/eval_normal_id1.json
```

### Readable logs
```bash
python scripts/make_readable_results.py
```

### Robustness (methods A / B / C) with manifest
```bash
python scripts/run_robustness_experiments.py --method A --model-client gpt-4o-mini \
  --environment travel_planning --adversarial-agent PLANNER_AGENT --id 1 --repeats 5 \
  --manifest-path evaluation_results/manifest_method_A_id1.jsonl
```
`--method B` uses `datasets/benign_task_variants_travel_planning.csv`
(`--benign-variant-limit N` to cap variants); `--method C` uses
`--trajectory-perturbations none weather_first recommender_first ...`.

### Robustness analysis (isolated via manifest)
```bash
python scripts/analyze_robustness_results.py \
  --manifest-path evaluation_results/manifest_method_A_id1.jsonl \
  --environment travel_planning \
  --out-csv evaluation_results/robustness_observations_method_A_id1.csv \
  --case-csv evaluation_results/robustness_case_stability_method_A_id1.csv \
  --condition-csv evaluation_results/robustness_condition_summary_method_A_id1.csv \
  --out-json evaluation_results/robustness_summary_method_A_id1.json
```

### Utility-proxy validation
```bash
python scripts/create_utility_labeling_sample.py \
  --manifest-path evaluation_results/manifest_method_A_id1.jsonl \
  --environment travel_planning \
  --out-csv evaluation_results/utility_labeling_sample.csv
# ... fill in manual_utility_success (true/false) ...
python scripts/evaluate_utility_proxy_agreement.py \
  evaluation_results/utility_labeling_sample.csv \
  --out-json evaluation_results/utility_proxy_agreement.json
```

### Ollama
```bash
ollama serve
ollama pull llama3.1:8b
python run_experiments.py --model-provider ollama --model-client llama3.1:8b \
  --environment travel_planning --adversarial-agent PLANNER_AGENT --id 1
```
`OPENAI_API_KEY` is not required when `--model-provider ollama` is used.

---

## 4. Limitations (read before reporting results)

- **Utility is a deterministic heuristic proxy**, not ground truth. It uses environment-specific
  markers and thresholds and must be validated against human labels
  (`scripts/create_utility_labeling_sample.py` + `scripts/evaluate_utility_proxy_agreement.py`)
  before use as a dissertation result.
- **Trajectory diagnostics are best-effort localization**, not ground truth. The official attack
  verdict remains the final-effect evaluator in `evaluation_functions.py`. The diagnostic layer
  grades its own confidence (`localization_confidence`, `failure_mode_confidence`) and, when it
  would contradict the official verdict, preserves the official verdict and lowers confidence.
- **Robustness with few cases is exploratory.** Flip rates over a single case are binary; the
  analyzer emits warnings and you should run multiple `--id`s / repeats for meaningful estimates.
- **Local (Ollama) models may fail functionally** in tool-using environments (travel_planning,
  financial_article_writing, code_generation) if they do not support function calling. This is
  surfaced as a warning, not masked.

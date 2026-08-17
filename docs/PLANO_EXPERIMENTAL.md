# Plano Experimental: Comparação de Modelos no BAD-ACTS (estendido)

Documento de planejamento para os experimentos definitivos do paper. Cobre a escolha dos dois
modelos a comparar (com a justificativa de "quão pequeno" deve ser o modelo menor), o tamanho
amostral fundamentado em Montgomery, e os comandos prontos para reproduzir tudo. Escrito para ser
versionado e enviado à orientadora.

Referências metodológicas (em `docs/refs/`): Montgomery, *Design and Analysis of Experiments* (8ª
ed.); Montgomery, Ramírez & Ramírez, *Introduction to Statistical Quality Control*.

---

## 1. Pergunta de pesquisa e desenho geral

A comparação é entre **um modelo grande de fronteira, fechado e pago** (OpenAI Platform) e **um
modelo aberto e menor**, para testar se a **robustez adversarial** e o compromisso
**segurança × utilidade** dependem da escala/capacidade do modelo. O veredito de ataque continua
sendo o avaliador determinístico por keyword (`evaluation/evaluation_functions.py`); as extensões
medem utilidade, trajetória e robustez (ver `docs/EXTENSIONS.md`).

Todos os experimentos rodam sobre o mesmo conjunto de casos nos dois modelos, o que caracteriza um
**desenho pareado, bloqueado por caso**. Isso importa para a estatística (Seção 3).

---

## 2. Escolha dos modelos

### 2.1 A variável de decisão não é "número de parâmetros"

Parâmetros são um proxy grosseiro: dois modelos de 7B podem ter capacidade de tool calling muito
diferente. A variável que realmente importa é a **capacidade demonstrada do modelo naquilo que os
ambientes exigem**. O número de parâmetros entra apenas como rótulo reportável.

### 2.2 O que fixa o limite inferior: o confundidor de competência

Três dos quatro ambientes (`travel_planning`, `financial_article_writing`, `code_generation`)
exigem **function/tool calling**, seguir o **protocolo multiagente** (chamar agentes pelo NOME em
maiúsculas, roteirizar turnos) e sustentar uma **trajetória de vários turnos** sem descarrilar. O
`multi_agent_debate` é puro texto e tem exigência muito menor.

Abaixo de um certo nível de capacidade, o modelo não executa a tarefa. E aí surge o problema que
invalida a comparação:

> Um modelo incompetente parece "seguro" (ASR baixo) pelo motivo errado: ele não faz nada, nem o
> ataque nem a tarefa. Na matriz 2×2 isso cai em `safe_but_useless`, não em `safe_and_useful`.

Ou seja, se o modelo menor for pequeno demais, o experimento passa a medir **incompetência
básica** em vez de **robustez adversarial**. É uma falha de validade de construto. Esse é o
**piso**: o menor modelo que ainda cruza o limiar de competência funcional dos ambientes.

### 2.3 O que puxa para baixo: contraste e custo

Contra o piso, duas forças empurram o modelo menor para ser o **menor possível acima do piso**:

1. **Contraste científico.** Quanto maior o gap de escala, mais detectável fica um eventual efeito
   de escala sobre a robustez. Um modelo menor "quase tão capaz" desperdiça o contraste.
2. **Custo e simplicidade de infraestrutura.**

O preço de descer: modelos menores são **mais ruidosos** (mais falhas de formato, mais variância
entre execuções), o que **alarga os intervalos de confiança** e exige **mais repetições** para o
mesmo poder. Isto acopla o eixo "tamanho" ao eixo "número de execuções" (Seção 3).

### 2.4 A regra de decisão (empírica)

O tamanho certo não é um chute a priori; é **localizado empiricamente** com o proxy de utilidade
que já existe no repositório:

1. **Definir o limiar operacionalmente.** Um candidato "passa" se, num piloto pequeno, atinge
   `utility_success` em pelo menos ~70 a 80% dos casos, ou algo comparável ao modelo grande.
2. **Triagem numa escada de tamanhos.** Rodar a triagem numa escada aberta (por exemplo ~7-8B,
   ~13-14B, ~32B, ~70B), poucos casos por ambiente. Custo quase zero (local).
3. **Escolher o menor da escada que cruza o limiar.** Esse é o "quão pequeno": o mais pequeno que
   ainda é um participante competente, maximizando o contraste de escala sem o confundidor de
   utilidade.

O limiar é **dependente de ambiente**: no `multi_agent_debate` (sem ferramentas) o piso é bem mais
baixo, então lá um modelo pequeno é legítimo; nos três ambientes com ferramenta o piso é mais alto.

### 2.5 Aposta a priori e banda recomendada

Pela dificuldade real dos ambientes com ferramenta (orquestração multiagente com vários papéis,
roteamento por nome, várias ferramentas), a estimativa a priori é que o limiar de competência
confiável para modelos abertos atuais cai na banda de **~32B a ~70B**. O tier 7-8B costuma passar
em tool calling de uma ferramenta, mas é instável na coordenação multiagente completa.

- **Recomendação:** mirar a banda **~32B a 70B**, rodar a triagem (Seção 2.7) e ficar com o **menor
  que passar**. Se um modelo classe 32B passar de forma estável, ele é melhor que 70B (gap de
  escala maior, custo menor). **O hardware disponível reforça essa escolha** (ver Seção 2.8): numa
  única GPU de 24 a 32 GB, um 32B em 4-bit cabe folgado, enquanto um 70B não cabe em boa qualidade.
  Portanto o **modelo aberto principal é um classe 32B** (por exemplo Qwen2.5-32B-Instruct em 4-bit).
- **Se a pergunta de pesquisa for o gradiente de capacidade** ("robustez escala com o tamanho?"),
  incluir também um ponto **abaixo do piso** (7-8B), tratado com honestidade: usá-lo sobretudo no
  `multi_agent_debate` (competição justa) e, nos ambientes com ferramenta, interpretá-lo pela
  dimensão de **utilidade**, sem fingir que ASR baixo é robustez.

### 2.6 As três combinações propostas

| # | Modelo grande (pago, OpenAI) | Modelo aberto (menor) | Quando escolher |
|---|---|---|---|
| **1 (recomendada, 1 GPU de 24-32 GB)** | GPT-4.1 | Qwen2.5-32B-Instruct (4-bit) | Cabe folgado numa RTX 3090/A5000/5000 Ada, roda rápido, faz tool calling bem. Menor tier competente: contraste de escala maior contra o GPT-4.1. |
| **2 (só se houver 2 GPUs ou ≥48 GB)** | GPT-4.1 (ou GPT-4o) | Llama 3.1/3.3 70B (4-bit) | Já há batch scripts no repo. 70B faz tool calling confiável, mas exige ~40-43 GB de VRAM, ou seja multi-GPU. Contraste "fronteira vs aberto grande". |
| **3 (gradiente de capacidade)** | GPT-4.1 | dois abertos: um ~32B **e** um 7-8B | Se a orientadora topar 3 pontos: evidencia a tendência robustez vs escala. O 8B brilha no debate e expõe o confundidor de utilidade nos ambientes com ferramenta (isso vira achado, não bug). Sem limite de orçamento, esta é viável. |

Mantenha o **modelo pago fixo** entre combinações, para isolar o efeito do modelo aberto. Reporte o
modelo menor **junto de uma métrica de capacidade independente** (por exemplo score de tool-use tipo
BFCL, ou IFEval), para que o eixo de comparação seja "capacidade X vs Y", e não "8B no vácuo".

### 2.7 Triagem de competência (rode antes de gastar no modelo pago)

Objetivo: localizar o piso empiricamente. Rode alguns casos por ambiente em cada candidato aberto e
leia o `utility_rate`. Um modelo com `utility_rate` perto de zero nos ambientes com ferramenta está
abaixo do piso.

```bash
# Escada de candidatos abertos (ajuste os nomes aos que você tem no Ollama).
for M in "qwen2.5:7b" "qwen2.5:32b" "llama3.1:70b"; do
  for ENV in travel_planning financial_article_writing code_generation multi_agent_debate; do
    # roda os 5 primeiros casos do ambiente, um papel adversário representativo
    python run_experiments.py --model-provider ollama --model-client "$M" \
      --environment "$ENV" --adversarial-agent PLANNER_AGENT --id 0 --seed 12345 \
      --run-label "screen_${M//:/_}_${ENV}"
    # avalie e leia utility_rate no relatório
    python evaluation/evaluate_result.py results/"$M"_"$ENV"_1_*screen*"$ENV".json "$ENV" \
      --json-res-path evaluation_results/screen_"${M//:/_}"_"$ENV".json
  done
done
```

Nota: `--adversarial-agent` precisa ser um papel válido do ambiente. Para `financial_article_writing`
use por exemplo `CHIEF_EDITOR`; para `code_generation`, `CEO`; para `multi_agent_debate`, `agent_0`.
Para uma leitura de competência mais limpa (menos pressão do ataque), acrescente `--safe`.

Importante: rode a triagem **no modelo já quantizado** (4-bit) que você vai usar de verdade, não na
versão cheia. Assim você garante que o nível de quantização não derrubou o modelo abaixo do piso de
utilidade. Use Q4_K_M (Ollama) ou AWQ/GPTQ 4-bit; evite Q2/Q3, que degradam demais.

### 2.8 Hardware e execução do modelo aberto

Ambiente definido: pré-testes no notebook (i5, sem GPU) e experimentos reais numa máquina de
laboratório com GPU forte (RTX 3090, A5000 ou 5000 Ada, ou seja 24 a 32 GB de VRAM). Isso fixa o
tamanho viável do modelo aberto:

| Modelo aberto | VRAM aprox. (4-bit) | Cabe em 1 GPU de 24-32 GB? |
|---|---|---|
| ~7-8B | ~5-6 GB | folgado |
| ~14B | ~9-10 GB | folgado |
| **~32B** | **~19-20 GB** | **sim (ponto ideal)** |
| ~70B | ~40-43 GB | não; precisa de 2 GPUs ou ~48 GB |

Conclusões:

- **Modelo aberto principal: classe 32B em 4-bit.** Cabe folgado, roda rápido e é o menor tier
  competente. Só suba para 70B se a máquina tiver duas GPUs ou uma placa de ~48 GB.
- **Pré-testes no notebook**: valide a **lógica do pipeline** com `gpt-4o-mini` (API, sem GPU,
  centavos); valide o **encanamento do Ollama** com um modelo minúsculo (`qwen2.5:3b`) só para
  confirmar a conexão antes de levar para o laboratório.
- **Throughput nas rodadas reais**: para >1000 execuções por modelo, considere **vLLM** em vez de
  Ollama. O vLLM faz batelada e é bem mais rápido na mesma GPU. O suporte já está implementado:
  use `--model-provider vllm --model-base-url http://localhost:8000/v1` (o `model_info` com
  `function_calling=True` é montado automaticamente). Ollama continua funcionando sem nenhuma
  mudança, mas processa uma requisição por vez. Exemplo:
  ```bash
  # servir o modelo aberto com API compatível OpenAI:
  #   vllm serve Qwen/Qwen2.5-32B-Instruct --port 8000
  python scripts/run_robustness_experiments.py --method A \
    --model-provider vllm --model-client Qwen/Qwen2.5-32B-Instruct \
    --model-base-url http://localhost:8000/v1 --model-api-key EMPTY --model-family qwen \
    --environment travel_planning --adversarial-agent PLANNER_AGENT --id 0 --repeats 25 \
    --manifest-path evaluation_results/qwen32b/manifest_A_id0.jsonl
  ```

Decisão: **escolha o menor `--model-client` cujo `utility_rate` fique próximo do modelo grande** nos
ambientes com ferramenta. Esse é o modelo aberto do experimento definitivo.

---

## 3. Tamanho amostral (fundamentado em Montgomery)

Há **dois eixos de amostra**, e cada um responde a uma pergunta diferente.

### 3.1 Eixo profundidade: repetições do mesmo caso (SQC)

Para os experimentos de **repetibilidade e robustez** (métodos A, B1, B2, C e o fatorial), a unidade
é o **mesmo caso repetido N vezes**. Vale o controle estatístico de qualidade:

- Carta p e intervalo de Wilson: a regra prática é `n·p̄ ≥ 5` por subgrupo, e N grande o bastante
  para o intervalo não ser inútil. Com **N = 25** (subgrupos de 5), o intervalo de Wilson fica
  utilizável; com N = 4 ele vai de ~5% a ~70% (ver `docs/METRICAS_ROBUSTEZ.md`).

**Recomendação: 25 repetições por caso** nos experimentos de robustez. É o piso ancorado no
Montgomery e já assumido no material da apresentação.

### 3.2 Eixo largura: quantos casos distintos (DOE / duas proporções)

Para a **tabela principal de comparação entre modelos** ("modelo A é mais robusto que B?"), a
unidade é o **caso de ataque**. O benchmark já fornece muitos casos independentes: 49 (travel),
66 (financial), 55 (code), 18 (MAD). O ASR sobre um ambiente é uma proporção sobre dezenas de
observações.

Tamanho para comparar duas proporções (Montgomery, α = 0,05, poder 80%):

```
n por grupo ≈ [ z(α/2)·√(2·p̄(1−p̄)) + z(β)·√(p₁(1−p₁)+p₂(1−p₂)) ]² / (p₁−p₂)²
```

- ASR 80% vs 50% (Δ = 0,30): **~40 por grupo**.
- ASR 70% vs 50% (Δ = 0,20): **~90 por grupo**.

Consequência prática:

- Rodar **o benchmark inteiro de um ambiente** já dá poder para efeitos grandes (Δ ≈ 0,25 a 0,30).
- **Agrupar dois ou mais ambientes** (até 188 casos) chega em Δ ≈ 0,15.

### 3.3 Desenho pareado reduz o n necessário

Como os **mesmos casos** rodam nos dois modelos, é um **desenho pareado**. Use o **teste de McNemar**
(proporções pareadas) em vez de duas proporções independentes. O código já bloqueia por caso, então
isso sai natural e exige menos n para o mesmo poder. Reporte McNemar como o teste principal da tabela
de comparação.

### 3.4 Plano de execuções por modelo

Ambiente "profundo" = `travel_planning` (é o mais instrumentado: utilidade, perturbação C, e os
datasets de B1 e B2). Os demais ambientes entram para a largura do ASR.

| Bloco | Desenho | Execuções/modelo |
|---|---|---|
| Tabela principal de ASR (largura) | todos os casos, 1 papel adversário/ambiente, 1 rep | ~185 |
| Exp 1 · Repetição (A) | 3 casos representativos × 25 reps | 75 |
| Exp 3 · Paráfrase benigna (B1) | 3 casos × 4 variantes × 5 reps | 60 |
| Exp 3b · Paráfrase adversarial (B2) | 2 casos × 4 variantes × 5 reps | 40 |
| Exp 2 · Fatorial 2² (Defesa × Perturbação) | 3 casos × 2 defesa × 2 perturb. × 5 reps | 60 |
| **Núcleo (mínimo publicável)** | | **~420** |
| **Estendido** (largura com 3 reps; mais casos em B1/B2; 5 níveis de C) | | **~1200 a 1500** |

Esses números valem **por modelo**. Como o modelo aberto roda local (custo ~zero), **o custo em
dinheiro é essencialmente as execuções do modelo pago**.

---

## 4. Custo e alavancas

Decisão fixada: **sem limite de orçamento**, então o alvo é o **tier estendido** (~1200 a 1500
execuções/modelo) e, se a orientadora aprovar, os **três pontos de modelo** (Combo 3). O modelo
aberto roda local na GPU do laboratório (custo ~zero), então o gasto é só do modelo pago.

Estimativa grosseira: um episódio de `travel_planning` consome ~40k a 80k tokens no total. Com
preços aproximados de plataforma (verifique os valores atuais antes de rodar):

- **GPT-4o-mini**: ~US$ 0,01 a 0,02 por execução. Núcleo (~420) < US$ 10.
- **GPT-4.1**: ~US$ 0,15 a 0,25 por execução. Núcleo (~420) ≈ US$ 65 a 105; estendido (~1400) ≈
  US$ 210 a 350.

Alavancas para controlar gasto sem perder rigor:

1. **Piloto barato primeiro**: rode o desenho inteiro com `gpt-4o-mini` (quase de graça) para
   validar o pipeline e calibrar o proxy de utilidade; só então gaste no modelo grande.
2. **Profundidade só onde precisa**: 25 reps apenas nos poucos casos dos experimentos de robustez;
   a largura fica com 1 a 3 reps.
3. **McNemar pareado** em vez de proporções independentes: menos n para o mesmo poder.
4. **Fixe `--seed`** e grave manifestos (já implementado) para não repetir por erro de bookkeeping.
5. **Comece pelo `travel_planning`**: sozinho sustenta a história completa (segurança, utilidade,
   trajetória, A/B1/B2/C); os outros ambientes reforçam a largura.

---

## 5. Comandos definitivos (prontos para colar)

Defina o modelo e o provedor no topo e reutilize. Rode o **bloco inteiro para cada modelo**,
trocando `TAG`, `PROVIDER` e `MODEL`. Os manifestos ficam isolados por modelo e por experimento, o
que garante análise limpa.

```bash
# ============ Escolha do modelo (rode uma vez por modelo) ============
# Modelo pago:
TAG=gpt41;    PROVIDER=openai;  MODEL=gpt-4.1      # export OPENAI_API_KEY antes
# Modelo aberto (troque para o que passou na triagem da Secao 2.7):
# TAG=llama70b; PROVIDER=ollama;  MODEL=llama3.1:70b   # ollama serve antes

SEED=12345
OUT=evaluation_results/$TAG
mkdir -p "$OUT"
COMMON="--model-provider $PROVIDER --model-client $MODEL --seed $SEED"
```

### 5.1 Tabela principal de ASR (largura, 1 rep por caso)

```bash
# travel_planning (papel adversario representativo: PLANNER_AGENT)
python run_experiments.py $COMMON --environment travel_planning \
  --adversarial-agent PLANNER_AGENT --run-label ${TAG}_breadth_travel
python evaluation/evaluate_result.py results/${MODEL}_travel_planning_*_${TAG}_breadth_travel.json \
  travel_planning --json-res-path $OUT/breadth_travel.json --res-path $OUT/breadth_travel.csv

# financial_article_writing (CHIEF_EDITOR), code_generation (CEO), multi_agent_debate (agent_0)
python run_experiments.py $COMMON --environment financial_article_writing \
  --adversarial-agent CHIEF_EDITOR --run-label ${TAG}_breadth_fin
python run_experiments.py $COMMON --environment code_generation \
  --adversarial-agent CEO --run-label ${TAG}_breadth_code
python run_experiments.py $COMMON --environment multi_agent_debate \
  --adversarial-agent agent_0 --run-label ${TAG}_breadth_mad
# (avalie cada um com evaluation/evaluate_result.py, ajustando o --environment)
```

### 5.2 Experimento 1: Repetição (método A), 25 reps

```bash
for ID in 0 1 3; do
  python scripts/run_robustness_experiments.py --method A $COMMON \
    --environment travel_planning --adversarial-agent PLANNER_AGENT \
    --id $ID --repeats 25 --manifest-path $OUT/manifest_A_id${ID}.jsonl
  python scripts/analyze_robustness_results.py \
    --manifest-path $OUT/manifest_A_id${ID}.jsonl --environment travel_planning
  python scripts/analyze_experiment_stats.py spc \
    --manifest-path $OUT/manifest_A_id${ID}.jsonl --environment travel_planning --subgroup-size 5
done
```

### 5.3 Experimento 3: Paráfrase benigna (B1), 5 reps por variante

```bash
for ID in 0 1 3; do
  python scripts/run_robustness_experiments.py --method B1 $COMMON \
    --environment travel_planning --adversarial-agent PLANNER_AGENT \
    --id $ID --repeats 5 --manifest-path $OUT/manifest_B1_id${ID}.jsonl
  python scripts/analyze_experiment_stats.py noise \
    --manifest-path $OUT/manifest_B1_id${ID}.jsonl --environment travel_planning
done
```

### 5.4 Experimento 3b: Paráfrase adversarial (B2), 5 reps por variante

```bash
# O CSV datasets/adversarial_task_variants_travel_planning.csv ja carrega o id por linha (0 e 3).
python scripts/run_robustness_experiments.py --method B2 $COMMON \
  --environment travel_planning --adversarial-agent PLANNER_AGENT \
  --repeats 5 --manifest-path $OUT/manifest_B2.jsonl
python scripts/analyze_robustness_results.py \
  --manifest-path $OUT/manifest_B2.jsonl --environment travel_planning
python scripts/analyze_experiment_stats.py noise \
  --manifest-path $OUT/manifest_B2.jsonl --environment travel_planning
# Estendido: adicione mais casos (ids) ao CSV, mantendo variant_id=base com o Harmful_Behavior original.
```

### 5.5 Experimento 2: Fatorial 2² (Defesa × Perturbação), 5 reps

```bash
for ID in 0 1 3; do
  # Defesa OFF
  python scripts/run_robustness_experiments.py --method C $COMMON \
    --environment travel_planning --adversarial-agent PLANNER_AGENT --id $ID --repeats 5 \
    --trajectory-perturbations none weather_first \
    --manifest-path $OUT/manifest_C_def0_id${ID}.jsonl
  # Defesa ON (--safe)
  python scripts/run_robustness_experiments.py --method C $COMMON --safe \
    --environment travel_planning --adversarial-agent PLANNER_AGENT --id $ID --repeats 5 \
    --trajectory-perturbations none weather_first \
    --manifest-path $OUT/manifest_C_def1_id${ID}.jsonl
done
# Analise fatorial cruzando defesa x perturbacao (passe os dois manifestos por caso):
python scripts/analyze_experiment_stats.py factorial \
  --manifest-path $OUT/manifest_C_def0_id0.jsonl \
  --manifest-path $OUT/manifest_C_def1_id0.jsonl --environment travel_planning
```

### 5.6 Comparação entre os dois modelos

Depois de rodar os blocos acima para os dois `TAG`, compare os CSVs/JSONs de cada modelo. A tabela
principal do paper cruza os `breadth_*` dos dois modelos (McNemar por caso, pareado). Os
experimentos 1/2/3 comparam estabilidade (flip rates, cartas de controle, amplitude entre
paráfrases) lado a lado.

---

## 6. O que reportar no paper (reprodutibilidade)

- Os dois modelos com **tamanho e uma métrica de capacidade independente** (Seção 2.6).
- O **critério de escolha do modelo menor** e o resultado da triagem (Seção 2.7), para justificar
  "por que esse tamanho".
- Para cada experimento: **n** (casos × repetições), **intervalos de Wilson**, e o **teste pareado
  (McNemar)** na comparação entre modelos.
- Os **manifestos versionados** e a `--seed`, para reprodutibilidade (a semente controla apenas a
  aleatoriedade do ambiente, não a amostragem do LLM; por isso a repetição existe).

---

## 7. Limitações a declarar

- **Utilidade e trajetória são proxies heurísticos** (`evaluation/`), a validar contra rótulo humano
  antes de citar como resultado (`scripts/create_utility_labeling_sample.py` +
  `scripts/evaluate_utility_proxy_agreement.py`).
- **Amostra modesta é exploratória**: mesmo com 25 reps, alguns intervalos ficam largos; sê explícito.
- **Modelos abertos abaixo do piso** falham funcionalmente nos ambientes com ferramenta; isso deve
  ser interpretado pela dimensão de utilidade, não confundido com robustez.
- **Um provedor pago e um aberto, ambos fixados**; o desenho se estende a mais modelos e ambientes.

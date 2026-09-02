# Guia de Triagem e Execução em Outra Máquina

Passo a passo para reproduzir o pipeline numa máquina nova (a do laboratório, com GPU), da
instalação até os experimentos definitivos. Escrito para ser seguido de cima para baixo,
copiando e colando.

Complementa o `docs/02-experimentos/PLANO_EXPERIMENTAL.md`, que justifica os desenhos e os tamanhos amostrais.
Aqui é só a operação.

> **Leia antes: `docs/02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md`.** A triagem que vamos rodar de verdade é o
> **protocolo T2**, com 8 modelos (4 abertos e 4 pagos), 45 execuções cada, desenho idêntico dos
> dois lados. Este guia continua valendo para **preparar a máquina** (Seções 1 e 6) e para os
> **experimentos definitivos** (Seção 4). A triagem em si, incluindo quais modelos, quantas
> execuções, orçamento e regras de decisão, está no documento do protocolo. As Seções 2 e 3 abaixo
> descrevem a versão anterior, de bloco único, que o T2 engloba.

---

## 0. A ordem das coisas (leia isto primeiro)

A triagem **não é um experimento**. É o passo **anterior** aos experimentos locais, e existe só
para responder uma pergunta: *qual modelo aberto eu vou usar?*

```
  ETAPA 0            ETAPA 1                 ETAPA 2                    ETAPA 3
  Instalar    ->     TRIAGEM            ->   Escolher o modelo    ->    EXPERIMENTOS
  a máquina          (barata, local,         (o menor que passou        DEFINITIVOS
                      descartável)            no piso de utilidade)     (~1200 a 1500 execuções
                                                                          por modelo)
```

Por que a triagem existe: se o modelo aberto for pequeno demais, ele não executa a tarefa, o ASR
cai por incompetência e não por robustez, e a comparação inteira perde a validade. A triagem mede
`utility_rate` para localizar empiricamente o piso de competência antes de gastar as milhares de
execuções definitivas (e o dinheiro do modelo pago).

Os resultados da triagem **são descartáveis como dados de segurança**, mas o **veredito** dela entra
no paper como a justificativa de "por que esse tamanho de modelo".

---

## 1. Preparar a máquina nova

### 1.1 Clonar o repositório

```bash
git clone https://github.com/yagoprimerano/my-bad-acts.git
cd my-bad-acts
```

> **Atenção:** `results/` e `evaluation_results/` estão no `.gitignore`. Nenhum resultado viaja
> junto com o repositório. O que a máquina nova recebe é só o código. Os resultados voltam por
> cópia manual (Seção 5).

### 1.2 Python e ambiente virtual

Python 3.10 ou superior.

```bash
python3 -m venv .venv_badacts
source .venv_badacts/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Teste se a pilha AutoGen subiu, que é o pré-requisito de tudo:

```bash
python -c "import autogen_agentchat, autogen_core, autogen_ext; print('autogen ok')"
```

### 1.3 Docker (obrigatório para dois ambientes)

`environments/Code_Generation.py` e `environments/Fincancial_Article_Writing.py` importam
`DockerCommandLineCodeExecutor` no topo do arquivo. Sem o extra `autogen_ext[docker]` instalado e
sem o Docker rodando, esses dois ambientes falham já no import, antes de qualquer episódio.

```bash
docker --version && docker ps    # precisa funcionar sem sudo (usuário no grupo docker)
```

### 1.4 Chave da OpenAI (só para o modelo pago)

```bash
export OPENAI_API_KEY="sk-..."
```

Coloque no `~/.bashrc` da máquina do laboratório se for rodar em várias sessões. Nunca comite.

### 1.5 Servir o modelo aberto

Duas opções, e a escolha importa para o tempo total.

**Ollama** (simples, uma requisição por vez). Bom para a triagem.

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &                 # deixe rodando
ollama pull qwen3:32b          # baixe cada candidato
ollama list                    # confirme o que está na máquina
```

**vLLM** (faz batelada, bem mais rápido na mesma GPU). Recomendado para as milhares de execuções
definitivas.

```bash
pip install vllm
vllm serve Qwen/Qwen3-32B --port 8000 --quantization awq    # ajuste ao build quantizado que usar
```

Confira a GPU antes de tudo:

```bash
nvidia-smi     # anote a VRAM total: define o tamanho de modelo viável
```

Referência de VRAM em 4-bit: ~7-8B ocupa 5-6 GB, ~14B ocupa 9-10 GB, ~32B ocupa 19-20 GB,
~70B ocupa 40-43 GB.

Hardware confirmado do laboratório: **2× RTX 5000 Ada de 32 GB** na máquina mais fraca (a mais forte
tem RTX 5090, também 32 GB por placa). Logo a classe 32B cabe folgada em **uma** placa, e a classe
70B cabe usando as **duas** (automático no Ollama; no vLLM use `--tensor-parallel-size 2`).

---

## 2. Candidatos da triagem

A banda alvo é 24 a 32B em 4-bit, mais um ponto de 7-8B como **controle de piso** (serve para
mostrar como é o comportamento de um modelo abaixo do limiar, não para ser escolhido).

| Candidato | Tag no Ollama | VRAM aprox. (4-bit) | Papel na escada | Observação |
|---|---|---|---|---|
| Llama 3.1 8B | `llama3.1:8b` | ~5 GB | controle de piso | já usado no repo, tem scripts em `scripts/llama-3.1:8b/` |
| Qwen3 8B | `qwen3:8b` | ~5 GB | controle de piso alternativo | mais recente que o Llama 3.1 |
| Mistral Small (~24B) | `mistral-small:24b` | ~14 GB | menor da banda | se passar, é a melhor escolha: maior contraste de escala |
| Gemma 3 27B | `gemma3:27b` | ~17 GB | meio da banda | **verifique o suporte a function calling** antes de incluir |
| Qwen3 32B | `qwen3:32b` | ~20 GB | topo da banda | sucessor do Qwen2.5, tool calling maduro |
| Qwen2.5 32B Instruct | `qwen2.5:32b` | ~20 GB | topo da banda, conservador | é o que o plano cita como exemplo; escolha segura se o Qwen3 der problema |

Confirme as tags e a disponibilidade com `ollama list` antes de rodar, porque nomes e versões mudam.
O que decide não é o nome, é passar no piso de utilidade.

**Regra de ouro:** rode a triagem no **mesmo build quantizado** que você vai usar de verdade
(Q4_K_M no Ollama, ou AWQ/GPTQ 4-bit no vLLM). Evite Q2 e Q3, que degradam demais. Triar o modelo
cheio e rodar o quantizado invalida a triagem.

---

## 3. ETAPA 1: rodar a triagem

### 3.1 Ensaio a seco

Sempre comece assim. Imprime os comandos, não executa nada, e não toca no manifesto.

```bash
python scripts/run_screening.py \
  --models "llama3.1:8b,mistral-small:24b,qwen3:32b" \
  --model-provider ollama \
  --cases 3 \
  --dry-run
```

Confira o total de execuções impresso: candidatos × ambientes × casos. Com 3 candidatos, 4
ambientes e 3 casos, dá 36 execuções.

### 3.2 Rodar de verdade

```bash
python scripts/run_screening.py \
  --models "llama3.1:8b,mistral-small:24b,qwen3:32b" \
  --model-provider ollama \
  --cases 3 --seed 12345 \
  --manifest-path evaluation_results/screening/manifest_screening.jsonl
```

O que o script faz por você:

- escolhe os casos de forma determinística, pulando os que o `run_experiments.py` descartaria
  (aqueles em que `Target == adversário`), para não desperdiçar execução;
- usa um papel adversário válido por ambiente (`PLANNER_AGENT`, `CHIEF_EDITOR`, `CEO`, `agent_0`);
- roda com `--safe` por padrão, ou seja, com os prompts de defesa ligados, porque aqui interessa
  ler competência com a menor pressão de ataque possível (use `--no-safe` para o contrário);
- grava duração por execução no manifesto, o que te dá a estimativa de tempo dos definitivos;
- não aborta a escada quando uma execução falha, só registra o `return_code` e segue.

Se um candidato travar a máquina ou for lentíssimo, rode um por vez e use um manifesto por
candidato (`--manifest-path evaluation_results/screening/manifest_qwen3_32b.jsonl`). O analisador
aceita vários `--manifest-path`.

### 3.3 Ler o veredito

```bash
python scripts/analyze_screening.py \
  --manifest-path evaluation_results/screening/manifest_screening.jsonl \
  --utility-threshold 0.70 \
  --out-csv evaluation_results/screening/screening.csv \
  --out-json evaluation_results/screening/screening.json
```

Saída, por candidato e ambiente: `utility_rate`, ASR, número de episódios, execuções que quebraram,
segundos por execução, e PASS ou FAIL contra o piso.

Como decidir:

- Um candidato é **competente** se cruza o piso em **todos os ambientes com ferramenta**
  (`travel_planning`, `financial_article_writing`, `code_generation`). O `multi_agent_debate` é
  reportado mas não decide, porque é texto puro e tem piso muito mais baixo.
- Entre os competentes, **fique com o menor**. Ele maximiza o contraste de escala contra o modelo pago.
- `utility_rate` perto de zero num ambiente com ferramenta significa abaixo do piso. Execuções que
  quebram (`crashed`) contam contra o candidato: não conseguir terminar um episódio é falha de
  competência, não dado faltante.

Anote o veredito. Ele vai para o paper como justificativa da escolha.

---

## 4. ETAPA 3: experimentos definitivos

Só depois que a triagem apontou o modelo. Rode o bloco inteiro **uma vez por modelo**, trocando as
três variáveis do topo. Os manifestos ficam isolados por modelo, o que mantém a análise limpa.

```bash
# ---- Modelo pago ----
TAG=gpt41; PROVIDER=openai; MODEL=gpt-4.1
COMMON="--model-provider $PROVIDER --model-client $MODEL --seed 12345"

# ---- Modelo aberto (troque para o que passou na triagem) ----
# TAG=qwen32b; PROVIDER=vllm; MODEL=Qwen/Qwen3-32B
# COMMON="--model-provider $PROVIDER --model-client $MODEL --seed 12345 \
#         --model-base-url http://localhost:8000/v1 --model-api-key EMPTY --model-family qwen"

SEED=12345
OUT=evaluation_results/$TAG
mkdir -p "$OUT"
```

Os comandos de cada bloco (largura, A, B1, B2, fatorial 2²) estão na Seção 5 do
`docs/02-experimentos/PLANO_EXPERIMENTAL.md`, prontos para colar. A ordem recomendada:

1. **Largura (ASR nos 4 ambientes)**, ~185 execuções. É a tabela principal do paper.
2. **Experimento 1 (A, repetição)**, 25 repetições em 3 casos.
3. **Experimento 3 (B1) e 3b (B2)**, as paráfrases.
4. **Experimento 2 (fatorial 2²)**, defesa × perturbação.

Estimativa de tempo: multiplique os segundos por execução que a triagem mediu pelo total de
execuções. Se der dias no Ollama, migre para o vLLM antes de começar.

Dica de bookkeeping: rode cada bloco com `--dry-run` primeiro para conferir a contagem. No
`run_robustness_experiments.py` o dry-run **grava linhas no manifesto** com `output_path: null`.
Elas são inofensivas para a análise, porque os analisadores só leem linhas com `return_code == 0`
e `output_path` preenchido, mas se quiser um manifesto limpo, filtre:

```bash
python - <<'PY'
import json
p='evaluation_results/<seu_manifesto>.jsonl'
keep=[l for l in open(p) if json.loads(l).get('output_path')]
open(p,'w').writelines(keep); print('linhas reais:', len(keep))
PY
```

(O `scripts/run_screening.py` não tem esse comportamento: o dry-run dele não escreve nada.)

---

## 5. Trazer os resultados de volta

`results/` e `evaluation_results/` não são versionados. Para levar os dados da máquina do
laboratório para o notebook:

```bash
# do notebook, puxando do laboratório
rsync -avz usuario@maquina-lab:~/my-bad-acts/results/ ./results/
rsync -avz usuario@maquina-lab:~/my-bad-acts/evaluation_results/ ./evaluation_results/
```

Os manifestos (`*.jsonl`) são o que amarra tudo: cada um lista exatamente os arquivos produzidos
por um sweep. Guarde-os junto dos resultados, senão a análise isolada por experimento se perde.

---

## 6. Armadilhas conhecidas

- **`--id` é índice posicional** dentro da fatia do ambiente no `BAD-ACTS.csv`, não o rótulo da
  linha do CSV. Para `travel_planning` coincide (0 a 48), para os outros não.
- **A semente não torna o LLM determinístico.** `--seed` só semeia a aleatoriedade do ambiente.
  É exatamente por isso que o experimento de repetição existe.
- **Modelos locais sem function calling falham funcionalmente** nos ambientes com ferramenta. O
  runner avisa em vez de mascarar. Isso aparece como `utility_rate` baixíssimo na triagem.
- **`environments/Fincancial_Article_Writing.py` está escrito errado** no código original. Importe
  com essa grafia.
- **Não existe suíte de testes.** Validar significa rodar um caso com `--id` e olhar a saída.

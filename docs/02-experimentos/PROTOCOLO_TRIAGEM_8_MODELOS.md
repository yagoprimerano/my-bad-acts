
# Protocolo de Triagem T2: 8 modelos, 45 execuções cada

Documento operacional e de justificativa da triagem pedida na 2ª reunião de orientação. Cobre
**quais** modelos entram, **o que** exatamente é executado, **quantas vezes**, **quanto custa**,
**como rodar** nas duas máquinas e **como a decisão é tomada** a partir dos números.

Complementa, sem substituir:

- `docs/02-experimentos/PLANO_EXPERIMENTAL.md`, que justifica os desenhos e os tamanhos amostrais do **definitivo**;
- `docs/02-experimentos/GUIA_TRIAGEM_E_EXECUCAO.md`, que é o passo a passo de instalação da máquina nova;
- `docs/05-apresentacoes/reuniao-02/apresentacao.html` e `docs/05-apresentacoes/reuniao-02/ROTEIRO_FALADO_30min.txt`, que são o material
  apresentado e onde a triagem aparece como slide 14.

> **Correção importante em relação ao slide 16b.** A medição de tokens apresentada na reunião
> (37,2 mil de entrada por episódio) estava inflada por contagem tripla. A medição corrigida é de
> **11,9 mil de entrada e 1,3 mil de saída** por episódio. Todo o orçamento deste documento usa a
> medição corrigida. A conta e o motivo estão no Anexo A.

---

## 1. O que a triagem é, e por que ela existe

A triagem **não é um experimento**. É o passo anterior aos experimentos definitivos, e existe para
responder duas perguntas de decisão. Os dados dela são descartáveis; o que entra no paper é o
**veredito** e a justificativa dele.

**Pergunta 1, lado aberto: qual dos 4 modelos abertos vamos usar?**
A resposta não pode ser um chute de tamanho. Três dos quatro ambientes exigem chamada de função,
protocolo multiagente e trajetórias de vários turnos. Abaixo de certo nível de capacidade o modelo
simplesmente não executa a tarefa, e aí o ASR fica baixo porque ele não fez nada, nem o ataque nem
a viagem. Isso cai no quadrante `safe_but_useless` e o experimento passaria a medir incompetência
básica em vez de robustez adversarial. É uma falha de validade de construto, e a triagem existe
para localizar esse piso empiricamente antes de gastar as milhares de execuções definitivas.

**Pergunta 2, lado pago: o ganho de desempenho justifica o custo financeiro?**
Temos orçamento, mas isso não é razão para gastar. A triagem roda quatro degraus de preço da
OpenAI, do mais barato ao mais potente, sobre exatamente os mesmos casos, e mede se o degrau caro
produz uma conclusão diferente. Se não produzir, o definitivo pode rodar no degrau barato e a
economia é de uma ordem de grandeza. Com quatro degraus em vez de três dá também para separar
**escala** de **geração**, o que a Seção 2.2 explora.

**Por que um protocolo só para as duas.** A exigência da orientação é comparabilidade: os
experimentos precisam ser iguais nos dois lados. Por isso o desenho está **fixado no código**
(`PROTOCOL` em `scripts/run_screening_protocol.py`), não em flags de linha de comando. O operador
escolhe o modelo e o backend; ele não consegue, por acidente, dar a um candidato uma triagem mais
fácil que a de outro.

```
  ETAPA 0          ETAPA 1                   ETAPA 2                    ETAPA 3
  Instalar   ->    TRIAGEM T2           ->   Congelar a dupla      ->   EXPERIMENTOS
  as duas          8 modelos x 45 exec       (1 aberto + 1 pago)        DEFINITIVOS
  máquinas         360 execuções             com dados, não aposta      ~1200 a 1500 por modelo
                   ~US$ 2 no esperado
```

---

## 2. Os 8 modelos

### 2.1 Escada aberta: 4 candidatos (máquina do laboratório)

Hardware confirmado: **2× RTX 5000 Ada, 32 GB cada, 64 GB no total**, na máquina mais fraca. A
máquina mais forte tem RTX 5090, também 32 GB por placa. Como as duas máquinas têm o mesmo teto por
GPU, a escada abaixo roda nas duas sem alteração, o que é condição para os resultados serem
comparáveis entre elas.

| # | Modelo | Tag no Ollama | Parâmetros | VRAM em 4-bit | GPUs | Papel na escada |
|---|---|---|---|---|---|---|
| O1 | Qwen3 8B | `qwen3:8b` | 8 B | ~6 GB | 1 | **controle de piso.** Entra para mostrar como é um modelo abaixo do limiar, não para ser escolhido. |
| O2 | Qwen3 14B | `qwen3:14b` | 14 B | ~10 GB | 1 | degrau intermediário. Se ele passar, a escolha desce e o contraste de escala aumenta. |
| O3 | Qwen3 32B | `qwen3:32b` | 32 B | ~20 GB | 1 | **aposta a priori.** Cabe folgado em uma única placa, tool calling maduro. |
| O4 | Llama 3.3 70B | `llama3.3:70b` | 70 B | ~43 GB | 2 (tensor parallel) | **teto.** Responde se o ganho de escala compensa o dobro de VRAM e o tempo de GPU. |

**Por que esta escada e não outra.** Os três primeiros degraus são da mesma família, o que isola o
efeito de escala: se o 14B passa e o 8B não, a diferença é tamanho, não família. O quarto degrau
troca de família de propósito, porque a pergunta dele é diferente: não é "quanto tamanho preciso",
é "existe teto acima do 32B que valha o custo de infraestrutura". Llama 3.3 70B é o 70B aberto com
tool calling mais maduro e já tem scripts de lote no repositório (`scripts/llama-3.1:70b/`).

**Confusão declarada:** como O4 muda família junto com tamanho, uma eventual vantagem dele não pode
ser atribuída só à escala. Isso é aceitável porque a triagem é um passo de **seleção**, não um
resultado reportado. Se você quiser uma escada de escala pura de ponta a ponta, troque para
Qwen2.5 nos quatro degraus (`qwen2.5:7b`, `qwen2.5:14b`, `qwen2.5:32b`, `qwen2.5:72b`), que existe
inteira na mesma família. O custo é usar uma geração anterior.

**Regra de ouro da quantização:** rode a triagem **no mesmo build quantizado que vai usar de
verdade** (Q4_K_M no Ollama, AWQ ou GPTQ de 4 bits no vLLM). Triar o modelo cheio e rodar o
quantizado invalida a triagem, porque a quantização pode derrubar o modelo abaixo do piso. Evite Q2
e Q3, que degradam demais.

### 2.2 Escada paga: 4 degraus de preço (notebook, API do laboratório)

Custo por execução calculado sobre a medição corrigida de 11.930 tokens de entrada e 1.333 de saída
por episódio (Anexo A).

| # | Modelo | US$ por 1M (in · out) | US$ por execução | Papel na escada |
|---|---|---|---|---|
| P1 | `gpt-5-nano` | 0,05 · 0,40 | 0,0011 | **piso de preço** da plataforma |
| P2 | `gpt-5-mini` | 0,25 · 2,00 | 0,0056 | degrau do meio, geração atual |
| P3 | `gpt-4.1-mini` | 0,40 · 1,60 | 0,0069 | degrau do meio, **geração anterior**, custo quase idêntico ao P2 |
| P4 | `gpt-5` | 1,25 · 10,00 | 0,0282 | **fronteira**, 25x o P1 |

**Por que estes quatro.** Os quatro degraus respondem duas perguntas de uma vez, e é isso que
justifica gastar o quarto degrau em vez de ficar em três:

1. **Escada de escala com geração fixa: P1 → P2 → P4.** Nano, mini e completo da mesma família
   GPT-5. Como a geração não muda ao longo dela, uma diferença nesse eixo é capacidade, e não
   modernidade. Essa é a escada que responde literalmente "vale a pena pagar mais".
2. **Controle de geração a custo praticamente igual: P2 contra P3.** `gpt-5-mini` custa
   US$ 0,0056 por execução e `gpt-4.1-mini` custa US$ 0,0069, ou seja, a mesma faixa. Rodando os
   dois sobre os mesmos casos, a comparação vira "pelo mesmo dólar, a geração nova entrega mais?".
   É a única célula da tabela em que preço está controlado e geração varia.

E há um resultado embutido na própria tabela de preços que vale mostrar na reunião: **`gpt-5`
custa menos por execução que `gpt-4.1`** (US$ 0,0282 contra US$ 0,0345), porque a entrada do
`gpt-5` é mais barata e 90% do custo aqui é entrada. A fronteira atual não é o degrau mais caro da
plataforma, e isso muda a pergunta "compensa pagar mais" antes mesmo de rodar qualquer episódio.

**O que ficou de fora, e o que custaria trocar.** Se a orientação quiser a linha literalmente mais
cara da plataforma no lugar do P3, a troca é de uma palavra no script, e os custos por execução
são: `gpt-4.1` US$ 0,0345, `gpt-4o` US$ 0,0432, `o4-mini` US$ 0,0190. Trocar P3 por `gpt-4o`
levaria a projeção conservadora de US$ 5,26 para US$ 8,52, ou seja, estouraria os US$ 6 e exigiria
cair para cerca de 30 execuções por modelo. O julgamento aqui é que **20 casos pareados valem mais
que uma linha de preço mais alta**, porque é o pareamento que dá poder ao teste.

**Três dos quatro são modelos de raciocínio, e isso precisa de controle.** A família GPT-5 gasta
tokens de raciocínio, cobrados como saída. Deixados no padrão do provedor, esses tokens variam de
execução para execução, o custo por episódio deixa de ser comparável entre modelos, e o orçamento
deixa de ser previsível. Por isso a triagem **fixa o esforço de raciocínio** em `minimal`:

```bash
--model-extra-args '{"reasoning_effort": "minimal"}'
```

Isso é controle experimental, não economia: um fator que varia sem ser medido é um confundidor. Se
quisermos depois medir o efeito do raciocínio, ele passa a ser um fator declarado do desenho, subido
para `low` ou `medium` **em todos** os modelos de raciocínio, com o orçamento refeito. O parâmetro
só vai para os modelos de raciocínio, porque a API o rejeita nos modelos da família 4.1.

**Dois detalhes de infraestrutura que descobri ao preparar isto** e que teriam derrubado a triagem
na primeira execução:

- **O autogen 0.5.6 não conhece a família GPT-5.** Ele carrega uma tabela fixa de modelos que para
  na geração 4.1/o4, e levanta `model_info is required when model name is not a valid OpenAI model`
  já na construção do cliente. O `run_experiments.py` agora detecta um nome desconhecido e monta o
  `model_info` sozinho, avisando no log. Sem isso, nenhum `gpt-5*` roda neste repositório.
- **Chaves não reconhecidas são descartadas em silêncio.** O autogen filtra os create-args por uma
  lista permitida e ignora o resto sem erro, então um `--model-extra-args` com erro de digitação
  não falha: ele simplesmente não faz nada. `reasoning_effort` e `max_completion_tokens` estão na
  lista permitida e funcionam.

Os preços são de tabela e vivem em `DEFAULT_PRICES` dentro de `scripts/analyze_cost.py`.
**Confirme na página de preços antes de rodar.** Se mudaram, corrija ali ou passe `--prices-json`;
nada mais no pipeline precisa mudar.

---

## 3. O protocolo T2

### 3.1 Os cinco blocos, 45 execuções por modelo

Cada bloco é um espelho reduzido de um dos experimentos do desenho definitivo. Nenhum experimento
ficou de fora: o que varia entre triagem e definitivo é só o número de execuções.

| Bloco | Corresponde a | Desenho | Execuções | O que ele mede na triagem |
|---|---|---|---|---|
| **L** | Tabela principal de ASR (largura) | 4 ambientes × 5 casos × 1 rep | **20** | competência (`utility_rate`) e ASR em todos os ambientes |
| **A** | Experimento 1 (repetição) | `travel_planning`, caso 0, 4 reps | **4** | variabilidade entre execuções do mesmo caso |
| **B1** | Experimento 3 (paráfrase benigna) | caso 0, 5 variantes da tarefa | **5** | a conclusão depende da redação do pedido legítimo? |
| **B2** | Experimento 3b (paráfrase adversarial) | casos 0 e 3, 4 variantes do ataque | **8** | a conclusão depende da redação do ataque? |
| **F** | Experimento 2 (fatorial 2²) | caso 0, Defesa{off,on} × Perturbação{none,weather_first}, 2 reps | **8** | o modelo responde aos prompts de defesa? |
| | | **Total por modelo** | **45** | |

**8 modelos × 45 execuções = 360 execuções no total.**

**Sobre o bloco A ter só 4 execuções.** Lido sozinho, 4 seria um número indefensável. Ele não é
lido sozinho. Quatro blocos colocam execuções na **mesma condição de referência**, que é
`travel_planning`, caso 0, defesa desligada, sem perturbação, tarefa original e ataque original:

| Origem | Execuções |
|---|---|
| bloco A | 4 |
| bloco B1, variante `base` (guarda a tarefa original literal) | 1 |
| bloco B2, variante `base` do caso 0 (guarda o `Harmful_Behavior` original literal) | 1 |
| bloco F, célula (defesa off, perturbação none), 2 reps | 2 |
| **Total de execuções idênticas** | **8** |

O `scripts/analyze_screening_protocol.py` **junta as oito** para a leitura de repetibilidade, em vez
de olhar só o bloco A. E o teste que ele usa para reconhecer a condição é sobre os campos salvos, e
não sobre o nome do bloco, então continua correto se o desenho mudar.

As execuções economizadas foram para o bloco L de propósito: **é o bloco L que carrega a comparação
pareada entre modelos**, ou seja, é ele que responde a pergunta da orientadora sobre o modelo caro.
Trocar 5 execuções de repetição por 4 casos pareados a mais é a troca certa aqui.

### 3.2 O que é fixo e o que varia

**Fixo em todos os 8 modelos:** os blocos, os casos, os papéis adversários, a semente (12345), os
datasets de paráfrase, o critério de sucesso do ataque (avaliador determinístico por palavra-chave),
a ordem de execução e, nos modelos de raciocínio, o esforço de raciocínio (`minimal`).
**Varia:** só o modelo e o backend.

Isso é o que torna a comparação **pareada**. Como os mesmos casos rodam em todos os modelos, a
comparação entre dois deles usa o **teste de McNemar** sobre os casos discordantes, e não duas
proporções independentes. McNemar exige menos amostra para o mesmo poder, o que é o que salva uma
triagem de 45 execuções de ser inútil.

### 3.3 Os casos exatos

A seleção é **determinística e estratificada**: o script percorre em rodízio os `Target` distintos
de cada ambiente, um caso por alvo por passada. O motivo é que o `BAD-ACTS.csv` vem ordenado por
alvo, então pegar "os 5 primeiros" leria a competência por um único canal de ataque. Os ids
resultantes são estes, e são os mesmos para todos os 8 modelos:

| Ambiente | Agente adversário | Casos (`--id`) | Alvos cobertos |
|---|---|---|---|
| `travel_planning` | PLANNER_AGENT | 0, 1, 22, 23, 30 | MESSAGING, MESSAGING, TICKETING, TICKETING, WEATHER |
| `financial_article_writing` | CHIEF_EDITOR | 0, 1, 5, 6, 10 | CHIEF_EDITOR/EDITOR ×2, IMAGE_GENERATOR ×2, WRITER |
| `code_generation` | CEO | 0, 1, 15, 18, 53 | PROGRAMMER ×2, BROWSER, FILES, EXECUTER |
| `multi_agent_debate` | agent_0 | 0, 1, 2, 8, 9 | ANSWER ×3, CONTAINS ×2 |

Lembre que `--id` é **índice posicional dentro da fatia do ambiente**, não o rótulo da linha do CSV.

### 3.4 Por que 45, e não 25 ou 200

O número de execuções é o único parâmetro que a triagem podia escolher livremente, e ele saiu de
uma restrição dura e de uma restrição de leitura.

**A restrição dura é o orçamento.** Com US$ 6 de teto e a escada de quatro degraus, o custo
esperado é `45 × (0,0011 + 0,0056 + 0,0069 + 0,0282) = US$ 1,89`. A projeção conservadora aplica 2x
em entrada e saída (porque a medição do piloto cobre só `travel_planning` com um modelo pequeno, e
outros ambientes ou modelos maiores podem produzir trajetórias mais longas) e **outro 2x só na
saída dos modelos de raciocínio**, porque os tokens de raciocínio são cobrados como saída e não
existem no perfil do piloto. Isso dá **US$ 5,26**, que cabe nos US$ 6 com margem.

A margem não é decorativa. A tabela abaixo mostra o que cada N custaria:

| Execuções por modelo | Esperado | Conservador |
|---|---|---|
| 40 | US$ 1,68 | US$ 4,68 |
| **45** | **US$ 1,89** | **US$ 5,26** |
| 50 | US$ 2,10 | US$ 5,85 |

50 ainda caberia no papel, mas com US$ 0,15 de margem sobre um cenário conservador cujo fator de
raciocínio é uma estimativa, não uma medição. 45 é o maior N que sobrevive a um erro nessa
estimativa. Se o `gpt-5-nano`, que roda primeiro e custa centavos, mostrar que os tokens de
raciocínio inflam menos que o previsto, subir para 50 ou 60 é trocar um número no script e refazer
a sweep dos pagos.

**A restrição de leitura é o que 45 execuções conseguem dizer.** Com 20 casos pareados no bloco L,
o McNemar entre dois degraus só detecta diferenças grandes, e é isso mesmo que se quer: a decisão
"vale a pena pagar 25x" só deve mudar se a diferença for grande. E com as 8 execuções da condição de
referência (Seção 3.1), o intervalo de Wilson fica largo, o que já basta para o uso da triagem, que
é ver se o mesmo caso troca de quadrante entre execuções.

**O que 45 execuções não conseguem dizer está na Seção 7.** Elas não fecham nenhuma conclusão
científica, e o documento é explícito nisso em três lugares porque essa é a confusão fácil de fazer.

---

## 4. Orçamento e as travas que o protegem

### 4.1 A conta

Custo por execução calculado sobre a medição corrigida de **11.930 tokens de entrada e 1.333 de
saída** por episódio (Anexo A):

| Modelo | US$/execução | 45 execuções | Conservador | Teto configurado no script |
|---|---|---|---|---|
| `gpt-5-nano` | 0,0011 | 0,05 | 0,15 | **0,20** |
| `gpt-5-mini` | 0,0056 | 0,25 | 0,75 | **0,80** |
| `gpt-4.1-mini` | 0,0069 | 0,31 | 0,62 | **0,70** |
| `gpt-5` | 0,0282 | 1,27 | 3,74 | **3,90** |
| **Total** | | **1,89** | **5,26** | **5,60** (teto global 6,00) |

O fator conservador é 2x em entrada e saída para todos, mais outro 2x só na saída dos três modelos
de raciocínio. É por isso que a coluna conservadora do `gpt-4.1-mini` é 2x a esperada, enquanto a do
`gpt-5` é quase 3x.

Os modelos abertos não entram nesta conta: rodam local e custam **tempo de GPU**, não dinheiro. A
triagem mede esse tempo (segundos por execução, gravados no manifesto) e é justamente daí que sai a
estimativa de quanto vai demorar o definitivo.

### 4.2 As três travas

1. **Ensaio a seco obrigatório.** Todo script aceita `--dry-run`, que imprime o plano e a projeção
   de custo sem executar nada e sem gastar um centavo.
2. **Medição real após cada bloco.** `scripts/run_screening_protocol.py --budget-usd X` relê os
   tokens dos arquivos de resultado depois de cada bloco e aborta na hora se passar do teto. A
   contagem vem dos arquivos, não de estimativa.
3. **Ordem do mais barato para o mais caro.** Quando a sweep chega no `gpt-5`, você já mediu o
   custo real do protocolo inteiro nos três degraus anteriores. A projeção do último degrau deixa de
   ser previsão e vira aritmética. Isso é o que domestica a incógnita dos tokens de raciocínio: o
   `gpt-5-nano` mede o inflamento por menos de um centavo, e o número medido nele corrige a projeção
   do `gpt-5` antes de gastar nele.
4. **Esforço de raciocínio fixado.** Sem `reasoning_effort` pinado, o custo de um modelo GPT-5 é uma
   variável aleatória, e nenhum teto orçamentário sobrevive a isso. O orquestrador **avisa** quando
   você aponta um modelo de raciocínio sem passar `--model-extra-args`.

Se um teto estourar, o script para e **avisa que o protocolo daquele modelo ficou incompleto**. Um
modelo com protocolo incompleto não pode entrar na tabela comparativa como se estivesse completo, e
o analisador marca isso com o veredito `INCOMPLETO`.

Sobre a contabilidade dos tokens de raciocínio: a API da OpenAI inclui os tokens de raciocínio no
`completion_tokens` (o campo `reasoning_tokens` é um detalhamento dele, não um adicional), e é o
`completion_tokens` que o autogen grava. Portanto **a medição de custo já contabiliza o raciocínio**
mesmo sem enxergá-lo separadamente. O que não dá para fazer é atribuir a parcela: o relatório mostra
o total de saída, não quanto dele foi raciocínio.

---

## 5. Como executar

### 5.0 Passo zero, em qualquer máquina: validar com uma execução

Antes de disparar qualquer sweep, prove que o encanamento funciona com aquele modelo específico.
Uma execução do `gpt-5-nano` custa menos de meio centavo e detecta na hora se o modelo não está
liberado na conta, se a chave está errada, ou se o nome do modelo mudou.

```bash
export OPENAI_API_KEY="sk-..."
python run_experiments.py --model-provider openai --model-client gpt-5-nano \
  --model-extra-args '{"reasoning_effort": "minimal"}' \
  --environment travel_planning --adversarial-agent PLANNER_AGENT --id 0 \
  --seed 12345 --run-label smoke_nano

python scripts/analyze_cost.py --results 'results/*smoke_nano*.json'
```

Espere ver no log a linha `Note: autogen has no built-in model_info for 'gpt-5-nano'`. Ela é
esperada e é justamente o mecanismo que faz a família GPT-5 rodar nesta versão do autogen
(Seção 2.2).

**Compare o `out/ep` desta execução com os 1.333 tokens do perfil do piloto.** É a medição que
diz o quanto o raciocínio infla a saída, e é ela que valida ou derruba o fator conservador de 2x
usado no orçamento. Se vier muito acima, corrija o teto do `gpt-5` antes de chegar nele.

Na máquina do laboratório, o equivalente é a mesma linha com
`--model-provider ollama --model-client qwen3:8b` e sem `--model-extra-args`.

### 5.1 Notebook: os 4 modelos pagos

```bash
cd ~/Documents/USP/mestrado/benchmarks/BAD-ACTS
source .venv_badacts/bin/activate
export OPENAI_API_KEY="sk-..."          # a chave do laboratório

# 1. ensaio a seco: mostra o plano e a projeção de custo, não gasta nada
bash scripts/triagem/run_triagem_openai.sh --dry-run

# 2. valendo. 180 execuções, algo entre 1 e 3 horas, US$ 2 a 5
bash scripts/triagem/run_triagem_openai.sh
```

O script roda os quatro modelos em sequência (gpt-5-nano, gpt-5-mini, gpt-4.1-mini, gpt-5), cada um
com seu teto, passa `reasoning_effort=minimal` só para os de raciocínio, grava um log por modelo em
`evaluation_results/screening/logs/` e, no fim, imprime o custo total medido com uma verificação
contra o teto global de US$ 6.

Para mudar o esforço de raciocínio de todos de uma vez:
`REASONING=low bash scripts/triagem/run_triagem_openai.sh` (e refaça o orçamento antes).

Se cair no meio, repita o mesmo comando: `--resume` está ligado e pula os blocos cujo manifesto já
existe. O resume é **por bloco**, então no pior caso você repete um bloco, nunca a triagem inteira.

### 5.2 Máquina com GPU, por SSH: os 4 modelos abertos

**Preparação, uma vez só.** O passo a passo completo de instalação está em
`docs/02-experimentos/GUIA_TRIAGEM_E_EXECUCAO.md`, Seção 1. O resumo:

```bash
git clone <repo> && cd BAD-ACTS
python3 -m venv .venv_badacts && source .venv_badacts/bin/activate
pip install --upgrade pip && pip install -r requirements.txt
python -c "import autogen_agentchat, autogen_core, autogen_ext; print('autogen ok')"

docker ps                 # obrigatório: code_generation e financial_article_writing
                          # importam DockerCommandLineCodeExecutor no topo do arquivo
nvidia-smi                # confirme as duas placas e a VRAM

curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull qwen3:8b && ollama pull qwen3:14b && ollama pull qwen3:32b && ollama pull llama3.3:70b
ollama list               # confirme as tags, porque nomes e versões mudam
```

**Rodar.** Como o acesso é só por linha de comando e a triagem leva horas, use `tmux`, ou a queda da
conexão mata a sweep no meio:

```bash
tmux new -s triagem
cd ~/BAD-ACTS && source .venv_badacts/bin/activate

bash scripts/triagem/run_triagem_local.sh --dry-run    # sempre primeiro
bash scripts/triagem/run_triagem_local.sh

# Ctrl-b d para desanexar. Depois: tmux attach -t triagem
```

O script confere o ambiente antes de começar (GPUs, autogen, docker, ollama), roda os quatro
candidatos em sequência e, no fim, imprime o veredito da escada aberta.

**Sobre o 70B e as duas placas.** Llama 3.3 70B em 4 bits ocupa cerca de 43 GB e **não cabe em uma
única RTX 5000 Ada de 32 GB**. Ele precisa das duas. No Ollama o particionamento é automático. Se
migrar para vLLM, sirva explicitamente:

```bash
vllm serve <modelo-quantizado-70B> --port 8000 --tensor-parallel-size 2
PROVIDER=vllm BASE_URL=http://localhost:8000/v1 bash scripts/triagem/run_triagem_local.sh
```

**Sobre o tempo.** É a incógnita da triagem, e medi-la é um dos produtos dela. Ordem de grandeza:
um episódio no piloto (API, notebook sem GPU) levou cerca de 25 segundos. Local, espere de 1 a 4
minutos por episódio conforme o tamanho do modelo. Com 4 candidatos × 45 execuções = 180 episódios,
isso dá algo entre 3 e 12 horas para a escada inteira, e o 70B é quem domina a conta. Os números reais saem na coluna `s/exec` do relatório. Se der tempo demais no Ollama,
migre para vLLM antes do definitivo: ele faz batelada na mesma GPU.

**Um candidato que quebra não interrompe a escada.** Quebrar é o resultado dele. As execuções
quebradas são contadas e pesam contra o candidato, porque não conseguir terminar um episódio é
falha de competência, não dado faltante.

### 5.3 Juntar as duas metades e ler o relatório

Traga os resultados do laboratório para o notebook. Os caminhos gravados nos manifestos são
relativos à raiz do repositório, então a cópia funciona sem ajuste:

```bash
rsync -avz USUARIO@MAQUINA-LAB:~/BAD-ACTS/results/ ./results/
rsync -avz USUARIO@MAQUINA-LAB:~/BAD-ACTS/evaluation_results/ ./evaluation_results/
```

E rode o relatório único, com os 8 modelos:

```bash
python scripts/analyze_screening_protocol.py \
  --screening-dir evaluation_results/screening \
  --utility-threshold 0.70 \
  --open-ladder qwen3-8b,qwen3-14b,qwen3-32b,llama33-70b \
  --paid-ladder gpt5nano,gpt5mini,gpt41mini,gpt5 \
  --out-json evaluation_results/screening/relatorio_triagem.json \
  --out-csv  evaluation_results/screening/relatorio_triagem.csv
```

Sobre a ordem do `--paid-ladder`: ela é por **custo crescente**, e a escada de custo-benefício
compara degraus **adjacentes**. Com `gpt5nano,gpt5mini,gpt41mini,gpt5` você recebe três
comparações: nano→mini (escala), gpt-5-mini→gpt-4.1-mini (geração, a custo quase igual) e
gpt-4.1-mini→gpt-5 (o salto para a fronteira). Para ler a escada de escala pura da família GPT-5,
rode uma segunda vez com `--paid-ladder gpt5nano,gpt5mini,gpt5`.

As duas ordens importam: `--open-ladder` do menor para o maior (a regra de decisão é "o menor
competente") e `--paid-ladder` do mais barato para o mais caro (a escada de custo-benefício compara
degraus adjacentes). Sem elas o script ordena por diretório e avisa que a recomendação não
significa nada.

---

## 6. Como a decisão é tomada

O relatório imprime cinco seções. As regras abaixo estão implementadas, não são interpretação livre.

### 6.1 Modelo aberto: piso de utilidade, depois o menor

1. **O piso é `utility_rate ≥ 70%`** nos três ambientes com ferramenta. O `multi_agent_debate` é
   reportado mas **não decide**, porque é texto puro e o piso ali é muito mais baixo.
2. **Passar significa passar em todos os três.** Ambiente sem dado não conta como aprovação: se o
   candidato quebrou no `code_generation`, não há evidência de que ele faça `code_generation`, e o
   veredito vira `INCOMPLETO`, não `COMPETENTE`.
3. **Execuções que quebram contam contra o candidato.**
4. **Entre os competentes, fica o menor.** Menor modelo competente significa maior contraste de
   escala contra o modelo pago, que é o eixo da pergunta do paper.

O bloco L roda com a **defesa desligada**, que é a condição padrão do BAD-ACTS, para o ASR ficar
comparável com o benchmark publicado. Isso torna a leitura de competência **conservadora**: um
modelo que mantém a utilidade mesmo sob ataque é competente sem discussão. Quando um candidato falha
o piso, olhe as células com defesa ligada do bloco F para separar "incompetente" de "capaz, mas
descarrilado pelo ataque".

### 6.2 Modelo pago: McNemar pareado contra o preço

Para cada par de degraus adjacentes, o relatório imprime o múltiplo de preço, o ASR e a utilidade
de cada um, quantos casos discordaram, e o p-valor do McNemar exato. A leitura automática é:

- **p > 0,05 nos dois desfechos:** a triagem não detectou diferença. O gasto extra não se justifica
  **por esta evidência**.
- **p ≤ 0,05:** o degrau caro muda a conclusão, e aí a diferença é grande de verdade, porque com 20
  casos pareados só o que é grande aparece.

A assimetria acima é deliberada e precisa ser dita em voz alta na reunião: **"não detectamos
diferença" não é "são equivalentes"**. O uso legítimo da triagem é o inverso, ou seja, se o degrau
caro já se separa com 20 casos, a diferença é substancial. Se não se separa, a decisão de subir de
degrau passa a depender de argumento de representatividade (usar um modelo de fronteira porque é ele
que as pessoas usam), e não de desempenho medido.

A tabela de custo fecha a decisão traduzindo o custo por execução medido em **quanto custaria o
definitivo** naquele modelo, nos dois tiers do `PLANO_EXPERIMENTAL.md` (núcleo de 420 e estendido de
1400 execuções). Com a medição corrigida:

| Modelo | Núcleo (420) | Estendido (1400) |
|---|---|---|
| `gpt-5-nano` | US$ 0,47 | US$ 1,58 |
| `gpt-5-mini` | US$ 2,37 | US$ 7,91 |
| `gpt-4.1-mini` | US$ 2,90 | US$ 9,67 |
| `gpt-5` | US$ 11,86 | US$ 39,54 |

Ou seja, **nenhum dos quatro degraus é proibitivo nem no tier estendido**. Isso é importante dizer
com clareza na reunião, porque redefine a pergunta: não é "podemos pagar o modelo caro", é "o modelo
caro entrega algo diferente". A resposta vem do McNemar, não do orçamento. Os valores da tabela são
o perfil de tokens do piloto; para os modelos de raciocínio a triagem vai medir o número real e o
relatório recalcula estas colunas a partir dele.

### 6.3 E se ninguém passar no piso

Esse cenário é **publicável, não um fracasso**. Significa que os ambientes com ferramenta do
BAD-ACTS estão acima da capacidade dos modelos abertos daquela banda. Nesse caso:

- reporte a comparação pela dimensão de **utilidade**, deixando explícito que ASR baixo ali é
  incompetência e não robustez;
- use o `multi_agent_debate`, que é texto puro, como arena de comparação justa;
- e considere que o próprio confundidor de competência vira um achado do trabalho, que é
  exatamente o mecanismo que o experimento B2 já expôs por outro caminho (três das quatro rodadas
  "seguras" eram colapso do episódio).

---

## 7. O que a triagem não responde

Está aqui para ser citado literalmente se a pergunta vier na reunião.

1. **Nada de segurança.** 45 execuções por modelo dão intervalos largos por construção. Nenhum
   número da triagem entra no paper como resultado. O que entra é o veredito de escolha e o custo
   medido.
2. **Um caso por bloco profundo.** Os blocos A, B1 e F rodam sobre o caso 0 de `travel_planning`.
   Um caso não representa o benchmark; ele representa a condição de referência contra a qual as
   outras células são comparadas.
3. **A utilidade é um proxy heurístico**, não rótulo humano (`evaluation/evaluation_functions.py`).
   Como o piso de competência inteiro depende dela, essa é a limitação mais séria da triagem. A
   validação contra rótulo humano é o passo 4 do cronograma
   (`scripts/create_utility_labeling_sample.py` e `scripts/evaluate_utility_proxy_agreement.py`), e
   até ela existir o piso é declarado como proxy.
4. **A semente não torna o modelo determinístico.** `--seed` semeia só a aleatoriedade do ambiente.
   É por isso que o bloco A existe.
5. **O bloco L usa um papel adversário por ambiente**, não todos. Cobre os alvos, não os atacantes.
6. **O degrau O4 mistura escala e família** (Seção 2.1).
7. **O esforço de raciocínio está fixado em `minimal`.** Isso controla o confundidor de custo, mas
   também significa que os modelos GPT-5 rodam **abaixo** da capacidade que atingiriam no padrão do
   provedor. A triagem responde "o degrau caro compensa com raciocínio mínimo", e não "o degrau caro
   compensa no seu melhor". Se a comparação final for entre um aberto e um GPT-5, o esforço de
   raciocínio deve entrar no definitivo como fator declarado do desenho.
8. **O relatório não separa tokens de raciocínio dos de resposta.** Eles vêm somados no
   `completion_tokens`, então o custo está certo, mas a atribuição não é possível com o que o
   autogen grava.

---

## 8. Referência de arquivos

### Código novo desta triagem

| Arquivo | O que faz |
|---|---|
| `scripts/run_screening_protocol.py` | Orquestra o protocolo T2 (5 blocos, 45 execuções) para **um** modelo. Contém a constante `PROTOCOL`, que é o desenho, e a projeção de custo ciente de modelos de raciocínio. |
| `scripts/analyze_screening_protocol.py` | Relatório dos 8 modelos: competência, estabilidade (juntando as 8 execuções da condição de referência), custo, escada de custo-benefício com McNemar, decisão. |
| `scripts/analyze_cost.py` | Contabilidade de tokens e dólares a partir dos arquivos de resultado. Trava de orçamento (`--budget-usd`, sai com código 3). |
| `scripts/triagem/run_triagem_openai.sh` | Roda os 4 pagos no notebook, com teto por modelo, log por modelo e `reasoning_effort` só nos modelos de raciocínio. |
| `scripts/triagem/run_triagem_local.sh` | Roda os 4 abertos na máquina com GPU, checando o ambiente antes. |

### Código existente que foi ajustado

| Arquivo | Ajuste |
|---|---|
| `run_experiments.py` | Duas mudanças que a família GPT-5 exigiu. (1) Quando o nome do modelo não está na tabela interna do autogen 0.5.6, o `model_info` é montado automaticamente, com aviso no log. Sem isso nenhum `gpt-5*` roda. (2) Nova opção `--model-extra-args`, um objeto JSON de create-args repassados ao cliente, que é como se fixa `reasoning_effort` e `max_completion_tokens`. O valor usado fica gravado em cada datapoint. |
| `scripts/run_screening.py` | Nova opção `--case-selection stratified` (padrão), que faz rodízio pelos `Target` distintos em vez de pegar os N primeiros, que caíam todos no mesmo alvo. Repassa `--model-extra-args`. |
| `scripts/run_robustness_experiments.py` | O manifesto passou a gravar `duration_seconds` (para estimar tempo de GPU) e a identidade do modelo/ambiente, para que os analisadores não precisem abrir cada resultado só para saber quem produziu a sweep. Repassa `--model-extra-args`. |

### Onde os dados caem

```
evaluation_results/screening/
  <tag>/                                    # um diretório por modelo
    manifest_L_breadth.jsonl
    manifest_A_repetition.jsonl
    manifest_B1_benign_paraphrase.jsonl
    manifest_B2_adversarial_paraphrase.jsonl
    manifest_F_factorial_def0_nosafe.jsonl
    manifest_F_factorial_def1_safe.jsonl
    protocol_summary.json                   # versão do protocolo, tempo total, códigos de retorno
  logs/<tag>.log
  relatorio_triagem.json | .csv
results/                                    # os episódios em si, um JSON por execução
```

Os manifestos são o que amarra tudo: cada um lista exatamente os arquivos produzidos por um bloco,
o que mantém a análise isolada em vez de varrer o `results/` inteiro. Guarde-os junto dos
resultados. Nem `results/` nem `evaluation_results/` são versionados.

---

## Anexo A: a correção da medição de tokens

O slide 16b da apresentação reporta 37,2 mil tokens de entrada e 3,7 mil de saída por episódio.
Esse número está inflado por cerca de 3x, e a correção importa porque todo o orçamento depende dela.

**Onde os tokens ficam.** `run_experiments.py` salva `team.save_state()` no campo `team_states`.
Dentro dele há duas estruturas que contêm `models_usage`:

- `agent_states.SelectorGroupChatManager.message_thread`, que é a **thread ordenada** do episódio.
  Cada mensagem produzida por uma chamada de modelo carrega o `prompt_tokens` e o
  `completion_tokens` daquela chamada. Somar essa thread é o registro completo e sem duplicata do
  que foi cobrado.
- `agent_states.<AGENTE>.message_buffer`, que guarda **cópias** de mensagens da thread que ainda
  estavam na fila de entrega de cada agente quando o estado foi salvo. Elas não são chamadas
  adicionais ao modelo.

**A conta.** Sobre os 158 episódios do piloto que rodaram no `gpt-4o-mini` (o manifesto tem 163 no
total, cinco deles em `llama3.1:8b`):

| Fonte somada | Entrada/episódio | Saída/episódio |
|---|---|---|
| só `message_thread` (correto) | **11.930** | **1.333** |
| só os `message_buffer` | 24.903 | 2.349 |
| os dois somados (o que o slide reportou) | 36.833 | 3.682 |

**A consequência prática é boa.** O piloto inteiro custou **US$ 0,41**, e não os US$ 1,22 que a
contagem inflada implicaria. E o tier estendido do definitivo no `gpt-4.1` sai por cerca de
US$ 48, e não US$ 145. O custo continua não sendo o gargalo, mas agora o número é auditável, e
`scripts/analyze_cost.py` recalcula tudo a partir dos arquivos a qualquer momento.

**Um ajuste a mais no discurso.** O slide sugere o cache de prompt da API como alavanca de economia,
porque 91% do custo é entrada. Isso não se aplica a esta carga: o cache automático da OpenAI só
incide em prompts a partir de cerca de 1024 tokens, e as chamadas aqui ficam quase todas abaixo
disso (a trajetória típica vai de 279 a 1854 tokens de contexto, crescendo turno a turno). O
mecanismo existe, mas não é a alavanca que o slide sugere.

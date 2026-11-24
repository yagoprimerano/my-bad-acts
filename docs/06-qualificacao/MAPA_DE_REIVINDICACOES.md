# Mapa de reivindicações da qualificação

Etapa 1 da auditoria pedida pelo autor em 23/11/2026, antes do sorteio dos guardados e antes de
começar a escrever a qualificação (inscrição em **31/05/2027**). Objetivo: listar cada afirmação
que o texto da qualificação vai fazer, com a evidência e a referência que a sustentam, para ver
onde há furo **antes** de construir mais coisas em cima.

**Reunião 8** (decidido pelo autor em 24/11/2026): não será de avanço do desenvolvimento (o sorteio
dos 336 guardados segue parado), e sim uma pausa para levar à orientadora o resultado desta auditoria:
o enquadramento, as decisões da Seção 5, os furos da Seção 4 e as perguntas do HarpIA (Seção 9).

As etapas seguintes da auditoria, na ordem combinada:

1. **este mapa** (e a proposta de pergunta de pesquisa e objetivos que reconcilia julho com hoje);
2. auditoria das referências que já existem (existe? diz o que citamos? onde saiu? revisada por pares?);
3. teste adversarial da lacuna (buscar o trabalho que a derrubaria; pesquisas externas direcionadas);
4. revisão metodológica como a banca faria;
5. esqueleto da qualificação e rotina de consolidação mensal.

Status usados na tabela da Seção 3:

| Status | Significa |
|---|---|
| **SUSTENTADA** | há evidência própria ou trecho conferido no original, e a afirmação está no tamanho certo |
| **PARCIAL** | a direção está certa, mas falta referência, número ou o recorte está largo demais |
| **NÃO CONFERIDA** | veio de relatório de pesquisa automática ou de memória; ninguém abriu o original |
| **SEM DADOS** | depende de algo que ainda não foi construído ou rodado |
| **FALSA COMO ESTÁ** | a frase, do jeito que está escrita hoje, é derrubada por um trabalho conhecido |

---

## 1. As duas histórias

Existem hoje dois textos que descrevem o mestrado, e eles não contam a mesma pesquisa.

**A monografia de julho/2026** (disciplina de Metodologia,
`~/Documents/USP/mestrado/metodologia/entrega-final/monografia_ppgsi_overleaf_clean/`, 37 páginas,
12 referências). Título: *Avaliação de métricas para ataques adversariais em sistemas com agentes
baseados em modelos de linguagem*. Questão: "como benchmarks e registros de trajetória podem ser
usados para avaliar conjuntamente segurança, robustez e utilidade de agentes baseados em LLMs sob
ataques adversariais?". Proposta: mapear benchmarks, selecionar alguns (AgentDojo, BAD-ACTS,
AgentLeak, SafeAgents/DHARMA, TAMAS se viável), instrumentar a trajetória (ferramentas, memória,
RAG, estado), propor matriz utilidade × segurança, cenário aplicado de MLOps. O BAD-ACTS aparece
como "alternativa promissora" caso o TAMAS não funcione.

**O trabalho real desde agosto/2026** (este repositório). Um só benchmark, o BAD-ACTS multiagente;
robustez tratada como objeto, com repetição, paráfrase da tarefa e do ataque, perturbação e fatorial
2² (blocos A, B1, B2, C, F), lida com o ferramental do Montgomery; triagem de 14 modelos com piso de
competência; auditoria do proxy de utilidade contra rótulo humano (κ 0,15); desenho de uma medida de
utilidade híbrida validada num conjunto guardado. O `NOVIDADE_E_POSICIONAMENTO.md` (agosto) põe como
contribuição principal o paradigma de controle estatístico (cartas de controle e fatorial) e, desde o
adendo de 21/10, a medida de utilidade como contribuição secundária.

O que da monografia de julho **continua valendo**, o que **muda** e o que **sai**:

| Item de julho | Destino | Por quê |
|---|---|---|
| Título "Avaliação de métricas para ataques adversariais..." | **continua** (ver Seção 2) | descreve o que foi feito melhor do que parece à primeira vista |
| Problema: avaliar segurança, robustez e utilidade juntos, sob ataque | **continua** | é o fio de tudo que foi feito |
| Mapeamento sistemático (protocolo, ACM DL, 20 extrações) | **continua como base dos relacionados**, a completar | extração preliminar, um só pesquisador, leituras integrais pendentes |
| Matriz utilidade × segurança | **continua**: virou o quadrante 2×2 | já implementado (`evaluate_utility_success` + `quadrant`) |
| Instrumentação da trajetória | **continua, menor**: diagnóstico heurístico | `trajectory_diagnostics.py`; não é contribuição central |
| Vários benchmarks (AgentDojo, AgentLeak, SafeAgents, TAMAS) | **sai como objeto empírico**, fica como trabalho relacionado | o trabalho virou profundidade num benchmark, não largura |
| Memória, RAG, MLOps, MITRE ATLAS | **sai** (no máximo, trabalho futuro) | nada disso foi feito |
| Robustez como uma das três dimensões | **sobe**: vira o eixo principal | é onde está a lacuna do Li et al. |
| HarpIA / projeto SP01 como contexto institucional | **HarpIA continua** (decidido em 24/11); SP01 a confirmar com a orientadora | é preciso entregar um artefato de contribuição ao HarpIA (Seção 5) |

Nada disso é grave: projeto de qualificação existe para mudar. Mas a banca vai ler o texto novo, e
ele tem de contar **uma** pesquisa, com pergunta, objetivos e contribuições que correspondam ao que
foi feito. Hoje esse texto não existe em lugar nenhum.

---

## 2. Proposta de pergunta de pesquisa e objetivos (rascunho para o autor aprovar)

### 2.1 O fio que une tudo: a validade das métricas

Lendo o que foi feito em sequência, todo achado forte até agora é do mesmo tipo: **uma métrica de
avaliação adversarial que, sozinha, leva a uma conclusão errada**.

- O ASR de uma execução muda quando se repete ou se reescreve o pedido (piloto B2: em 18,4% das
  comparações o quadrante discorda da execução base).
- O ASR baixo pode ser inércia, não defesa (`gpt-5-nano`: 0% de ASR com 2 chamadas de ferramenta em
  52 episódios).
- A queda do ASR sob paráfrase pode ser colapso da tarefa, não resistência (3 de 4 "seguranças" do B2
  eram `safe_but_useless`).
- O proxy de utilidade por regra simples superestima a utilidade (concorda com o humano em 40% dos
  "útil" na viagem; κ 0,15).

Isso casa com o título de julho, *Avaliação de métricas para ataques adversariais*, e dá à robustez e
à utilidade o mesmo papel: são as duas coisas que faltam ao ASR de execução única para que a conclusão
se sustente. Também casa com o ISQC, que trata a medida como um sistema de medição a validar (Seção
8.7, já usada no `MEDIDA_UTILIDADE_HIBRIDA.md` 7.5).

### 2.2 Pergunta proposta

> **As conclusões que um benchmark adversarial multiagente tira do ASR de uma execução se
> sustentam quando se mede também a utilidade sob ataque e se repete o experimento sob variações
> semanticamente equivalentes?**

Perguntas auxiliares, cada uma com o bloco de trabalho que a responde:

| # | Pergunta auxiliar | Responde com | Estado |
|---|---|---|---|
| QA1 | Quanto da variação do ASR e do quadrante é ruído do próprio modelo (repetição) e quanto vem de reescrever o pedido legítimo ou o ataque? | blocos A, B1, B2 (triagem e definitivo); `analyze_experiment_stats.py spc` e `noise` | piloto (gpt-4o-mini) e triagem (14 modelos, poucas réplicas); definitivo por rodar |
| QA2 | Como medir a utilidade sob ataque de modo que a medida concorde com o julgamento humano? | medida híbrida (código + juiz), lote 2 com o Pedro, conjunto guardado de 336 | desenho aprovado; nada construído |
| QA3 | Quando o ASR baixo é resistência e quando é incapacidade do time? | quadrante 2×2, piso de competência, triagem dos 14 | evidência forte num caso (`gpt-5-nano`); piso a refazer com a medida nova |
| QA4 | A defesa (aviso adversarial) e a perturbação da coordenação mudam o ASR, e interagem? | bloco F, fatorial 2² | piloto; definitivo por rodar |

### 2.3 Objetivos propostos

Geral: avaliar a validade das conclusões tiradas do ASR num benchmark adversarial multiagente
(BAD-ACTS), acrescentando medidas de utilidade sob ataque e de estabilidade sob repetição e
reformulação, com delineamento e leitura estatística apoiados no Montgomery.

Específicos:

1. caracterizar a variabilidade do ASR e do quadrante segurança × utilidade entre repetições e sob
   paráfrase da tarefa e do ataque (QA1);
2. construir e validar contra rótulo humano cego uma medida de utilidade sob ataque para o ambiente de
   viagem (QA2);
3. mostrar, com o quadrante e o piso de competência, quando um ASR baixo não indica resistência (QA3);
4. estimar efeitos principais e interação de defesa e perturbação num fatorial 2² (QA4);
5. aplicar o protocolo a dois modelos escolhidos pela triagem e discutir validade e custo.

### 2.4 Contribuições, no tamanho que a evidência permite hoje

- **C-principal:** um protocolo de avaliação que mede, junto com o ASR, a utilidade sob ataque e a
  estabilidade sob repetição e reformulação, e evidência de que o ASR de execução única leva a
  conclusões que mudam (QA1, QA3).
- **C-medida:** uma medida de utilidade sob ataque para tarefa aberta em linguagem natural, validada
  contra humano cego num conjunto guardado (QA2). O recorte exato depende da etapa 3 (ver C11 na
  Seção 3).
- **C-método:** a leitura da robustez com cartas de controle e fatorial, que era a contribuição
  principal em agosto. **Rebaixada para contribuição de método (decidido em 24/11; registro na Seção 8)**, porque é onde está a
  objeção mais séria ainda sem resposta (C15) e porque não tem dado definitivo. Se a etapa 3
  confirmar que ninguém fez e a objeção for respondida, ela volta a subir.

O que **não** está na pergunta: o efeito da escala do modelo (ver F6 na Seção 4).

---

## 3. O mapa: cada afirmação, sua evidência, sua referência

| # | Afirmação que a quali faria | Onde entra | Evidência / referência hoje | Status | O que falta |
|---|---|---|---|---|---|
| C1 | Benchmarks de segurança de agentes avaliam majoritariamente com uma execução por caso, sem repetição | introdução, relacionados | Li et al. (2026), Gap 4: "the corpus is dominated by one-shot action/outcome evaluation [...] very little repeated-perturbation testing" (conferido no PDF em 23/11) | **PARCIAL** | fonte única; contar nos 20 da revisão sistemática quantos repetem execuções e reportam variância |
| C2 | Robustez e confiabilidade (R10) não têm benchmark primário | introdução, lacuna | Li et al. (2026): R10 com 0 primários e 7 parciais, incluindo o próprio BAD-ACTS (conferido no PDF em 23/11). R10 inclui "inconsistent safety behavior [...] in semantically equivalent situations", que é o que B1/B2 medem | **PARCIAL** | Li et al. é preprint do arXiv, sem revisão por pares, corpus até mar/2026; precisa de apoio independente e de busca de abr a nov/2026 (etapa 3) |
| C3 | Rankings de benchmarks de segurança não concordam entre si | introdução (motivação) | Li et al. (2026): W de Kendall = 0,10, p = 0,94, sobre 11 modelos com dados completos (conferido em 23/11) | **SUSTENTADA** | citar com a ressalva dos 11 modelos e das células faltantes que o próprio artigo faz |
| C4 | Ninguém combinou adversarial × multiagente × robustez medida estatisticamente | lacuna | `NOVIDADE_E_POSICIONAMENTO.md` 3.3; os concorrentes (Princeton 2602.16666, 2605.10516, ReasonBench, 2605.28840) vêm de pesquisa automática de agosto | **NÃO CONFERIDA** | conferir que os quatro existem e dizem o que citamos (etapa 2); buscar de novo (etapa 3); o "trabalho da Frontiers (2026)" não tem referência completa |
| C5 | Ninguém aplicou cartas de controle e fatorial (Montgomery) à segurança de agentes | contribuição de método | mesma pesquisa de agosto; precedentes só em outros domínios (2310.01537, 2105.10707) | **NÃO CONFERIDA** | etapas 2 e 3; escrever sempre "não encontramos até <data>" |
| C6 | ASR baixo pode ser incapacidade, não resistência | resultado preliminar | própria: `gpt-5-nano`, 2 chamadas de ferramenta em 52 episódios, 0% de utilidade (`ESTADO_DA_TRIAGEM.md` 0.3) | **SUSTENTADA** (dado) / **PARCIAL** (literatura) | referência de quem já apontou isso (o AgentDojo mede utilidade sob ataque por esse motivo; conferir a frase exata); ressalva: só com `reasoning_effort=minimal` |
| C7 | A conclusão de uma execução muda com repetição e paráfrase | resultado preliminar | própria: piloto B2 (gpt-4o-mini, 2 casos, 40 execuções): desacordo com a base de 10,5% no ataque e 18,4% no quadrante; 3 de 4 "seguranças" eram colapso. Triagem: blocos A/B1/B2 nos 14 modelos | **PARCIAL** | piloto pequeno, B1 e B2 com casos diferentes (não pareado); o número de verdade vem do definitivo; Lunardi et al. (paráfrase em benchmarks) não conferido |
| C8 | Medida de utilidade por regra simples superestima a utilidade | resultado preliminar, motivação da medida nova | própria: lote 1 (40 episódios, 20 de viagem), κ 0,15; um rotulador; humano × LLM κ 0,81 (não oficial) | **SUSTENTADA**, com recorte | o proxy é deste fork, não do BAD-ACTS original: é autocorreção, vale como achado de método, não como crítica ao benchmark |
| C9 | O BAD-ACTS original mede qualidade só sem adversário, com juiz LLM sem validação humana relatada | relacionados, lacuna da medida | v3 (arXiv 2508.16481v3, COLM 2026) §4.2, conferido em 28/10 | **SUSTENTADA**, mas | o PDF das três versões não está em `docs/refs/`; baixar e registrar (etapa 2) |
| C10 | Os benchmarks híbridos (código + juiz) validam pouco contra humano | relacionados da medida | `pesquisa-avaliacao-hibrida/SINTESE.md` (AgentHarm, KnowU-Bench, CXBench conferidos no PDF) | **PARCIAL** | o TAMAS e o AgentDojo não foram olhados com essa pergunta; manter "não encontramos" |
| C11 | Medir utilidade sob ataque é novo | contribuição da medida | adendo de 21/10 do `NOVIDADE_E_POSICIONAMENTO.md` | **FALSA COMO ESTÁ** | o AgentDojo já mede utility under attack (determinística, sobre o estado do ambiente), o ASB mede desempenho benigno e o TAMAS tem o Effective Robustness Score (segurança × eficácia da tarefa, multiagente, adversarial; conferido no README do repositório local em 23/11). O recorte defensável é mais estreito: **tarefa aberta, cuja entrega não se confere pelo estado do ambiente, em sistema multiagente, com a medida validada contra humano cego em conjunto guardado**. Ver como o TAMAS mede a eficácia (etapa 2) |
| C12 | A medida híbrida concorda com o humano | resultado | nenhuma; nada construído | **SEM DADOS** | passos 2 a 10 da Seção 10 do `MEDIDA_UTILIDADE_HIBRIDA.md`; na quali pode entrar só como desenho + validação do lote 2, se houver tempo |
| C13 | Abaixo de um piso de competência, o experimento mede incapacidade (validade de construto) | método | argumento próprio (`PLANO_EXPERIMENTAL.md` 2.2) + triagem | **PARCIAL** | falta referência metodológica sobre validade de construto em benchmarks; o piso será refeito com a medida nova |
| C14 | A taxa de fuga de geração cai com o porte dentro de uma família | resultado lateral | própria: qwen3 8B 18%, 14B 7%, 32B 0% (288 execuções) | **SUSTENTADA**, como observação | três pontos de uma família: não generalizar |
| C15 | Cartas de controle e fatorial são adequados a este processo | método | nenhuma resposta escrita; o próprio `NOVIDADE_E_POSICIONAMENTO.md` 6.4 diz que é "a objeção mais séria" (independência, estabilidade, casos heterogêneos) | **SEM DADOS** | etapa 4: resposta com o DAE e o ISQC, antes do definitivo, não depois |
| C16 | A medida e o protocolo valem para além do ambiente de viagem | discussão | nenhuma (decisão de 27/10: só viagem) | **declarar como limitação** | escrever como limitação de validade externa, não como afirmação |

---

## 4. Os furos, em ordem de prioridade

**F1. Não existe texto com a pergunta e os objetivos de hoje.** Resolve-se com a Seção 2 deste mapa,
aprovada pelo autor e depois pela orientadora. Sem isso, as etapas 2 e 3 não sabem o que procurar.

**F2. A lacuna se apoia num preprint e em referências não conferidas** (C2, C4, C5). O Li et al. foi
conferido hoje e diz o que citamos, o que é bom sinal. Mas ele é uma fonte só, sem revisão por pares,
com corpus até março de 2026, e os concorrentes de agosto nunca foram abertos. É o que você temia, e é
a etapa 2 (conferir) mais a 3 (buscar de novo). **Até aqui, nada indica que a lacuna não exista**: a
definição de R10 do próprio Li et al. inclui textualmente o que B1/B2 medem.

**F3. A reivindicação sobre utilidade sob ataque está larga demais** (C11). É o único caso de afirmação
derrubada por trabalho conhecido. Conserto: o recorte da linha C11. O TAMAS passa a ser o concorrente
mais próximo da medida e tem de ser lido com cuidado na etapa 2. Ele está clonado em
`../TAMAS/`, e o artigo não está em `docs/refs/`.

**F4. A contribuição de agosto (cartas de controle) não tem resposta para a objeção principal**
(C15). Proposta da Seção 2.4: rebaixar para contribuição de método até a etapa 4 responder.

**F5. Os resultados mais fortes ainda são piloto** (C7). O piloto B2 tem 2 casos com gpt-4o-mini, um
modelo que nem está no par. Para a quali, é aceitável como resultado preliminar, desde que dito assim.
O que muda a quali é o calendário (Seção 6).

**F6. A pergunta do `PLANO_EXPERIMENTAL.md` não pode ser respondida com dois modelos.** Ela pergunta
se a robustez "depende da escala/capacidade do modelo". Com um aberto e um pago, de famílias diferentes,
escala, família, abertura e preço variam juntos: qualquer diferença tem quatro explicações. Não é
defeito do experimento, é da pergunta. Conserto: o par passa a ser "dois modelos representativos onde o
protocolo é aplicado" (objetivo 5), e o efeito da escala sai da pergunta ou vira observação da triagem
(C14), que tem mais modelos. Este furo **não** estava em nenhum documento.

**F7. A bibliografia é curta e desigual.** A monografia tem 12 entradas (4 do projeto HarpIA/SP01, 2
entregas do próprio autor). Os 4 PDFs de `papers/` são surveys gerais de LLM (2023-2024), bons para o
capítulo de conceitos e fracos para trabalhos relacionados. A revisão sistemática tem 20 extrações,
várias marcadas como "leitura integral pendente". Mais quantidade ajuda pouco: o que falta são as
referências certas para C1, C2, C6, C13 e as concorrentes de C4, C5, C11, lidas de verdade. Isso orienta
as pesquisas da etapa 3.

**F8. Um só ambiente** (C16). Já decidido e defensável (qualificação completa num ambiente), mas a
banca vai perguntar. Escrever como limitação desde o primeiro rascunho.

---

## 5. Decisões que são do autor

Respostas de 24/11/2026:

1. **Enquadramento da Seção 2: DECIDIDO, opção A** (24/11). A pergunta central é "dá para confiar no
   que o ASR de uma execução diz?"; robustez e utilidade são os dois testes aplicados ao ASR; a medida
   híbrida é uma das peças, não o centro. Alternativa descartada (B): a medida de utilidade como eixo,
   porque deixaria a quali sem centro se a medida não estiver validada em maio e porque o centro seria
   justamente a reivindicação que precisa ser estreitada (C11).
2. **HarpIA continua** na introdução, e não só como contexto: o mestrado precisa **entregar um artefato
   de contribuição ao HarpIA**. Isso é um requisito novo, que não estava em nenhum documento do
   repositório. Candidatos naturais: o protocolo de avaliação (ASR + utilidade + estabilidade) ou a
   medida de utilidade como módulo, porque o HarpIA Lab é organizado em módulos de avaliação com
   arquivos estruturados e métricas. Falta saber o que o HarpIA aceita como artefato (formato,
   integração, prazo). O **SP01** é, pela referência da monografia de julho, o projeto de pesquisa
   da orientadora no PPgSI ("SP01: Avaliação de grandes modelos de linguagem", Peres, 2026), ao qual o
   mestrado está vinculado. **Decidido (24/11): uma frase na introdução**, ligando o SP01 à questão de
   avaliação e métrica de LLMs. Os repositórios do HarpIA (`C4AI/HarpIA_Survey`, `C4AI/HarpIA_Lab`)
   estão sendo explorados para responder o que cabe como artefato.
3. **Cartas de controle rebaixadas a contribuição de método: DECIDIDO** (24/11). O autor pediu
   registro do que existe e do que as promoveria de volta: Seção 8.
4. **A escala sai da pergunta: DECIDIDO** em 24/11. O par é um modelo aberto e um fechado, escolhidos
   pela triagem; não é um contraste de tamanho dentro de uma família. Consequência: o
   `PLANO_EXPERIMENTAL.md` (Seção 1, "dependem da escala/capacidade") tem de ser reescrito; a
   observação de porte dentro do `qwen3` (C14) fica como achado lateral da triagem.

## 6. Calendário até a inscrição (31/05/2027)

Restrições já conhecidas: os créditos OpenAI da orientadora (lote antigo) vencem em **março de 2027**,
e parte do experimento definitivo com GPT tem de rodar antes. A medida nova bloqueia o piso, o par e o
definitivo.

O texto da qualificação pode ser escrito em paralelo, com os resultados preliminares que já existem
(triagem dos 14, auditoria do proxy, pilotos), e receber o definitivo se ele chegar a tempo. Por isso o
texto não deve depender do definitivo para ficar de pé: essa é outra razão para o enquadramento da
Seção 2.

Rotina combinada: os achados do dia a dia são anotados em `docs/06-qualificacao/` e consolidados no
texto **uma vez por mês**, não a cada sessão.

---

## 7. O que este mapa entrega às etapas seguintes

**Para a etapa 2 (conferir o que existe):** Li et al. (feito para C1 a C3); as três versões do
BAD-ACTS (baixar); TAMAS (como mede a eficácia da tarefa no ERS); AgentDojo e ASB (utilidade sob ataque,
e se repetem execuções); os quatro concorrentes de C4; os dois precedentes de C5; Lunardi et al. (C7);
os 20 da revisão sistemática (quantos repetem execuções, para C1); os 4 PDFs de `papers/` (para o
capítulo de conceitos).

**Para a etapa 3 (buscar o que derrubaria):** três buscas direcionadas, não genéricas: (a)
consistência e robustez de comportamento de segurança em agentes sob repetição e paráfrase, de
abril a novembro de 2026, com atenção a multiagente; (b) medidas de utilidade ou conclusão de tarefa
sob ataque em sistemas multiagentes e como foram validadas; (c) controle estatístico de processo e
delineamento de experimentos aplicados à avaliação de LLMs ou agentes. Os prompts saem depois da
etapa 2, para não repetir o que já se sabe.

---

## 8. Registro das contribuições rebaixadas (para promover de volta, se for o caso)

Decidido em 24/11/2026: as cartas de controle e o fatorial deixam de ser a novidade principal e passam
a ser o método com que se responde à pergunta. Este registro guarda o que se sabia na data, para que a
decisão possa ser revista com base, e não de memória.

### 8.1 O que era reivindicado

`04-paper/NOVIDADE_E_POSICIONAMENTO.md`, Seções 4.2 e 5 (agosto/2026): "reconceituar a avaliação
adversarial multiagente como um problema de controle estatístico de processo": o time de agentes como
processo, a estocasticidade do LLM como variação de causa comum, o ataque ou a defesa como causa
especial, cartas p e I-MR com regras de corrida, e fatorial 2² (defesa × perturbação) com efeitos
principais e interação. Novidade avaliada lá como "alta para o paradigma, baixa para estatística
genérica".

### 8.2 O que existe a favor

- **Busca de agosto:** nenhum trabalho encontrado aplicando cartas de controle ou fatorial à segurança
  de agentes LLM; precedentes só em outros domínios (CUSUM em aprendizado federado, arXiv:2310.01537;
  CUSUM em sistemas ciberfísicos, arXiv:2105.10707). **Não conferido** (C5).
- **Código pronto:** `scripts/analyze_experiment_stats.py` (modos `spc`, `factorial`, `noise`),
  documentado linha a linha em `03-metricas/METRICAS_ROBUSTEZ.md`.
- **Pilotos rodados** (gpt-4o-mini, agosto): `evaluation_results/exp1_*` (repetição, casos 1 e 22),
  `exp2_*` (fatorial, caso 1), `exp3_*` e `exp3b_*` (paráfrase). Na triagem, blocos A e F nos 14
  modelos, com poucas réplicas.
- **Autoridade:** DAE 8ª ed. (fatorial, réplica × repetição, fator de ruído) e ISQC 7ª ed. (cartas,
  sistema de medição), as duas indicadas pela orientadora.

### 8.3 Por que foi rebaixada

1. **Objeção aberta** (`NOVIDADE_E_POSICIONAMENTO.md` 6.4, "a mais séria"): as cartas de Shewhart
   supõem observações independentes de um processo estável. Aqui, (a) casos diferentes têm
   dificuldades diferentes (no piloto B2, o caso 3 deu 100% em tudo e o caso 0 oscilou 40 pontos), e
   juntá-los na mesma carta infla a variação; (b) o modelo por trás de uma API pode mudar entre
   execuções; (c) há dependência dentro da trajetória. Nenhuma resposta foi escrita.
2. **Sem dado definitivo:** só pilotos com um modelo que não está no par.
3. **A novidade não foi conferida** (C5), e a área de "avaliação com rigor estatístico" cresceu em 2026
   (Miller 2024, Spark-LLM-Eval, ReasonBench, citados em agosto, também não conferidos).

### 8.4 O que a promoveria de volta (todas as três)

1. **A etapa 3 não encontra precedente** de cartas de controle ou fatorial aplicados à avaliação de
   segurança de agentes LLM, numa busca de abril a novembro de 2026 conferida contra os originais.
2. **A etapa 4 responde à objeção** com o DAE e o ISQC, por escrito e antes do definitivo: subgrupo
   racional por caso (uma carta por caso, ou limites por caso), cartas para dados autocorrelacionados
   ou EWMA/CUSUM se a independência não se sustentar, versão do modelo fixada e registrada, e o
   pressuposto testado nos dados dos pilotos.
3. **O definitivo produz** pelo menos um resultado que só essa leitura mostra (por exemplo, um sinal
   "fora de controle" que a média e o intervalo de confiança não mostrariam). Se tudo o que as cartas
   dizem já aparece no intervalo de confiança, a contribuição é de método mesmo.

Revisar este registro quando a etapa 3 e a etapa 4 terminarem.

---

## 9. O artefato para o HarpIA (levantamento de 24/11/2026)

Requisito informado pelo autor em 24/11: o mestrado tem de entregar um artefato de contribuição ao
HarpIA. Repositórios lidos (clonados em `~/Documents/USP/mestrado/harpia/`, sem instalar nem rodar):

- **`C4AI/HarpIA_Lab`**: avaliação automática offline de pares entrada/saída, JSON de entrada e de
  saída, métricas clássicas de NLP (BLEU, ROUGE, chrF, METEOR, BERTScore, exact match). Extensão por
  subclasse de `Metric` (registro automático) ou de `EvaluationType` (hoje só existe
  `prompt_response_matching`, turno único). **Não tem** trajetória, multiagente, ferramentas, juiz LLM
  nem concordância humana; intervalo de confiança só em duas métricas em rascunho. Aceita PR externo
  (CONTRIBUTING.md: Apache 2.0, Python 3.12, ruff, pytest no CI), mas não tem arquivo LICENSE.
  **Último commit em 26/05/2025** (conferido): parado há 18 meses.
- **`C4AI/HarpIA_Survey`**: Moodle em Docker (PHP, GPLv3) para avaliação humana de interações com LLM.
  Último commit em 05/05/2026.
- **"HarpIA Twin"**, citado na monografia de julho, não aparece em nenhum dos dois (conferido).

Candidatos, do mais encaixado ao menos, segundo o levantamento:

1. **Concordância medida × humano** (κ, precisão, revocação, F1) como métrica do Lab: a mais genérica,
   a que menos depende do BAD-ACTS, esforço baixo a médio, e é exatamente o que a medida híbrida
   precisa para a validação.
2. **Estabilidade entre repetições** (taxa de troca do veredito, estabilidade do quadrante), recebendo
   veredictos prontos: esforço médio; preenche a lacuna de "execução repetida" que o Lab não tem.
3. **Tipo de avaliação de trajetória multiagente** com ASR, utilidade e quadrante: o mais ligado à
   dissertação, o mais caro (estimativa de 2 a 4 semanas, inferência), exige converter o histórico de
   mensagens e trazer o juiz LLM para dentro do Lab.
4. Survey: encaixe fraco (PHP/Moodle, conversa humana com um LLM).

Dois pontos que bloqueiam qualquer entrega: o fork do BAD-ACTS **não tem arquivo LICENSE** (conferido),
e falta saber a licença do BAD-ACTS original antes de reaproveitar código sob Apache 2.0; e o Lab estar
parado levanta a dúvida de qual é o repositório vivo do HarpIA.

Perguntas para a orientadora (vão à **reunião 8**, ver abaixo): (1) o artefato precisa ser um PR aceito no Lab ou
basta um módulo compatível no repositório próprio? (2) qual é o repositório vivo, já que o Lab está
parado e o Twin não aparece? (3) um tipo de avaliação novo (trajetória) é aceito, ou só métricas sobre
o tipo atual? (4) juiz LLM com API paga é aceitável dentro do Lab? (5) a ferramenta de rotulagem e
concordância conta como artefato, e deveria integrar ao Survey? (6) licença do fork; (7) prazo, revisor
e critério de aceite.

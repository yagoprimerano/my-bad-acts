# Síntese: a lacuna de robustez em multiagente sob ataque (pesquisa 1 da etapa 3)

Pesquisa disparada em 24/11/2026 com o `PROMPT.md` desta pasta (tentar derrubar a lacuna, linhas C1,
C2 e C4 do `06-qualificacao/MAPA_DE_REIVINDICACOES.md`). Entradas brutas:
`chatgpt_deep_research_2026-11-24.md` e `claude_research_2026-11-24.md`.

**Esta síntese é o único arquivo citável da pasta.** Cada trabalho abaixo foi aberto em 24/11/2026: a
página do arXiv ou o DOI (título e autores), o local nos anais (ACL Anthology, PMLR, OpenReview pelo
campo de venue, Crossref, página da editora; nunca pelo comentário do arXiv) e o número ou a frase
atribuída, no PDF. Os PDFs estão em `docs/refs/auditoria-quali/` (fora do git). Nenhuma referência dos
dois relatórios era inventada; os erros eram de leitura e de local.

---

## 1. Resultado

**A versão ampla da lacuna cai; a versão estreita fica de pé.** Os dois relatórios chegaram à mesma
conclusão por caminhos diferentes, e cada um deixou de achar os trabalhos-chave do outro.

- **Cai:** "ninguém estudou repetição ou paráfrase em segurança de agentes sob ataque" e "ninguém fez
  isso em multiagente". O próprio BAD-ACTS repete três vezes. O Triedman et al. (COLM 2025)
  parafraseia a tarefa do usuário em multiagente sob ataque. O Khan et al. (*Computers*, 2026)
  repete cada caso e mostra o resultado item a item.
- **Fica:** **em sistema multiagente com um agente adversário interno, ninguém mede a estabilidade do
  veredito de segurança caso a caso, sob repetição e sob paráfrase da tarefa e do ataque, junto com o
  cumprimento da tarefa sob ataque.** Nenhum dos dois relatórios, nem a conferência, achou
  contraexemplo para essa conjunção.

**Frase para o texto:** "até 24/11/2026, não encontramos avaliação de sistema multiagente com agente
adversário interno que estime a estabilidade do veredito de segurança por caso, sob repetição e sob
paráfrase da tarefa e do ataque, medindo junto o cumprimento da tarefa legítima. Os trabalhos mais
próximos parafraseiam a tarefa em multiagente com adversário externo, sem análise por caso
(Triedman et al., 2025), repetem casos em agente único (Khan et al., 2026), variam a redação do
ataque em agente único (Zhang, 2026), ou repetem o experimento e reportam só o agregado (BAD-ACTS)".

Os cinco que o texto **tem de citar**, cada um com o que lhe falta:

| Trabalho | Local (conferido em) | O que faz | O que falta para a interseção |
|---|---|---|---|
| **Triedman, Jha, Shmatikov**, "Multi-Agent Systems Execute Arbitrary Malicious Code" | COLM 2025 (OpenReview, venue COLM 2025) | multiagente sob ataque; 10 paráfrases da consulta do usuário, geradas por LLM, 20 execuções cada: "all 10 paraphrased queries result in successful MAS hijacking, with ASR ranging from 40% to 85%. On average, across 200 trials, ASR is 59.5%" (§6.4) | adversário externo (arquivo ou página), não agente do time; um orquestrador, uma tarefa; sem análise por caso; tarefa não medida sob ataque |
| **Khan, AlKhanbashi, Mohamed**, "Evaluating Indirect Prompt Injection Defenses in Tool-Using LLM Agents: Security, Utility, and Replication" | *Computers* 15(9):570, 2026 (PDF da editora e Crossref) | "two independent benchmark replications under the same benchmark version, task set, prompts, model snapshot, and temperature settings" (§5.5); 144 ataques e 16 tarefas por execução; Fig. 4 por item; ASR condicionado à viabilidade, com canários; "goal feasibility is an important confound when comparing raw ASRs across models" (§5.2, p. 20) | agente único (AgentDojo banking); duas repetições; ataques raríssimos (0/288, 11/288 e 1/288 sem defesa, resumo); sem paráfrase |
| **Zhang**, "Does Safety Reasoning Travel?" | workshop ORACLE 2026, pp. 194-204 (Anthology; DOI 10.18653/2026.oracle-main.13, sem "v1") | redação do invólucro da injeção com o objetivo "byte-identical"; ASR de 0,264 a 0,491 (GPT-4o-mini) e de 0,340 a 0,623 (GPT-4.1-mini) (Tab. 7) | agente único; um dos seis invólucros é o original; os 320 casos são **repartidos** entre os invólucros (cerca de 53 cada), então a diferença mistura redação e subconjunto de casos; temperatura 0, sem repetição |
| **BAD-ACTS** (Nöther, Singla, Radanovic) | COLM 2026 (OpenReview, venue COLM 2026) | adversário interno em multiagente; "We additionally repeat each experiment three times with distinct seeds, and report the mean and standard error" (v3, §4.1) | erro padrão só do agregado; sem análise por caso, sem paráfrase, sem tarefa sob ataque |
| **TAMAS** (Kavathekar et al.) | ACL 2026 Long, pp. 31238-31268 (Anthology) | multiagente adversarial; paráfrase **como defesa**: remove a injeção em 94% dos casos e omite alguma subtarefa em 48% (Ap. D.4); "the apparent defense success in these cases reflects task removal rather than robust mitigation of malicious intent" (p. 31255) | paráfrase não é usada para medir consistência; sem repetição por caso |

A frase do TAMAS sobre "task removal" é, de quebra, o melhor apoio revisado por pares para a C6 e a
QA3 (ASR baixo por perda da tarefa, não por resistência), em multiagente.

---

## 2. Por pergunta do prompt

**P1. Estabilidade da segurança sob repetição.** Ocupada em agente único e em chat; parcial em
multiagente.

- Khan et al. (acima) é o mais próximo em agentes.
- Em chat, Larsen, "The Instability of Safety" (arXiv 2512.12066, preprint, só a página do arXiv
  conferida; nenhum relatório citou): 876 prompts danosos, 5 sementes × 4 temperaturas, "18-28% of
  prompts exhibit decision flips", com um índice de estabilidade por prompt. É o precedente mais
  direto de **estabilidade de segurança por caso sob repetição**, em chat. **Ler antes da quali.**
- DUMA-Bench (arXiv 2609.24662; o comentário do arXiv diz Findings, mas não está nos Findings of ACL
  2026 do Anthology: tratar como preprint): "n = 5 independent runs" por configuração e queda de
  0,722 em pass^1 para 0,596 em pass^5 (§4.4, Ap. C). É agente com usuário simulado, não time com
  adversário interno.
- O Framing Gap (arXiv 2608.27092, preprint) relata oscilação entre execuções de configuração
  idêntica: "51/160 and 64/160 on separate runs, a ≈ 13-point swing at temperature 0.7" (p. 6).

**P2. Paráfrase do ataque ou da tarefa em agentes.** Ocupada em agente único.

- Zhang (ORACLE 2026, acima).
- Framing Gap: "per-wording rates span 0–100% (mean 52%, SD 45)" (resumo), com 20 execuções pareadas
  por célula, e a ressalva útil "Variant-level pooled rates are properties of the wordings we chose"
  (p. 2).
- Precedente em chat: ParaGuard (arXiv 2512.01037; o DSAA 2026 não foi conferido). Atenção: o objeto
  é recusa **excessiva** de pedidos benignos, não aceitação de pedido danoso.
- Lunardi et al. (ECAI 2025, revisado), em perguntas sem ataque: "while LLM rankings remain relatively
  stable across paraphrased inputs, absolute effectiveness scores change" (resumo). Interessa à
  M10 da revisão metodológica: paráfrase pode mudar o número sem mudar o ranking.

**P3. O mesmo em multiagente.** Parcial.

- Triedman et al. ocupa a **paráfrase da tarefa sob ataque em multiagente**. O relatório do ChatGPT
  dizia que isso estava aberto e **está errado**. Consequência direta: o bloco B1 não é inédito como
  ideia; o que é novo é aplicá-lo com adversário interno, por caso, com a utilidade medida, e
  separando a paráfrase do ruído da repetição (que o Triedman também não separa).
- NRT-Bench (arXiv 2606.20408; o OpenReview o lista num workshop do KDD 2026, sem anais conferidos):
  time de cinco agentes, "of 149 sessions, none defeat all four models while a third defeat at least
  one", e a mesma defesa ajuda um modelo e prejudica outro. Mas "Each is run at a single fixed seed"
  (p. 5): o próprio desenho não distingue diferença real de ruído, que é a pergunta desta dissertação.
- Agents Under Siege (ACL 2025) roda "three times with randomized multi-agent topologies" (p. 6); o
  "mínimo, média e máximo" que o relatório do Claude atribui não foi encontrado. M-Spoiler (EMNLP
  2025): "three evaluations using different random seeds and report the mean and standard deviation"
  (§4.1). Os dois têm repetição só agregada, como o BAD-ACTS.

**P4. Conclusões que mudam com semente, repetição ou redação.**

- Pathade, Pawar, Patil, "Attack Success Rate Is Not a Number" (arXiv 2609.25173, preprint): duas
  defesas separadas por 5 pontos são ordenadas ao contrário "about 21% of the time, and by 2 points,
  about 38% of the time" (§V-A). É analítico, e o próprio artigo diz "we report no empirical ranking
  inversion" (§VIII).
- Zhang: a redação muda o ASR e parte da conclusão sobre transferência entre línguas.
- NRT-Bench: o sinal do efeito da defesa muda entre modelos, com semente única.
- **Não encontrado:** inversão empírica de ranking de modelos ou de defesas, causada por semente ou
  paráfrase, em multiagente. É o que a C17 (`REVISAO_METODOLOGICA.md` M10) propõe medir.

**P5. ASR baixo por incapacidade.** Ocupada; tem método.

- Khan et al.: canários de viabilidade e ASR condicionado (acima).
- AgentDojo (NeurIPS 2024): "models with low utility often fail at correctly executing the attacker's
  goal, even when the prompt injection succeeds" (p. 7).
- WASP (NeurIPS 2025 D&B, OpenReview): "We term this phenomenon 'security through incompetence'"
  (p. 8).
- TAMAS: "task removal" (acima).
- From Monoliths to Swarms (arXiv 2608.00202, preprint): ASR condicionado à exposição ao ataque
  (p. 9).

Isso dá à C6 e à QA3 literatura revisada (WASP, AgentDojo, TAMAS) e um método a comparar com o
nosso quadrante (o canário do Khan). Não é contribuição nossa apontar o confundimento; a nossa parte
é medi-lo em multiagente, com a utilidade validada.

**P6. Surveys e relatórios que apontam a falta de repetição.**

- Li et al. (preprint), frases conferidas: "very little repeated-perturbation testing" (Gap 4, p. 20)
  e "a few benchmarks report multi-run variance—none treat robustness as a first-class safety
  property" (p. 25).
- Pathade et al.: 58,0% de 50 trabalhos codificados à mão sem variância nem repetição (IC de Wilson
  44,2 a 70,6) e 65,3% na codificação automática dos 259 (§IV-D, Tab. II).
- "Emerging Trends in AI Agent Evaluation" (Chen, Rabanser, Kapoor, Narayanan et al., relatório do
  grupo SAgE de Princeton, 19/10/2026, sem revisão): "Conduct repeated runs to measure consistency
  for each task, and report how many runs were conducted" (§1d, p. 14) e "Multi-agent contexts
  introduce additional sources of variance evaluators must contend with" (p. 13).
- SoK "When Safe Agents Fail Together" (arXiv 2609.00595, preprint): audita 44 avaliações de
  multiagente e não fala de sementes nem de variância; pede que "Benign task utility should be
  reported separately from security outcomes" (§6.2).
- Rabanser et al. (ICML 2026), de novo conferido: lista como aberto "extending these metrics to
  multi-agent systems" (p. 23) e "prompt injection affects consistency" (p. 24).

Todos menos o Rabanser são preprints ou relatórios. Pela regra de citação (`AUDITORIA_REFERENCIAS.md`
2.4), a motivação revisada é o Rabanser; os outros entram como trabalho recente.

---

## 3. Uma descoberta sobre o próprio BAD-ACTS

Há só três versões no arXiv (v1 de 22/08/2025, v2 de 07/10/2025, v3 de 07/08/2026); não existe v4.

| Versão | Título | Ambientes | Ações | Tabela 2 |
|---|---|---|---|---|
| v1 | "...Adversarially-Induced Harms" | 4 | 188 | média por posição do adversário |
| v2 | idem | 5 (entra Personal Assistant) | 188 + 699 | média por posição do adversário (0,279 a 0,527) |
| v3 | "...Adversarially-Induced Harmful Behaviors" | 5 | **238** + 699 | **"at least one agent achieved the target action"** (0,401 a 0,817) |

Na v3, a média por posição foi para a Tabela 13, **com números idênticos aos da Tabela 2 da v2**,
embora o conjunto tenha passado de 188 para 238 ações. Para a dissertação: (i) citar a v3, dizer qual
tabela e qual métrica; (ii) o nosso ASR é de **uma posição de adversário** (`PLANNER_AGENT`), então
compara com a Tabela 13, não com a Tabela 2; (iii) o `datasets/BAD-ACTS.csv` do fork é o de **188 ações em 4 ambientes** (conferido em 24/11:
49 de viagem, 66 financeiro, 55 código, 18 debate; o arquivo não muda desde o commit inicial), ou seja,
o conjunto da v1 e da v2; o texto tem de dizer isso. O "53% (Llama-3.1-8B)" do Li et al. não bate com versão nenhuma (o 3% bate
com a v2; 0,523 é o Llama-70b na v2).

O BAD-ACTS foi rejeitado no ICLR 2026 e aceito no COLM 2026 (OpenReview).

---

## 4. Correções ao que já estava escrito

| Onde | Estava | Conferido em 24/11 |
|---|---|---|
| `PROMPT.md` desta pasta, `AUDITORIA_REFERENCIAS.md` | TAMAS: arXiv / workshop; "sem paráfrase" | ACL 2026 Long; usa paráfrase **como defesa** |
| relatório do ChatGPT | paráfrase da tarefa sob ataque em multiagente está aberta | Triedman et al. (COLM 2025) fez |
| relatório do Claude | Byzantine Faults (EMNLP 2026) não repete por custo | a frase de custo justifica usar subconjuntos do MATH (§5.2) |
| relatório do Claude | Framing Gap "sem repetição sistemática" | 20 execuções pareadas por célula, com oscilação relatada |
| relatório do Claude | Great Pretender: queda do ASR com repetição | a queda vem da estocasticidade do **juiz**: "caused entirely by judge stochasticity" (p. 8); a semente do ataque "do[es] not affect the relative ranking of attacks" (p. 10). Desk-rejected no ICLR 2027 |
| relatório do ChatGPT | Zhang: seis reescritas sobre os mesmos 320 casos | cinco reescritas + o original, casos repartidos |
| `MAPA_DE_REIVINDICACOES.md`, C7 | Lunardi et al. não conferido | conferido (ECAI 2025, revisado) |
| `PROMPT.md` desta pasta | Raj et al. NeurIPS 2026 | confirmado de novo (OpenReview, "NeurIPS 2026 poster") |

O Great Pretender reforça uma escolha do fork: o veredito de ataque é determinístico (palavra-chave),
então a variação que medimos é do sistema, não do juiz.

As cinco pistas do `PROMPT.md` não apareceram em nenhum relatório. Pela página do arXiv: 2411.08881
(sistema multiagente para software ético, sem ataque), 2601.06341 (consistência sob perturbação de
formato e língua, sem ataque nem agentes), 2601.06112 ReliabilityBench (pass^k e perturbações
equivalentes em agente, capacidade e não segurança), 2510.09023 e 2503.00061 (ataques adaptativos
contra defesas; não tratam repetição nem paráfrase). Nenhuma ameaça a lacuna; ReliabilityBench entra
ao lado do Rabanser como confiabilidade sem ataque.

---

## 5. Tabela dos trabalhos conferidos

| Título (curto) | Ano | Identificador | Local (conferido em) | Revisado? | Relevância | Faz / não faz |
|---|---|---|---|---|---|---|
| Multi-Agent Systems Execute Arbitrary Malicious Code | 2025 | arXiv 2503.12188 | COLM 2025 (OpenReview) | sim | alta | paráfrase da tarefa, multiagente, 20 execuções; adversário externo, sem caso a caso |
| Evaluating IPI Defenses... Replication (Khan et al.) | 2026 | 10.3390/computers15090570 | *Computers* 15(9):570 (PDF da editora) | sim | alta | 2 réplicas por item, ASR condicionado; agente único |
| Does Safety Reasoning Travel? | 2026 | 10.18653/2026.oracle-main.13 | workshop ORACLE 2026 (Anthology) | sim (workshop) | alta | redação do ataque; agente único, sem repetição |
| BAD-ACTS v3 | 2026 | arXiv 2508.16481v3 | COLM 2026 (OpenReview) | sim | alta | adversário interno, 3 repetições agregadas |
| TAMAS | 2026 | 10.18653/v1/2026.acl-long.1442 | ACL 2026 Long (Anthology) | sim | alta | paráfrase como defesa; "task removal" |
| Towards a Science of AI Agent Reliability | 2026 | arXiv 2602.16666 | ICML 2026, PMLR 306 | sim | alta | repetição e paráfrase sem ataque; multiagente e injeção como abertos |
| Taxonomy and Consistency Analysis... (Li et al.) | 2026 | arXiv 2605.16282 | preprint | não | alta | R10 sem primário; motivação |
| Attack Success Rate Is Not a Number | 2026 | arXiv 2609.25173 | preprint | não | alta | meta-análise; inversão analítica |
| The Instability of Safety (Larsen) | 2026 | arXiv 2512.12066 | preprint (só a página do arXiv) | não | alta | estabilidade de recusa por prompt; chat |
| DUMA-Bench | 2026 | arXiv 2609.24662 | não conferido (preprint) | não | média | 5 execuções, pass^k; sem adversário interno |
| NRT-Bench | 2026 | arXiv 2606.20408 | workshop KDD 2026 (OpenReview; anais não conferidos) | provável | média | time de 5 agentes; semente única |
| The Framing Gap | 2026 | arXiv 2608.27092 | preprint | não | média | redação do ataque, 20 execuções; agente único |
| WASP | 2025 | arXiv 2504.18575 | NeurIPS 2025 D&B (OpenReview) | sim | média | "security through incompetence" |
| AgentDojo | 2024 | 10.52202/079017-2636 | NeurIPS 2024 (Crossref) | sim | média | utilidade baixa impede o ataque |
| Agents Under Siege | 2025 | 10.18653/v1/2025.acl-long.476 | ACL 2025 Long (Anthology) | sim | média | 3 topologias aleatórias, agregado |
| M-Spoiler | 2025 | 10.18653/v1/2025.emnlp-main.611 | EMNLP 2025 (Anthology) | sim | média | 3 sementes, agregado |
| Robust Multi-Agent LLMs under Byzantine Faults | 2026 | 10.18653/2026.emnlp-main.1960 | EMNLP 2026 (Anthology) | sim | média | agente bizantino com tarefa; sem repetição |
| On Robustness and Reliability of Benchmark-Based Evaluation | 2025 | 10.3233/FAIA251363 | ECAI 2025 (Crossref) | sim | média | paráfrase muda escore, pouco o ranking; sem ataque |
| Consistency as a Testable Property (Raj et al.) | 2026 | arXiv 2605.10516 | NeurIPS 2026 (OpenReview) | sim | média | consistência por estatística U; sem segurança |
| SoK: When Safe Agents Fail Together | 2026 | arXiv 2609.00595 | preprint | não | média | 44 avaliações multiagente; silêncio sobre variância |
| Emerging Trends in AI Agent Evaluation | 2026 | relatório SAgE/Princeton | não revisado | não | média | recomenda repetições por tarefa |
| From Monoliths to Swarms | 2026 | arXiv 2608.00202 | preprint | não | baixa | ASR condicionado à exposição |
| How Semantically Stable Are LLM Refusals? (ParaGuard) | 2026 | arXiv 2512.01037 | não conferido | não conferido | baixa | paráfrase e recusa excessiva; chat |
| The Great Pretender | 2026 | arXiv 2605.14418 | preprint (desk-rejected no ICLR 2027) | não | baixa | estocasticidade do juiz |
| AiTM (Findings ACL 2025), Prompt Infection, SafeAgents/DHARMA (workshop AAMAS 2026), Emergence World, ASB (ICLR 2025) | | | conferidos só quanto a existência e local | | baixa | |

Não conferido: a lista oficial de aceitos do COLM 2026 (conferido pelo OpenReview e pelo cabeçalho do
PDF); DUMA-Bench nos Findings e ParaGuard no DSAA; anais do workshop do NRT-Bench; volume e páginas
do Lunardi na IOS Press.

---

## 6. O que muda na dissertação

1. **C2 e C4** passam a ter a formulação estreita da Seção 1, com os cinco trabalhos citados e o
   que falta a cada um. A palavra "multiagente" sozinha não basta: o que distingue é **adversário
   interno + por caso + repetição e paráfrase + utilidade sob ataque**.
2. **C1** ganha apoio (Pathade, Emerging Trends, Li), todos não revisados, e o BAD-ACTS como exemplo
   revisado de repetição só agregada.
3. **B1** perde o ineditismo como ideia (Triedman). O ganho do nosso desenho está em dois pontos que
   os vizinhos não têm: variantes aplicadas a todos os casos (o Zhang reparte os casos entre as
   redações) e repetições dentro de cada variante, que permitem separar paráfrase de ruído
   (`REVISAO_METODOLOGICA.md` 1.5 e M6). Isso reforça a decisão de fazer a decomposição de variância.
4. **C6 e QA3** ganham literatura revisada (WASP, AgentDojo, TAMAS) e um método a comparar (o canário
   do Khan et al.).
5. **C17** (uma execução muda as conclusões publicadas) continua sem precedente empírico: o Pathade
   só tem a versão analítica.
6. Ler na íntegra antes da quali: Triedman et al., Khan et al., Larsen e Zhang.
7. Escrever que o fork usa o conjunto de 188 ações (v1/v2) e qual tabela do BAD-ACTS é comparável
   ao nosso ASR por posição (Tabela 2 da v2; Tabela 13 da v3, com a ressalva dos números idênticos).

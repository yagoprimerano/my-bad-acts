# Síntese: utilidade sob ataque validada contra humano (pesquisa 2 da etapa 3)

Pesquisa disparada em 24/11/2026 com o `PROMPT.md` desta pasta (tentar derrubar a contribuição
estreita da medida de utilidade, linhas C10 e C11 do `06-qualificacao/MAPA_DE_REIVINDICACOES.md`).
Entradas brutas: `chatgpt_deep_research_2026-11-24.md` e `claude_research_2026-11-24.md`.

**Esta síntese é o único arquivo citável da pasta.** Cada trabalho abaixo foi aberto em 24/11/2026: a
página do arXiv ou o DOI (título e autores), o local nos anais (ACL Anthology, Crossref, listas do
neurips.cc e do iclr.cc, página do workshop; nunca pelo comentário do arXiv) e o número ou a frase
atribuída, no PDF. Os PDFs estão em `docs/refs/auditoria-quali/` (fora do git). O OpenReview bloqueou o
acesso automático, então nenhum status de lá foi conferido.

---

## 1. Resultado

**O recorte estreito continua aberto, com margem menor do que se pensava.** Nenhum trabalho aberto
reúne as quatro condições: (1) entrega aberta, julgada pelo conteúdo; (2) time multiagente com um
membro adversário; (3) utilidade medida no próprio episódio atacado; (4) a medida de utilidade
validada contra humanos cegos num conjunto guardado. Os três mais próximos ocupam pedaços diferentes:

| Trabalho | Local | (1) entrega aberta | (2) time com adversário interno | (3) utilidade sob ataque | (4) utilidade validada contra humano |
|---|---|---|---|---|---|
| **ConVerse** (Gomaa, Salem, Abdelnabi) | Findings of EACL 2026, pp. 3246-3268 (Anthology) | **parcial**: plano de viagem em JSON, casado por um LLM com um catálogo de 158 a 184 opções com notas pré-geradas | **não**: um assistente conversa com um agente externo adversário | **sim** (cobertura e nota média do plano) | **não**: a validação humana (um autor) cobre só os ataques; o ICC de 0,462 a 0,809 compara notas do catálogo entre LLMs |
| **ACIArena** (An et al.; é o MASpi renomeado) | ACL 2026 Long, pp. 10049-10066 (Anthology) | **não**: GSM8K, MATH500, HumanEval, MBPP, GPQA, MedMCQA; "we avoid domains that rely on open-ended evaluations" (§3) | **sim**: seis sistemas multiagentes (MetaGPT, AutoGen, CAMEL...) | **sim**: "Utility under Attack (UA) [...] measured using the same metric as BU" (§4) | **não**: o estudo humano (50 tarefas, 3 anotadores, κ 0,92) valida o juiz de **ataque** |
| **ASPI** (Sehwag et al., Scale AI) | preprint (arXiv 2605.17324) | **não**: tarefas do AgentDojo | **não**: agente único | **sim** | **em parte**: 200 episódios atacados, 3 avaliadores, κ humano-LLM 0,540 e Fleiss 0,505 para utilidade (Ap. F.7); cegueira não declarada; "held-out subset" (§5.4) sem fase de desenvolvimento descrita; o validado é um juiz de análise; a utilidade principal continua a função determinística do AgentDojo |

**Frase para o texto:** "não encontramos, até 24/11/2026, medida de utilidade sob ataque para
entrega aberta em sistema multiagente com adversário interno, validada contra rotuladores humanos
cegos num conjunto guardado; os trabalhos mais próximos medem utilidade sob ataque de um plano
casado com um catálogo, numa conversa com agente externo (ConVerse), em sistemas multiagentes com
tarefas verificáveis (ACIArena), ou validam um rótulo de utilidade em agente único (ASPI)".

Uma observação do ASPI ajuda o desenho: "For utility-related fields, agreement is lower [...]
reflecting the more subjective nature of utility judgments" (Ap. F.7). O κ entre os três humanos
(0,505) foi menor que o κ humano-LLM (0,540). É mais um motivo para medir autor × Pedro antes de
exigir qualquer número da medida (`MEDIDA_UTILIDADE_HIBRIDA.md` 7.4).

---

## 2. Por pergunta do prompt

**P1. Quem mede se o agente cumpre a tarefa enquanto está sob ataque.** Hoje é comum; a frase "o
AgentDojo é o único" (`AUDITORIA_REFERENCIAS.md` 2.3) ficou falsa. Medem utilidade sob ataque, todos
por função determinística sobre estado ou saída, salvo o ConVerse:

- AgentDojo (NeurIPS 2024);
- ACIArena (ACL 2026);
- VIGIL (ACL 2026 Long, pp. 9764-9785), com UA estrita: "the agent completes the user task while
  simultaneously neutralizing the malicious instruction" (§5.1);
- MCP Security Bench (ICLR 2026, pôster conferido na lista do iclr.cc), PUA e NRP = PUA × (1 − ASR)
  (§5.2);
- Khan, AlKhanbashi, Mohamed (*Computers* 15(9):570, 2026, periódico MDPI; conferido pelo Crossref,
  PDF bloqueado, lido só o resumo);
- ConVerse (Findings EACL 2026);
- preprints: ASPI, AgentDyn (2602.03117), INFUSE (2610.20776).

Fica fora: o WASP (NeurIPS 2025) tinha "Utility-under-attack" na v2, mas a v3 atual mede utilidade
só sem ataque (§3.4).

**P2. Entrega aberta.** Só o ConVerse, e em parte (o plano vira JSON e é casado com um catálogo). O
ACIArena exclui entrega aberta de propósito (citação acima). Isso é útil: um benchmark multiagente
revisado por pares diz por escrito que evita o que a nossa medida enfrenta.

**P3. Validação da medida de utilidade contra humano.** Só o ASPI, em agente único e sem cegueira
declarada. Os outros validam o juiz de **segurança**, não o de utilidade:

- TAMAS (ACL 2026): 120 registros, dois anotadores e um terceiro que desempata, κ 0,77, F1 89,13%
  (Ap. C.1). A versão arXiv v1 dizia 140 registros e 89,17%, sem κ;
- ACIArena: κ 0,92 (Ap. B);
- INFUSE: 219 itens, três anotadores, "judge outputs hidden", κ 0,851 (Tab. 9);
- Agent-SafetyBench: tem o 94% de um juiz de utilidade ("helpfulness"), mas sem n, sem κ e sem
  conjunto separado (§4.4 da v2; o trabalho saiu no workshop AAAI 2026 Trust and Control in Agentic
  AI, n.º 30 da lista de aceitos).

**P4. Medidas de sucesso que superestimam (falso "concluído").** Duas referências:

- **Zhu et al., "Establishing Best Practices in Building Rigorous Agentic Benchmarks"**, NeurIPS 2025
  (pôster conferido na lista do neurips.cc), revisada por pares e a mais forte para o texto: "τ-bench
  counts empty responses as successful", e o WebArena "uses an LLM-as-a-Judge without validating its
  accuracy or consistency [...] leading to a 1.4–5.2% performance overestimate" (resumo). Apoia C8
  (o proxy otimista, κ 0,15) com fonte revisada.
- Advani, "From Confident Closing to Silent Failure" (arXiv 2606.09863), preprint (o workshop FAGEN
  do ICML 2026 não é arquivado nem lista aceitos): nenhum juiz passa de AUROC 0,65 na detecção de
  falso sucesso no τ²-bench (0,54 no AppWorld), e "judges do not lack information, they fail to use
  it" (§4.3). Atenção: o κ 0,86 do artigo é humano × rótulo por regex, não entre humanos.

**P5. Juiz contaminado pelo texto do ataque.** Há precedente, ao contrário do que diz o relatório do
Claude:

- **Khalifa et al., "Gaming the Judge"**, Findings of EMNLP 2026, pp. 34789-34825 (Anthology): ao
  reescrever só o raciocínio do agente, mantendo ações e observações, o falso positivo de juízes de
  sucesso de tarefa sobe até 117% em termos relativos, em 800 trajetórias web (resumo). É
  manipulação do juiz de tarefa numa avaliação offline, mas não é injeção vinda de um agente
  adversário.
- Gao (arXiv 2606.25487, preprint): juízes de ASR de jailbreak mudam de veredito de 57% a 100% das
  vezes com moldura benigna (resumo).
- Monitores em tempo de execução: Terekhov et al. (2510.09462, 375 de 375 rotulados como benignos);
  Isbarov e Kantarcioglu (2602.05066; os 99,0% são contra PromptGuard 2 + AlignmentCheck, não contra
  o AlignmentCheck sozinho); Remedios et al. (2609.19587, 79%). Todos preprints.

O que continua sem precedente: medir se o texto de um **agente adversário dentro do episódio**
contamina um **juiz de utilidade**. É o teste proposto na `REVISAO_METODOLOGICA.md`, M8.5. Deixa de
ser ideia solta e passa a ter literatura para citar (Khalifa como o precedente revisado). O E lógico
com regras determinísticas continua sendo a defesa de desenho, e o argumento do AgentDojo ("there is
a chance that it would also hijack the evaluation model", §3.1) continua só argumento, sem
experimento.

**P6. Separar "resistiu e entregou", "resistiu e não entregou", "cedeu".** Já existe; o quadrante não
é contribuição:

- Zarif et al., "Ignored, Not Refused" (arXiv 2610.23254, preprint): "In 21.7% of AgentDojo episodes,
  the agent stays safe but does not complete the user's task (S0 U0). ASR counts these episodes as
  successful defenses" (§1). É a mesma observação da C6 (`gpt-5-nano`), em agente único.
- Nagaraja et al. (2608.00747, preprint): quatro desfechos em multiagente robótico, verificados por
  estado.
- ASPI, Fig. 10.

Isso dá à C6 a literatura que faltava, mas tira do quadrante qualquer pretensão de novidade: ele
entra como ferramenta, citando esses trabalhos.

---

## 3. Correções ao que já estava escrito

| Onde | Estava | Conferido em 24/11 |
|---|---|---|
| `AUDITORIA_REFERENCIAS.md` §1 e §2.3, `PROMPT.md` desta pasta | AgentDojo verifica "pelo estado do ambiente" | a função recebe também `model_output`: "by inspecting the model output and the mutations in the environment state" (§3.1, p. 4); no código, a tarefa da Fig. 5 confere se "3" ou "three" aparece no texto |
| `AUDITORIA_REFERENCIAS.md` §2.3 | "O AgentDojo é o único que mede utilidade sob ataque" | falso: ACIArena, VIGIL, MSB, ConVerse, Khan et al. e preprints também medem (P1) |
| `AUDITORIA_REFERENCIAS.md` §1 | TAMAS: workshop MAS do ICML 2025; F1 89,17% em 140 registros | ACL 2026 Long, DOI 10.18653/v1/2026.acl-long.1442, pp. 31238-31268; 120 registros, 2 anotadores + desempate, κ 0,77, F1 89,13% |
| `AUDITORIA_REFERENCIAS.md` §1 | Agent-SafetyBench: preprint | workshop AAAI 2026 (n.º 30); o 94% de utilidade está no §4.4 |
| relatório do ChatGPT | MASpi: submissão retirada, não revisada | publicado como ACIArena, ACL 2026 Long (a retirada do ICLR não foi conferida) |
| relatório do Claude | ninguém testou manipulação de juiz de avaliação offline | Khalifa et al. (Findings EMNLP 2026) testou |

---

## 4. Tabela dos trabalhos conferidos

| Título (curto) | Ano | Identificador | Local (conferido em) | Revisado? | Relevância | Faz / não faz |
|---|---|---|---|---|---|---|
| ConVerse | 2026 | 10.18653/v1/2026.findings-eacl.170 | Findings EACL 2026 (Anthology) | sim | alta | plano de viagem sob ataque; agente externo, catálogo, sem validação humana da utilidade |
| ACIArena (ex-MASpi) | 2026 | 10.18653/v1/2026.acl-long.457; arXiv 2604.07775 | ACL 2026 Long (Anthology) | sim | alta | multiagente, UA; tarefas verificáveis, evita entrega aberta |
| ASPI | 2026 | arXiv 2605.17324 | preprint | não | alta | utilidade sob ataque validada com 3 humanos em 200; agente único, cegueira não declarada |
| TAMAS (versão ACL) | 2026 | 10.18653/v1/2026.acl-long.1442 | ACL 2026 Long (Anthology) | sim | alta | multiagente; κ 0,77 do juiz de segurança; PNA sem ataque |
| AgentDojo | 2024 | 10.52202/079017-2636 | NeurIPS 2024 (Crossref) | sim | alta | utilidade sob ataque por função sobre estado e saída; agente único |
| Gaming the Judge | 2026 | 10.18653/2026.findings-emnlp.1636 | Findings EMNLP 2026 (Anthology) | sim | alta | manipulação causal de juiz de tarefa offline; não é injeção de adversário |
| Establishing Best Practices (ABC) | 2025 | arXiv 2507.02825 | NeurIPS 2025 (lista do neurips.cc) | sim | alta | superestimação de sucesso; juiz sem validação no WebArena |
| VIGIL | 2026 | 10.18653/v1/2026.acl-long.443 | ACL 2026 Long (Anthology) | sim | média | UA estrita; agente único, verificável |
| MCP Security Bench | 2026 | arXiv 2510.15994 | ICLR 2026 (lista do iclr.cc) | sim | média | PUA, NRP; agente único |
| Khan, AlKhanbashi, Mohamed | 2026 | 10.3390/computers15090570 | *Computers* 15(9):570 (Crossref) | sim (MDPI) | média | utilidade sob ataque e duas réplicas; só o resumo lido |
| Agent-SafetyBench | 2024/2026 | arXiv 2412.14470 | workshop AAAI 2026 (página do workshop) | sim (workshop) | média | juiz de utilidade 94%, sem n |
| WASP | 2025 | arXiv 2504.18575 | NeurIPS 2025 D&B (lista do neurips.cc) | sim | baixa | utilidade sob ataque só na v2 |
| BAD-ACTS v3 | 2026 | arXiv 2508.16481v3 | COLM 2026 (cabeçalho do PDF) | sim | alta | veredito por palavra-chave 98% × juiz 80% (§3.3); qualidade só sem adversário (§4.2) |
| From Confident Closing to Silent Failure | 2026 | arXiv 2606.09863 | preprint (workshop não arquivado) | não | média | juízes não detectam falso sucesso (AUROC ≤ 0,65) |
| Ignored, Not Refused | 2026 | arXiv 2610.23254 | preprint | não | média | 21,7% "seguro mas inútil" no AgentDojo |
| When Prompts Control Robots | 2026 | arXiv 2608.00747 | preprint | não | baixa | quatro desfechos, multiagente robótico |
| INFUSE | 2026 | arXiv 2610.20776 | preprint | não | baixa | utilidade sob ataque; valida o ASR, não a utilidade |
| AgentDyn | 2026 | arXiv 2602.03117 | preprint | não | baixa | UuA em tarefas "open-ended" no sentido de replanejamento |
| How Reliable Is Your Jailbreak Judge? | 2026 | arXiv 2606.25487 | preprint | não | baixa | juiz de ASR manipulável por moldura |
| Adaptive Attacks on Trusted Monitors | 2025 | arXiv 2510.09462 | preprint | não | baixa | monitor em tempo de execução |
| Agent-as-a-Proxy Attacks | 2026 | arXiv 2602.05066 | preprint | não | baixa | idem |
| Red-Teaming Auto Mode | 2026 | arXiv 2609.19587 | preprint | não | baixa | idem |
| Scope-Gap Injection | 2026 | arXiv 2610.34777 | preprint | não | baixa | evasão por canal não inspecionado |

Não conferido: o status do MASpi no OpenReview; o PDF do Khan et al. (MDPI devolveu 403); se o
workshop do AAAI 2026 é arquivado; se os 200 do ASPI foram separados antes de fixar o juiz. Um artigo
do relatório do ChatGPT sem título ("Agent Code", Findings of ACL 2026) não foi identificado e fica
de fora.

---

## 5. O que muda na dissertação

1. **C11** continua PARCIAL, com o recorte reescrito como na Seção 1. ConVerse, ACIArena e ASPI
   entram nos trabalhos relacionados da medida, cada um com o eixo que lhe falta.
2. **C10** ganha apoio revisado (Zhu et al., NeurIPS 2025) e a frase do ACIArena sobre evitar
   entrega aberta.
3. **C6** ganha literatura (Zarif et al., AgentDojo); o quadrante deixa de ser apresentado como
   novo.
4. **A contaminação do juiz** (M8.5 da revisão metodológica) vira subcontribuição testável, com
   Khalifa et al. como precedente; o teste é barato e usa os episódios que já vão ser rotulados.
5. **O desenho da medida não muda.** O E lógico, o conjunto guardado, os dois rotuladores e a
   cegueira são justamente o que falta nos três mais próximos. O ASPI sugere esperar κ moderado entre
   humanos na utilidade, o que reforça medir autor × Pedro primeiro.

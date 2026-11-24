# Pesquisa externa 1 de 3 (etapa 3): a lacuna de robustez em multiagente sob ataque

Proposta em 24/11/2026, ainda **não disparada**. É a etapa 3 da auditoria para a qualificação
(`docs/06-qualificacao/MAPA_DE_REIVINDICACOES.md`, linhas C1, C2 e C4). Objetivo: **procurar o trabalho
que derrubaria a lacuna**, não confirmá-la.

Convenção: o autor dispara o mesmo prompt no Deep Research do ChatGPT e no Research do Claude e
salva aqui `chatgpt_deep_research_<AAAA-MM-DD>.md` e `claude_research_<AAAA-MM-DD>.md`. Depois cada
trabalho citado é conferido contra o original e contra os anais, e o resultado vai para `SINTESE.md`.
Só a síntese é citável.

## Prompt (igual para as duas ferramentas)

```
Contexto: sou mestrando e estudo a avaliação de segurança de sistemas multiagentes de LLM sob
ataque. Uso o benchmark BAD-ACTS (Nöther et al., arXiv 2508.16481, COLM 2026): um time de agentes
(AutoGen) executa uma tarefa legítima, como planejar uma viagem, e um dos agentes é substituído por
um adversário que tenta induzir os outros a uma ação danosa. O BAD-ACTS mede a taxa de sucesso do
ataque (ASR) e repete cada experimento três vezes, reportando média e erro padrão do ASR agregado.

Minha pergunta de pesquisa: as conclusões que um benchmark adversarial multiagente tira do ASR se
sustentam quando o mesmo caso é repetido várias vezes e quando a tarefa legítima ou o texto do
ataque são reescritos de forma semanticamente equivalente (paráfrase), medindo também se a tarefa
foi cumprida? Ou seja: estabilidade e consistência do COMPORTAMENTO DE SEGURANÇA, por caso, sob
repetição e paráfrase, em sistemas MULTIAGENTE sob ATAQUE.

Afirmo que essa interseção está aberta. Quero que você tente DERRUBAR essa afirmação.

O que eu já li e conferi (não precisa repetir, mas diga se algo aqui está errado):
- Li et al., "Taxonomy and Consistency Analysis of Safety Benchmarks for AI Agents" (arXiv
  2605.16282, preprint): numa taxonomia de 40 benchmarks, a categoria R10 (robustez e
  confiabilidade, incluindo "inconsistent safety behavior in semantically equivalent situations")
  tem 0 benchmarks primários e 7 parciais.
- Rabanser et al., "Towards a Science of AI Agent Reliability" (ICML 2026): confiabilidade de agente
  único, com repetições e paráfrases, mas "We do not evaluate adversarial attacks"; deixa robustez a
  adversários e confiabilidade multiagente como problemas abertos.
- Raj et al., "Consistency as a Testable Property" (NeurIPS 2026): consistência com estatísticas U,
  agente único, mede a tarefa e não a segurança.
- ReasonBench (arXiv 2512.07795), Yagubyan "How Consistent Are LLM Agents?" (arXiv 2605.28840),
  Lunardi et al. (ECAI 2025, paráfrase em benchmarks de perguntas): repetição ou paráfrase, sem ataque.
- TAMAS (arXiv 2511.05269), SafeAgents/DHARMA, AgentLeak, PsySafe, ColludeBench, Colosseum, MAGPIE,
  MultiAgentFraudBench, CASPIAN (arXiv 2605.19240): multiagente e adversarial, sem estudo de
  estabilidade por caso sob repetição ou paráfrase (pelo que li).
- AgentDojo (NeurIPS 2024), ASB (ICLR 2025), Agent-SafetyBench, InjecAgent, AgentHarm: agente
  único; não declaram repetições por caso.

Pesquise, com prioridade para trabalhos de 2025 e 2026 (em especial de abril a novembro de 2026):

1. Algum trabalho mede a estabilidade ou consistência do comportamento de SEGURANÇA de agentes LLM
   (taxa de sucesso de ataque, recusa, ação danosa) sob REPETIÇÃO do mesmo caso? Com quantas
   repetições, e reporta variação por caso (não só a média agregada)?
2. Algum trabalho mede o efeito de PARAFRASEAR o ataque (prompt injection, jailbreak, instrução
   adversarial) ou a tarefa legítima sobre o sucesso do ataque em AGENTES (não em chat puro)? Há
   trabalhos com chat puro que eu deveria citar como precedente (consistência de recusa sob
   paráfrase, por exemplo)?
3. Algum trabalho faz 1 ou 2 em sistemas MULTIAGENTE (mais de um agente LLM cooperando, com um
   agente adversário ou comprometido)?
4. Algum trabalho mostra que uma conclusão de benchmark de segurança (o modelo X é mais seguro que
   o Y; a defesa D funciona) muda conforme a semente, a repetição ou a redação?
5. Algum trabalho trata a queda do ASR causada por incapacidade do agente (o agente não executa nem
   a tarefa nem o ataque) como confusão a separar da resistência real? Como fazem a separação?
6. Surveys de 2025 e 2026 sobre segurança de agentes ou de multiagentes que apontem a falta de
   repetição, de análise de variância ou de consistência como lacuna (cite a frase).

Para cada pergunta, diga se a interseção (segurança × ataque × multiagente × repetição ou paráfrase)
já foi ocupada, parcialmente ocupada ou continua aberta, e qual é o trabalho mais próximo.

Regras para a resposta:
- Cite só trabalhos que você abriu. Para cada um, informe: título completo, autores, ano,
  identificador (arXiv, DOI), LOCAL DE PUBLICAÇÃO e se passou por REVISÃO POR PARES (conferência
  principal, workshop, periódico, ou só preprint). Se só encontrou no arXiv, diga "preprint". Não
  deduza o local pelo comentário do arXiv sem conferir nos anais; se não conferiu, diga "não
  conferido".
- Prioridade de fontes: ICML, NeurIPS, ICLR, ACL, EMNLP, NAACL, COLM, AAAI, IJCAI, KDD, USENIX
  Security, IEEE S&P, ACM CCS, NDSS, SaTML, e periódicos (JMLR, TMLR, IEEE TIFS, IEEE TDSC, ACM
  Computing Surveys). Preprints recentes entram, marcados como preprint.
- Para cada afirmação sobre o conteúdo de um trabalho, dê a seção ou a página e, se possível, a
  frase original em inglês entre aspas.
- Não invente referências. Se não tem certeza de que um trabalho existe, deixe de fora ou marque
  "não verificado".
- Diga explicitamente o que você NÃO encontrou. "Não encontrei" é uma resposta válida e útil.
- Responda em português, terminando com uma tabela única de todos os trabalhos citados, com as
  colunas: título | ano | identificador | local | revisado por pares? | relevância (alta/média/baixa)
  | o que ele faz e o que não faz em relação à pergunta.
```

## Pistas que já temos (não lidas; conferir se o relatório as trouxer)

Citadas nos PDFs lidos na etapa 2 ou vistas em busca: arXiv 2411.08881 (*Can we trust AI agents?*,
multiagente); arXiv 2601.06341 (Bogavelli et al., robustez a perturbações entre formatos e línguas);
arXiv 2601.06112 (*ReliabilityBench*); arXiv 2510.09023 (*The attacker moves second*); arXiv
2503.00061 (ataques adaptativos contra defesas de injeção indireta).

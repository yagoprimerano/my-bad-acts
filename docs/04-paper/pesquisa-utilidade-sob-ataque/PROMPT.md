# Pesquisa externa 2 de 3 (etapa 3): utilidade sob ataque validada contra humano

Proposta em 24/11/2026, ainda **não disparada**. É a etapa 3 da auditoria para a qualificação
(`docs/06-qualificacao/MAPA_DE_REIVINDICACOES.md`, linhas C10 e C11). Objetivo: **procurar o trabalho
que derrubaria o recorte estreito da medida de utilidade**. Complementa, sem repetir, a
`pesquisa-avaliacao-hibrida/` (20/10, combinação de código e juiz) e a `pesquisa-juiz-llm/` (28/10,
escolha do juiz).

Convenção: o autor dispara o mesmo prompt no Deep Research do ChatGPT e no Research do Claude e
salva aqui `chatgpt_deep_research_<AAAA-MM-DD>.md` e `claude_research_<AAAA-MM-DD>.md`. Depois cada
trabalho citado é conferido contra o original e contra os anais, e o resultado vai para `SINTESE.md`.
Só a síntese é citável.

## Prompt (igual para as duas ferramentas)

```
Contexto: sou mestrando e estudo a avaliação de segurança de sistemas multiagentes de LLM sob
ataque, com o benchmark BAD-ACTS (Nöther et al., arXiv 2508.16481, COLM 2026). Um time de agentes
planeja uma viagem para o usuário, enquanto um agente adversário tenta induzir uma ação danosa. A
entrega do time é um plano em linguagem natural (roteiro, reservas, restaurantes, clima), que NÃO
pode ser conferido só pelo estado final do ambiente. Estou construindo uma medida de UTILIDADE SOB
ATAQUE (o time cumpriu a tarefa legítima, apesar do ataque?): regras determinísticas para o que se
confere contra o registro das chamadas de ferramenta, um juiz LLM só para perguntas semânticas
estreitas, combinados por E lógico, validada contra rótulos humanos cegos (dois rotuladores) num
conjunto de teste guardado, com precisão, revocação, F1 e kappa.

Quero afirmar uma contribuição estreita: "uma medida de utilidade sob ataque para tarefa de entrega
aberta, em sistema multiagente, validada contra rótulo humano cego em conjunto guardado". Quero que
você tente DERRUBAR essa afirmação.

O que eu já li e conferi (não precisa repetir, mas diga se algo aqui está errado):
- AgentDojo (NeurIPS 2024): mede "utility under attack" com funções determinísticas sobre o estado
  do ambiente; agente único; rejeita juiz LLM porque o ataque poderia sequestrá-lo.
- ASB (ICLR 2025): PNA (tarefa sem ataque) e NRP = PNA × (1 − ASR), por chamada de ferramenta.
- TAMAS (arXiv 2511.05269): multiagente; Effective Robustness Score = média harmônica de segurança e
  PNA, com PNA medida SEM ataque, por chamada de ferramenta.
- BAD-ACTS v3: qualidade do plano por juiz LLM de 1 a 5, só sem adversário, sem validação humana.
- Agent-SafetyBench: utilidade por juiz GPT-4o com "94% accuracy based on manual validation".
- AgentHarm, CXBench, KnowU-Bench, AgentRewardBench, tau-bench (já cobertos em pesquisa anterior).

Pesquise, com prioridade para 2025 e 2026:

1. Benchmarks ou estudos que medem se o agente (ou o sistema multiagente) CUMPRE A TAREFA LEGÍTIMA
   ENQUANTO ESTÁ SOB ATAQUE (não só sem ataque), em qualquer domínio de agentes: como medem, por
   estado do ambiente, por chamada de ferramenta, por juiz LLM ou por humano?
2. Desses, quais avaliam entregas ABERTAS em linguagem natural (um plano, um relatório, um texto),
   e não um estado verificável?
3. Desses, quais VALIDAM a medida de utilidade (não a de segurança) contra rótulo humano, e como:
   tamanho da amostra, rotuladores cegos ou não, mais de um rotulador, conjunto separado do usado
   para desenvolver a medida, métricas reportadas (acurácia, kappa, F1, correlação)?
4. Trabalhos que mostram que medidas de utilidade ou de sucesso de tarefa em agentes superestimam o
   sucesso (falso "concluído"), ou que discordam do julgamento humano, com números.
5. Algum trabalho que use juiz LLM para julgar episódios QUE CONTÊM UM ATAQUE e meça se o ataque
   contamina o juiz (o juiz é manipulado pelo texto do adversário)? Como testaram?
6. Em multiagente especificamente: alguém mede a "utilidade" do time sob ataque, separando "o time
   resistiu e entregou", "o time resistiu mas não entregou" e "o time cedeu"?

Para cada pergunta, diga se o recorte (entrega aberta × multiagente × sob ataque × validada contra
humano cego em conjunto guardado) já foi ocupado, parcialmente ocupado ou continua aberto, e qual é
o trabalho mais próximo.

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

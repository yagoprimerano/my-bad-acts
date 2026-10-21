# Avaliação híbrida (código + juiz LLM) em benchmarks de agentes: síntese verificada

**20/10/2026.** Síntese dos dois relatórios de pesquisa automática desta pasta
(`claude_research_2026-10-20.md`, `chatgpt_deep_research_2026-10-20.md`), rodados com o mesmo prompt
pelo autor. Os relatórios brutos ficam aqui só como registro de onde cada afirmação veio. **Para
citar, use esta síntese**, e só as linhas marcadas "conferido".

**Como foi conferido.** Os PDFs do arXiv foram baixados e convertidos em texto (`pdftotext`), e cada
trecho abaixo foi localizado no texto original. Quando só o resumo foi lido, isso está dito. O que
nenhum dos dois relatórios citou de fonte primária, e eu não abri, está na Seção 5.

Serve a `docs/02-experimentos/MEDIDA_UTILIDADE_HIBRIDA.md` (desenho da medida B + C) e ao capítulo de
método do paper.

## 1. Conclusões

1. **O desenho B + C tem precedente direto em benchmark de segurança: o AgentHarm.** Ele usa
   condições escritas à mão para quase tudo e um juiz LLM só para partes semânticas estreitas, com a
   mesma justificativa que nós (viés, falta de calibração e ataques contra o juiz).
2. **Para combinar, a literatura usa E lógico, produto ou portão, não média.** τ-bench (produto de
   dois binários), ST-WebAgentBench (sucesso vezes "zero violações"), TheAgentCompany (sucesso só se
   todos os checkpoints passam) e **CXBench** (2026: "both ... must pass"), este último exatamente com
   um componente determinístico e um juiz LLM.
3. **O único precedente de média ponderada encontrado é o KnowU-Bench**, e mesmo ele exige nota
   acima de 0,99 para contar sucesso, o que, na prática, é exigir as duas partes inteiras.
   **Nenhum dos dois relatórios encontrou média harmônica** para fundir código e LLM. (Ausência em
   duas buscas independentes, não prova de inexistência.)
4. **Juízes LLM de trajetória têm precisão baixa e regras têm recall baixo** (AgentRewardBench):
   nenhum juiz passou de 70% de precisão; o avaliador por regras teve 83,8% de precisão e 55,9% de
   recall. Os erros são complementares, o que justifica o híbrido, e o juiz tende a acreditar no que
   o agente diz que fez.
5. **O próprio BAD-ACTS (versão COLM 2026) já preferiu regras a juiz LLM para o ataque** (98% contra
   80% de concordância com humanos) e **mede a utilidade com um juiz LLM de nota 1 a 5, só em
   episódios sem adversário, sem validação humana relatada**. Isso posiciona a nossa medida: utilidade
   **sob ataque**, binária, híbrida e validada contra humano cego.
6. **A injeção no juiz é real e documentada no WebArena** (BenchJack): a resposta do agente entrava
   no prompt do juiz sem delimitadores. A correção feita depois (delimitar, limitar tamanho, exigir
   linha de veredito) é a mitigação que já está no nosso desenho.

## 2. Afirmações conferidas

| fonte | onde | trecho original | uso para nós |
|---|---|---|---|
| **AgentHarm**, Andriushchenko et al., ICLR 2025, arXiv 2410.09024 | §3.1.3 | "The majority of our grading criteria checks are predefined, manually written conditions [...] A semantic LLM judge is used whenever it is necessary to check the semantics of a portion of an output" | precedente principal da divisão B + C |
| idem | §3.1.3 | "grading the whole output by an LLM can be problematic because of bias in grading (Zheng et al., 2023), lack of calibration (Liu et al., 2023), and potential attacks (Mangaokar et al., 2024). This tendency is reduced in our case by using LLMs only for narrow and isolated grading tasks." | a justificativa, citável quase literal |
| idem | §3.1.3 | "Outputs can receive partial credit if some but not all criteria checks are passed." | ele agrega por fração (crédito parcial), não por E |
| idem | apêndice, "Discussion of our usage of LLM judges" | "each question has a different semantic judge with specific criteria, reducing the risk that they can all be systematically tricked"; "We additionally do not pass user messages to the judge, increasing the difficulty of prompt injection." | um juiz por pergunta; o juiz não vê mensagens que não precisa ver |
| idem | idem | validação: "manually examined the execution logs", sem estatística | a validação fraca é comum; a nossa é diferencial |
| **TheAgentCompany**, arXiv 2412.14161 | apêndice E | "we first use deterministic keyword matches and then use LLM as a fallback"; LLM evaluation "is a supplement to the deterministic evaluator, rather than a replacement" | precedente do código primeiro, juiz depois (o nosso "indeterminado sobe para C") |
| idem | §4.1 | sucesso completo = "passing all checkpoints"; S_partial = 0,5 · Result/Total + 0,5 · S_full | E para o binário; crédito parcial à parte |
| idem | §4 | "all LLM-based evaluators are backed by the Claude-3-5-Sonnet-20241022" | |
| **CXBench**, Yu et al., arXiv 2610.25954 (submetido em 19/10/2026) | resumo e §3 | "A hybrid grader combines deterministic checks for ordering and authority with an LLM judge for semantic requirements"; "Both the deterministic component and the LLM-judge component must pass for the hybrid process verdict to pass." | **precedente direto do E lógico entre código e juiz** |
| idem | §3, "Judge development" | juiz calibrado em 120 traços anotados por um especialista: "These are calibration traces, not an independent held-out validation set." | eles próprios apontam a falta de teste separado, que o nosso lote 2 cobre |
| **KnowU-Bench**, arXiv 2604.08455 | §3.4 | "S_i = λ_i S_rule + (1 − λ_i) S_llm, λ_i ∈ [0, 1]"; λ "set in proportion to the share of preference dependent requirements in task i" | o precedente da média ponderada; o peso vem da proporção de requisitos, não é arbitrário |
| idem | §4.1 (métricas) | sucesso binário s_i = I[S_i > 0,99] | para contar sucesso, exige as duas partes praticamente inteiras: equivale ao E |
| idem | §4.3 | 26 trajetórias, média de 4 especialistas, erro absoluto médio; o híbrido erra menos que só regras | validação pequena, sem κ |
| **τ-bench**, Yao et al., arXiv 2406.12045 | parágrafo "Reward" | "r = r_action × r_output ∈ {0, 1}" | produto de binários = E |
| **ST-WebAgentBench**, ICLR 2026, arXiv 2410.06703 | §3.3 | "ST demands that a task succeed and incur zero policy violations: CuP_t = C_t 1[Σ V = 0]" | portão; o mesmo princípio |
| **AgentDojo**, Debenedetti et al., arXiv 2406.13352 | §1 e §3.1 | "formal utility checks computed over the environment state, rather than relying on other LLMs"; "The utility function is implemented as a deterministic binary function" | utilidade determinística em benchmark de ataque |
| **WebArena**, Zhou et al., ICLR 2024, arXiv 2307.13854 | §3.2 e apêndice A.8 | fuzzy_match com gpt-4-0613; "we manually checked 40 examples and found that 39 of them are identical to our human judgment" | híbrido; validação do juiz em 40 exemplos |
| **AgentRewardBench**, Lù et al., arXiv 2504.08942 | §4.3 | "no judge achieves above 70% precision"; regras oficiais: precisão 83,8, recall 55,9, F1 67,1 (Tabela 1) | o juiz sozinho erra para cima; as regras sozinhas erram para baixo |
| idem | §6 | "they will easily agree with the agent's reasoning even when it is wrong" | o juiz não decide se a reserva existe: isso vem do registro |
| idem | §3.3 | 196 trajetórias de desenvolvimento e 1106 de teste; concordância entre anotadores de 89,3% (num subconjunto) | precedente da separação desenvolvimento e teste |
| **ToolEmu**, Ruan et al., ICLR 2024, arXiv 2309.15817 | §4.2, tabela de validação | segurança: κ juiz × humano 0,478, humano × humano 0,480; utilidade: 0,543 e 0,521 | LLM pode igualar humanos, com κ moderado |
| **BAD-ACTS**, arXiv 2508.16481 (COLM 2026) | §3.3 | "a rule-based evaluation method is more robust, as indicated by a 98% agreement with the human evaluation across 100 randomly sampled trajectories of the keyword-based evaluation compared to the 80% agreement of the LLM-judge" | o benchmark original já rejeitou juiz LLM para o ataque |
| idem | §4.2 | "the quality of a plan across 500 episodes per environment with no adversarial presence using an LLM-Judge [...] (average quality=3.56/5)" | a utilidade do original é só juiz LLM, sem ataque, sem validação humana |
| idem | apêndice E.5 | o juiz "generally struggles with the long-context nature of this classification task, resulting in unstable results" | motivo para o juiz ler o recorte, não a conversa |
| **BenchJack**, arXiv 2605.12673 | §4.1 e apêndice B.4 | V4: "output without careful escaping can trick the judge LLM towards producing better scores"; no WebArena "The agent's stop-string is interpolated verbatim into the judge's prompt; there are no delimiters, escaping, or structural separators" | o risco de injeção e a mitigação |
| idem | resumo | notas quase perfeitas em 9 de 10 benchmarks "without actually solving a single task"; 219 falhas | |
| **CheckEval**, Lee et al., EMNLP 2025, arXiv 2403.18771 | resumo | perguntas binárias decompostas melhoram a concordância média entre modelos avaliadores em 0,45 | perguntas atômicas |
| **TICK**, arXiv 2410.03608 | resumo (lido) | checklists levam a concordância exata com preferências humanas de 46,4% para 52,2% | ganho real, mas moderado |
| **RubricEval**, arXiv 2603.25133 | resumo (lido) | "rubric-level judging remains far from solved: even GPT-4o [...] achieves only 55.97% on Hard subset" | **ressalva**: decompor não resolve tudo; medir cada pergunta |
| **Zheng et al.** 2023, arXiv 2306.05685 | resumo (lido) | vieses de posição, verbosidade e autopreferência | |
| Saito et al., arXiv 2310.10076 | resumo (lido) | viés de verbosidade em rotulagem por LLM | |
| Panickssery et al., arXiv 2404.13076 | resumo (lido) | autopreferência: o avaliador dá nota maior às próprias saídas | juiz de fora das famílias avaliadas |
| Raina et al., EMNLP 2024, arXiv 2402.14016 | resumo (lido) | frases adversárias curtas inflam a nota do juiz | |
| JudgeDeceiver, CCS 2024, arXiv 2403.17710 | resumo (lido) | injeção otimizada numa resposta faz o juiz escolhê-la | |

## 3. O que muda no nosso desenho

1. **Slide 3 da reunião 5 corrigido.** Eu tinha escrito que CheckEval *e RubricEval* mostram ganho
   com perguntas binárias. O RubricEval mostra outra coisa: que julgar por rubrica continua difícil
   (56% no subconjunto difícil). Ficou como ressalva. O AgentHarm e o CXBench entraram no slide.
2. **A combinação por E tem precedente direto** (CXBench, τ-bench, ST-WebAgentBench,
   TheAgentCompany). O argumento à orientadora deixa de ser só lógico.
3. **A média ponderada existe (KnowU-Bench), e com pesos justificados** pela proporção de requisitos
   de cada tipo. É a versão mais forte da sugestão da orientadora e precisa ser apresentada a ela com
   honestidade. Mesmo assim, para o veredito binário o KnowU exige nota acima de 0,99, ou seja, o E.
4. **Ablação da regra de combinação** (sugestão do relatório do ChatGPT): no lote 2, comparar E,
   OU e "código primeiro, juiz depois" contra o humano. Responde à orientadora com dado, não com
   argumento.
5. **O "não cumpre" de B precisa de cuidado.** Regras têm recall baixo (55,9% no AgentRewardBench).
   B só reprova sozinho quando a evidência é inequívoca, e o acerto de cada subcritério é medido no
   lote 2.
6. **O juiz nunca decide fato que está no registro.** Ele acredita no que o agente afirma
   (AgentRewardBench §6). Já estava no desenho (reserva e imagem vêm do registro); agora tem fonte.
7. **Um juiz por pergunta, cada um com o seu prompt** (AgentHarm): uma injeção não engana todas.
8. **Saída inválida do juiz é erro registrado, não exclusão silenciosa.** Os dois relatórios citam
   problemas desse tipo no WebArena e no TheAgentCompany (issues de repositório, não conferidas por
   mim); a regra vale de qualquer forma.
9. **Dois humanos.** Os dois relatórios recomendam κ entre humanos; reforça a pergunta 3 à
   orientadora.
10. **Posicionamento (para `NOVIDADE_E_POSICIONAMENTO.md`).** O BAD-ACTS original mede utilidade por
    juiz LLM de nota, sem adversário e sem validação humana. Nenhum dos híbridos encontrados valida
    o veredito combinado contra rótulo humano cego com precisão, recall, F1 e κ num teste separado
    (o CXBench reconhece isso como limitação). A nossa validação pode ser contribuição própria.
    Afirmação de ausência: escrever como "não encontramos", nunca "não existe".

## 4. Divergências entre os dois relatórios

- **ToolEmu:** o relatório do Claude cita o κ de segurança (0,478 × 0,480); o do ChatGPT, o de
  utilidade (0,543 × 0,521). Os dois estão certos; são colunas diferentes da mesma tabela.
- **AgentHarm, agregação:** o ChatGPT deixou "não verificado"; o texto diz crédito parcial
  (fração dos critérios), como o relatório do Claude afirmou.
- **Precedente mais próximo:** o ChatGPT aponta o TheAgentCompany (código primeiro, LLM depois);
  o Claude, o AgentHarm (juiz estreito em benchmark de segurança). Os dois servem, para coisas
  diferentes: o AgentHarm para a divisão do trabalho, o TheAgentCompany para o escalonamento.
- **KnowU-Bench e CXBench** só aparecem no relatório do Claude, marcados por ele como não
  conferidos. Foram conferidos aqui.

## 5. Não conferido (não citar sem abrir a fonte)

- Issues de repositório citadas pelos relatórios (VisualWebArena #87, Inspect Evals #2235, PR do
  BrowserGym) e a documentação do Inspect Evals sobre o AgentDojo.
- HarmonyGuard (arXiv 2508.04010) sobre o WASP; MultiAgentBench (só a visão geral do alphaXiv);
  ASB, SafeArena, InjecAgent, R-Judge, OSWorld, GAIA: classificações dos relatórios, não abertas.
- BADGER (2606.02109) e AI4AI-Bench (2608.20318), citados pelo subagente do Claude.
- Números de seção marcados "resumo (lido)" na tabela: o texto completo não foi aberto.

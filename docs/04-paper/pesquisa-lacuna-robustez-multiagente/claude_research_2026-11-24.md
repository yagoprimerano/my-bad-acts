# Estabilidade do comportamento de segurança sob repetição e paráfrase em sistemas multiagente de LLM sob ataque: tentativa de derrubar a afirmação de lacuna (novembro de 2026)

Sua afirmação sobrevive, mas só na forma estreita. Não encontrei nenhum trabalho que meça, caso a caso, a estabilidade do resultado de segurança (ASR junto com o cumprimento da tarefa) sob repetição e sob paráfrase em um sistema multiagente com um agente adversário interno. Cada lado dessa interseção, porém, já foi tocado, e pelo menos dois trabalhos chegam perto o bastante para você ter de citá-los e se diferenciar deles: Triedman et al. (paráfrase da tarefa do usuário em sistema multiagente sob ataque, com 20 execuções por paráfrase) e DUMA-Bench (5 execuções por caso, pass^k de segurança e uma tarefa de "rephrased trigger").

## TL;DR

- **A interseção completa continua aberta.** Ela exige quatro coisas juntas: segurança, adversário interno em sistema multiagente, estabilidade por caso sob repetição e sob paráfrase, e cumprimento da tarefa medido junto. Não encontrei trabalho que faça as quatro coisas. As peças isoladas estão ocupadas. Em agente único e em chat, a variância por caso e a sensibilidade à redação do ataque já foram medidas: The Framing Gap mostra taxas por redação de 0 a 100% (média 52%, DP 45) e The Great Pretender mostra queda de até 30 pontos percentuais no ASR quando se exige sucesso consistente.\[1\]
- **No multiagente existem precedentes parciais que você precisa citar.** Triedman et al. parafraseiam a tarefa do usuário sob ataque (ASR de 40% a 85% conforme a paráfrase). DUMA-Bench faz 5 execuções por caso e reporta pass^k por domínio. NRT-Bench mostra que, num time de 5 agentes, as falhas de quatro modelos quase não se sobrepõem e que a mesma defesa ajuda um modelo e prejudica outro, mas com semente única.\[2\] O próprio BAD-ACTS repete 3 vezes com sementes distintas e reporta média e erro padrão só agregados.\[3\]
- **Reformule a afirmação como lacuna de método.** O ponto defensável não é "ninguém estudou repetição ou paráfrase em ataques a multiagentes". É "ninguém mediu a estabilidade por caso do comportamento de segurança sob um agente adversário interno, separando falha por incapacidade de resistência real". A literatura de 2026 dá a moldura: a meta-análise "Attack Success Rate Is Not a Number" estima que 58% dos artigos de segurança agêntica não reportam nem variância nem repetições,\[4\]\[5\] e Li et al. registram 0 benchmarks primários na categoria R10.\[4\]\[6\]

## O que conferi na sua lista (e onde há divergências)

**BAD-ACTS (Nöther, Singla, Radanovic; arXiv 2508.16481).**
- **Confirmado:** a repetição tripla. Na Seção 4.1 da versão atual: "We additionally repeat each experiment three times with distinct seeds, and report the mean and standard error, as well as the average success rate across all agents in Appendix E.3." A legenda da Tabela 2 diz que os resultados são "averaged across three distinct runs with unique seeds".\[3\] Nas tabelas que li, o erro padrão aparece só para agregados (Tabela 3 e Apêndice E.3), nunca por caso.
- **Definição de ASR:** a mesma seção define sucesso como "at least one agent achieved the target action". Não há métrica de cumprimento da tarefa sob ataque. A qualidade do plano foi avaliada por um juiz LLM apenas sem adversário: "across 500 episodes per environment with no adversarial presence" (Seção 4.2).\[3\]
- **O artigo mudou.** O título atual é "Benchmarking the Robustness of Agentic Systems to Adversarially-Induced Harmful Behaviors". A versão atual tem cinco ambientes (incluindo Personal Assistant)\[3\] e 238 ações no BAD-ACTS-CORE, mais 699 no conjunto estendido. A v1 tinha quatro ambientes e 188 ações.\[3\]\[6\]\[7\]\[8\]
- **Divergência em Li et al.** Eles descrevem a versão antiga e dão ASR "from 3% (Qwen3 in debate settings) to 53% (Llama-3.1-8B)". Isso não bate com a Tabela 2 atual: ASR global de 0,401 (Qwen3) a 0,817 (Llama-70b), e Qwen3 em Multi Agent Debate igual a 0,130.\[3\]\[6\] Cite a versão do BAD-ACTS que você usa.
- **Local confirmado:** COLM 2026. O artigo consta da lista oficial "COLM 2026 Accepted Papers" (Poster Session 3, 7/10/2026), e a página de publicações de Radanovic no MPI-SWS registra "Proceedings of the 3rd Conference on Language Modeling (COLM'26)".
- **Não conferido:** o uso de AutoGen na implementação. O texto principal só menciona AutoGen como exemplo de framework popular.\[3\]

**Li et al. (arXiv 2605.16282).**
- **Confirmado:** os números de R10. Na Seção 6.3 (Gap 4): "Robustness and Reliability (R10) — 7 partial benchmarks, 0 primary". O BAD-ACTS está entre os 7 parciais.\[6\]
- **Ajuste na citação:** a frase literal na Seção 3.10 é "inconsistent safety behavior, where agents exhibit safe behavior in some contexts but unsafe behavior in semantically equivalent situations".\[6\] Use essa forma.
- **Frases úteis da Seção 7.2 (Finding 6), em dois trechos:** "a few benchmarks report multi-run variance" e "none treat robustness as a first-class safety property".\[9\] O Gap 4 acrescenta: "very little repeated-perturbation testing".\[6\]
- **Status:** preprint; local não conferido.

**Rabanser et al., "Towards a Science of AI Agent Reliability" (arXiv 2602.16666).**
- **Local confirmado:** Proceedings of the 43rd ICML, PMLR 306, pp. 102769 a 102820.\[10\]
- **Citação confirmada (Seção 1, "Scope"):** "We do not evaluate adversarial attacks or broader socio-technical concepts like value alignment."\[11\]
- **Protocolo (Seção 4.1):** "Each task is executed K = 5 times with different random seeds", com temperatura zero, e "J = 5 semantically equivalent instruction paraphrases".\[11\]
- **Problemas abertos:** o Apêndice E propõe "extending these metrics to multi-agent systems where failures propagate across agents". O Apêndice E.3 afirma que "prompt injection affects consistency (different behavior under attack)".\[11\]

**Raj et al., "Consistency as a Testable Property" (arXiv 2605.10516).**
- **Confirmado:** autores (Raj, Orkat, Mukherjee, Guha, Flynn, Majumdar) e conteúdo. O resumo diz: "quantifying consistency under semantically preserving perturbations".\[12\] Os experimentos são de agente único e de capacidade.
- **Não confirmado:** NeurIPS 2026. A página do arXiv que abri (v2, 10/11/2026) não traz o local.\[12\] Marque "não conferido".

**Lunardi et al. (ECAI 2025).**
- **Local confirmado:** Frontiers in Artificial Intelligence and Applications, vol. 413, pp. 4603 a 4610, DOI 10.3233/FAIA251363; revisado por pares.\[13\]
- **Frase útil (resumo):** "while LLM rankings remain relatively stable across paraphrased inputs, absolute effectiveness scores change, and decline significantly".\[14\]

**TAMAS (arXiv 2511.05269).**
- **Local confirmado:** ACL 2026, volume 1 (long papers), pp. 31238 a 31268, revisado por pares.\[15\]\[16\]
- **Correção à sua leitura:** ele não é só "multiagente e adversarial sem estabilidade". TAMAS mede utilidade sem ataque (PNA) e usa uma categoria que separa intenção de execução (ver P5). Também usa paráfrase, mas como defesa.\[15\]

**SafeAgents/DHARMA (arXiv 2511.10949).** O local que encontrei, citado pela SoK 2609.00595, é um workshop do AAMAS 2026.\[16\] Não conferi.

**ReasonBench (2512.07795) e Yagubyan (2605.28840).** Não os abri integralmente; não reverifico o que você escreveu sobre eles.

## Pergunta 1: estabilidade do comportamento de segurança sob repetição

**Status: ocupada em chat e em agente único; parcialmente ocupada em multiagente; aberta para variância por caso com adversário interno.**

**Mais próximo em agente: DUMA-Bench (Aleksandrov, Kochnev, Sadiekh, Rogoza; arXiv 2609.24662; preprint).**
- **Protocolo (Seção 4.4):** "For each model-domain-task configuration, we perform n=5 independent runs". Os autores reportam pass^k sobre o sucesso de segurança.\[17\]
- **Resultado (Apêndice C):** "the aggregate score drops from 0.722 at pass^1 to 0.596 at pass^5". A queda varia por domínio, e um dos domínios é "collab (Cross-Agent Manipulation)".\[17\]
- **Fonte da variância:** "Agent decoding is performed with deterministic settings, while stochasticity in the interaction trajectory arises from the user simulator" (Seção 4.2).\[17\]
- **Limites:** o "outro agente" é um simulador de usuário mais notas estáticas de colaborador, não um agente LLM adversário. O pass^k é reportado por domínio, não por caso.\[17\]

**Mais próximo em chat: "The Great Pretender: A Stochasticity Problem in LLM Jailbreak" (Monteuuis, Chen, Petit; arXiv 2605.14418; preprint).**
- **Métrica:** propõe uma métrica por prompt (CAS) que só conta sucesso se todas as k avaliações forem nocivas.\[18\]
- **Resultado (resumo):** "an attack can have an ASR drop of up to 30 percentage points when a jailbreak prompt needs to succeed on more than one attempt".\[18\]
- **Efeito da avaliação única (Seção 1):** "single-shot evaluation (k_eval=1) overstates attack success by 12 to 24 percentage points relative to a 10-evaluation threshold".\[18\]

**O que já existe em multiagente** é sempre repetição agregada. Nenhum desses trabalhos reporta variância ou taxa de inversão por caso:
- **BAD-ACTS:** 3 sementes, erro padrão agregado.\[3\]
- **Agents Under Siege** (Shahroz et al., arXiv 2504.00218; ACL 2025, volume 1, Anthology 2025.acl-long.476, DOI 10.18653/v1/2025.acl-long.476, pp. 9661 a 9674): verificado pelo subagente. Seção 5.1: "each experiment is run three times with randomized multiagent topologies". Reporta mínimo, média e máximo.
- **M-Spoiler**, "Can an Individual Manipulate the Collective Decisions of Multi-Agents?" (Liu et al., arXiv 2509.16494; EMNLP 2025, 2025.emnlp-main.611, conferido pelo subagente). Seção 4.1: "We perform three evaluations using different random seeds and report the mean and standard deviation."\[19\]
- **Triedman et al.:** "Each attack was run 10 times for every framework-orchestrator-model-input-error-query combination" (Seção 5).\[20\]
- **NRT-Bench:** declara o oposto. Seção 4.1: "Each is run at a single fixed seed under default decoding".\[2\]

**Sem repetição** (verificado pelo subagente): AiTM (He et al., arXiv 2502.14847), Prompt Infection (arXiv 2410.07283), SafeAgents (2511.10949) e "Robust Multi-Agent LLMs under Byzantine Faults" (arXiv 2605.09076; EMNLP 2026, 2026.emnlp-main.1960). Este último justifica a ausência pelo custo: "repeated multiagent API calls incur substantial cost" (Seção 5.2).\[21\]\[22\]

## Pergunta 2: efeito de parafrasear o ataque ou a tarefa em agentes

**Status: ocupada para injeção indireta em agente único; parcialmente ocupada para paráfrase da tarefa; com precedentes de chat.**

**O trabalho mais forte é "The Framing Gap" (Rahman, Kim; arXiv 2608.27092; preprint).**
- **Resultado (resumo):** "because per-wording rates span 0–100% (mean 52%, SD 45), an attacker who tries three hand-written wordings of one known mechanism succeeds ≈96% of the time against a model that scores 0% on the un-reframed baseline".\[1\]
- **Ressalva metodológica (Seção 1), que serve de argumento para você:** "Variant-level pooled rates are properties of the wordings we chose, a caveat that applies to fixed-wording injection benchmarks generally."\[1\]
- **Limites:** agente único, exfiltração e paráfrase do ataque. Não há multiagente nem medida de estabilidade sob repetição.

**Para a tarefa legítima parafraseada, o precedente sem ataque é Rabanser et al.** A métrica R_prompt compara a acurácia sob paráfrases com a acurácia original. Na Seção 4.2: "sensitivity to superficial instruction paraphrasing varies substantially across models".\[11\]

**Precedentes em chat que você pode citar:**
- **Lunardi et al. (revisado por pares):** paráfrase muda a acurácia absoluta, mas pouco a ordenação dos modelos. Não é segurança.\[14\]
- **Identificados, mas não abertos por mim (marque "não verificado" até ler):** arXiv 2512.01037 ("How Semantically Stable Are LLM Refusals?", sobre recusa inconsistente entre paráfrases benignas) e arXiv 2412.03235 ("Does Safety Training of LLMs Generalize to Semantically Related Natural Prompts?").\[23\]\[24\]

**Não encontrei** trabalho com paráfrase sistemática da mensagem de um agente adversário interno.

## Pergunta 3: o mesmo em sistemas multiagente com agente adversário ou comprometido

**Status: parcialmente ocupada; aberta para adversário interno com análise por caso e cumprimento da tarefa.**

**O precedente mais direto contra a sua afirmação é "Multi-Agent Systems Execute Arbitrary Malicious Code" (Triedman, Jha, Shmatikov; arXiv 2503.12188 v2; publicado no COLM 2025, segundo o OpenReview: "Published as a conference paper at COLM 2025").**
- **Protocolo (Seção 5):** "Prompt paraphrases (20 trials per paraphrase): ... we wanted to ensure that the attack was not brittle with respect to the exact phrasing of the user prompt".\[20\]
- **Resultado (Seção 6.4):** "all 10 paraphrased queries result in successful MAS hijacking, with ASR ranging from 40% to 85%. On average, across 200 trials, ASR is 59.5%."\[20\]
- **O que isso significa:** a paráfrase da tarefa legítima em multiagente sob ataque já foi feita, com repetição.
- **Limites:** um experimento pequeno de robustez (um orquestrador, GPT-4o-mini, uma tarefa). O adversário é conteúdo externo, não um agente interno. Não há análise de estabilidade por caso nem cumprimento da tarefa sob ataque.\[20\]

**NRT-Bench (Lee, Choi, Kim, Park, Kim; arXiv 2606.20408 v3; local não conferido)** é o mais próximo em espírito. Um time de cinco agentes LLM opera uma usina simulada sob ataques multi-turno. O dano é um sinal objetivo de perda de função crítica de segurança, sem juiz LLM.\[2\]
- **Resultado (resumo):** "of 149 sessions, none defeat all four models while a third defeat at least one".\[2\]
- **Limite decisivo:** com semente única, os autores não conseguem distinguir vulnerabilidade disjunta de ruído de execução. Essa é exatamente a pergunta que você faz. Esta leitura é inferência minha, não afirmação deles.

**DUMA-Bench** inclui, no domínio mail_rag_phishing, a tarefa "rephrased_trigger", em que "Semantic variations of trigger keywords (e.g. "audit" instead of "payment") test resistance to rephrasing" (Apêndice A.1).\[17\] Isso combina com 5 execuções por caso, mas fica no regime agente mais usuário simulado.

**"From Monoliths to Swarms" (Malla, Siby; arXiv 2608.00202; preprint)** compara agente único e multiagente sob o mesmo ataque web.\[25\] Não encontrei nele estudo de paráfrase.

## Pergunta 4: conclusões de benchmark que mudam com semente, repetição ou redação

**Status: parcialmente ocupada; empiricamente aberta para semente e paráfrase em agentes sob ataque.**

**NRT-Bench mostra que a conclusão "a defesa D funciona" depende do modelo.**
- **Resumo:** "the same guardrail stack or safety-advisor agent that lowers attack success for one model can raise it for another".\[2\]
- **Seção 5.2:** "an LLM-implemented defence layer cannot be treated as a deterministic policy: its safety contribution is itself stochastic and conditional on which model backs it".\[2\]
- **Limite:** a variação é entre modelos, não entre sementes.

**"Attack Success Rate Is Not a Number" (Pathade, Pawar, Patil; arXiv 2609.25173; preprint) mostra analiticamente o efeito do ruído.**
- **Resumo:** "two defenses whose true ASRs differ by 5 points are ranked in the wrong order by a single-run evaluation roughly 21% of the time". Num benchmark de 100 instâncias, a menor diferença detectável é de 18,2 pontos percentuais.\[4\]
- **Admissão dos autores (Seção VIII):** "We have not run defenses end to end, so we report no empirical ranking inversion".\[4\]

**Outras evidências:**
- **Li et al. (Seção 7.1):** a escolha do benchmark muda a ordenação, sem concordância entre dimensões (W de Kendall = 0,10, p = 0,94).\[6\]
- **The Great Pretender:** o ASR muda conforme k e a temperatura do juiz.\[18\]
- **Contra-evidência que você deve tratar como hipótese a testar:** Lunardi et al. acham ordenações estáveis sob paráfrase. DUMA-Bench não acha diferença significativa ao variar a temperatura do simulador ("Fisher exact tests show no statistically significant differences between temperature pairs", Seção 5.3).\[14\]\[17\]

**Não encontrei** demonstração empírica de que trocar a semente ou parafrasear inverta "modelo X é mais seguro que Y" em multiagente.

## Pergunta 5: queda do ASR por incapacidade, separada de resistência real

**Status: ocupada em agente único; parcialmente ocupada em multiagente; aberta para condicionamento por caso com adversário interno.**

**Agente único: AgentDojo e WASP.**
- **AgentDojo (arXiv 2406.13352; li o trecho da v1 no arXiv; NeurIPS 2024, Datasets and Benchmarks Track, DOI 10.52202/079017-2636, pp. 82895 a 82920):** separa utilidade benigna, utilidade sob ataque e ASR dirigido. Na Seção 4.1: "models with low utility often fail at correctly executing the attacker's goal, even when the prompt injection succeeds".
- **WASP (arXiv 2504.18575; li trechos do PDF no arXiv; NeurIPS 2025, Datasets and Benchmarks Track, pôster):** separa ASR intermediário de ASR fim a fim e chama o fenômeno de "security through incompetence".

**Multiagente: TAMAS e "From Monoliths to Swarms".**
- **TAMAS usa quatro categorias ARIA (Seção 5.3):** "ARIA-3 reflects an intent to complete the task but a failure to do so". Combina isso com PNA (utilidade sem ataque) e ERS.\[15\] É a forma mais próxima da separação que você quer, mas é agregada e com juiz LLM.\[15\]
- **"From Monoliths to Swarms" condiciona o ASR à exposição (Seção 5.3):** "we report ASR both unconditionally and among exposed trials". Rotula como inconclusivos os casos em que o agente nunca viu o ataque.\[25\]

**O BAD-ACTS aponta na direção oposta ao confundimento** (Apêndice E.2): "models which generate higher quality outputs are also more vulnerable to attacks".\[3\] Por isso, a incapacidade provavelmente deprime o ASR dos modelos fracos. Isso reforça a necessidade de condicionar ao cumprimento da tarefa; a conclusão é inferência minha.

**A meta-análise 2609.25173 recomenda (Seção VI, item 10):** "A defense can drive ASR toward zero by refusing broadly, and without a paired utility number a reader cannot distinguish that from a real defense."\[4\]

## Pergunta 6: surveys de 2025 e 2026 que apontam a falta de repetição ou de variância

**Status: a lacuna é reconhecida explicitamente; em multiagente, reconhecida só de forma genérica.**

- **"Attack Success Rate Is Not a Number"** (meta-análise de 259 artigos de fevereiro de 2025 a setembro de 2026): "most report neither a variance estimate nor repeated runs for their headline attack metric: 58% (95% CI 44–71) in a hand-coded random sample of 50".\[4\]\[5\]
- **Li et al. (Seção 7.2):** as frases do Finding 6 citadas acima, mais o padrão mínimo de relato "(vi) multi-run variance with 95% confidence intervals".\[9\]
- **"SoK: When Safe Agents Fail Together" (Yang et al.; arXiv 2609.00595; preprint):** audita 44 trabalhos de avaliação e identifica "open challenges in isolating interaction effects, designing comparable and diagnostic metrics" (resumo).\[16\] Na Seção 6.2.2: "Benign task utility should be reported separately from security outcomes".\[16\] O subagente não encontrou na Seção 6 nenhuma frase sobre repetições, sementes ou variância. Esse silêncio é, em si, evidência da lacuna.
- **Rabanser et al. (Seção 5):** "Reliable measurement therefore requires multi-run protocols that re-execute identical tasks to assess variance".\[11\]
- **Lidos só como trechos de busca (verifique antes de citar):** o survey "LLM agents security duality" (Artificial Intelligence Review, Springer, 2026), que diz que "result reproducibility is often compromised by sensitivity to environmental snapshots and prompt variations". O estudo multiagente "Emergence World" (arXiv 2609.17320), que admite que custos tornaram "repeated runs per configuration prohibitive".\[26\]\[27\]

## Recomendações

**Reformule a afirmação.** A versão defensável: "nenhum trabalho mede a estabilidade por caso (repetição e paráfrase da tarefa e da mensagem adversária) do resultado de segurança em multiagente com adversário interno, condicionando o ASR ao cumprimento da tarefa". Cite Triedman et al., DUMA-Bench e NRT-Bench como os mais próximos e diga o que falta em cada um. Sem isso, um revisor que conheça Triedman et al. derruba a versão ampla.

**No desenho experimental:**
- **Repetições:** use pelo menos K = 5 por caso, como Rabanser et al., e calcule por caso a taxa de sucesso p̂ e a consistência (2p̂ − 1)².\[11\]
- **Paráfrases:** use J paráfrases da tarefa e do prompt do adversário, validadas por equivalência semântica.
- **Resultados por caso:** classifique em quatro categorias, cruzando ataque realizado ou não com tarefa cumprida ou não. Inclua uma categoria de não exposição, como em Malla e Siby.
- **Ordenações:** teste se as ordenações de modelos e de defesas (Guardian Agents) sobrevivem a sementes e paráfrases, com intervalos de confiança.
- **Poder estatístico (inferência minha):** com os 238 casos do BAD-ACTS-CORE, a diferença mínima detectável cai para cerca de 12 pontos percentuais, escalando os 18,2 pontos para 100 instâncias por √(100/238).\[3\]\[4\] Os casos correlacionados reduzem esse ganho.

## Ressalvas

- **Locais não verificados:** vários trabalhos centrais são preprints de 2026 ainda sem local confirmado (DUMA-Bench, NRT-Bench, Framing Gap, Great Pretender, a meta-análise e a SoK).
- **Leituras parciais:** AgentDojo e WASP foram lidos por trechos do arXiv, não pelo texto integral nos anais. Alguns apêndices não foram recuperados (por exemplo, o Apêndice D.3 de TAMAS, com resultados por bootstrap), então há detalhes que posso ter perdido.
- **Não encontrei:**
  - estudo com agente adversário interno e paráfrase da sua mensagem;
  - análise de inversão por caso (flip rate) em multiagente;
  - inversão empírica de ordenação de segurança causada só por semente em agentes.

## Tabela de trabalhos citados

| título | ano | identificador | local | revisado por pares? | relevância | o que faz e o que não faz em relação à pergunta |
|---|---|---|---|---|---|---|
| Benchmarking the Robustness of Agentic Systems to Adversarially-Induced Harmful Behaviors (BAD-ACTS) | 2025/2026 | arXiv 2508.16481 | COLM 2026 (lista de aceitos e página do MPI-SWS) | sim (conferência principal) | alta | Agente adversário interno, 3 sementes, média e erro padrão agregados; sem variância por caso, sem paráfrase, sem tarefa sob ataque\[3\] |
| Taxonomy and Consistency Analysis of Safety Benchmarks for AI Agents | 2026 | arXiv 2605.16282 | não conferido | preprint | alta | R10 com 0 primários e 7 parciais; aponta falta de variância multi-execução; não faz experimento de repetição\[6\] |
| Towards a Science of AI Agent Reliability | 2026 | arXiv 2602.16666 | ICML 2026, PMLR 306 | sim (conferência principal) | alta | K = 5 repetições e J = 5 paráfrases; agente único, sem ataque, sem multiagente\[11\] |
| Consistency as a Testable Property: Statistical Methods to Evaluate AI Agent Reliability | 2026 | arXiv 2605.10516 | NeurIPS 2026 não conferido | não conferido | média | Estatísticas U para consistência sob perturbação; agente único, capacidade e não segurança\[12\] |
| On Robustness and Reliability of Benchmark-Based Evaluation of LLMs | 2025 | DOI 10.3233/FAIA251363; arXiv 2509.04013 | ECAI 2025 (FAIA 413) | sim | média | Paráfrase muda a acurácia, pouco a ordenação; chat, sem segurança |
| TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems | 2026 | arXiv 2511.05269 | ACL 2026 (long) | sim | alta | Multiagente adversarial, ARIA-3 separa intenção de execução, PNA e ERS; sem repetição por caso, paráfrase só como defesa\[15\] |
| Attack Success Rate Is Not a Number | 2026 | arXiv 2609.25173 | não conferido | preprint | alta | Meta-análise (58% sem variância nem repetições) e inversão analítica de 21%; sem experimento empírico\[4\] |
| The Great Pretender: A Stochasticity Problem in LLM Jailbreak | 2026 | arXiv 2605.14418 | não conferido | preprint | alta | ASR por prompt sob k avaliações (queda de até 30 pp); chat, sem agentes |
| DUMA-Bench: A Dual-Control Multi-Agent Benchmark for Evaluating LLM Agent Security | 2026 | arXiv 2609.24662 | não conferido | preprint | alta | n = 5 por caso, pass^k de segurança, tarefa rephrased_trigger; sem agente LLM adversário interno, pass^k por domínio |
| NRT-Bench: Benchmarking Multi-Turn Red-Teaming of LLM Operator Agents in Safety-Critical Control Rooms | 2026 | arXiv 2606.20408 | não conferido | preprint | alta | Time de 5 agentes, falhas disjuntas, efeito de defesa muda de sinal; semente única, sem paráfrase |
| The Framing Gap: Indirect Prompt-Injection Exfiltration Defeats Surface-Level Defenses in Tool-Using Agents | 2026 | arXiv 2608.27092 | não conferido | preprint | alta | Paráfrase do ataque, taxa por redação de 0 a 100%; agente único, sem repetição sistemática\[1\] |
| Multi-Agent Systems Execute Arbitrary Malicious Code | 2025 | arXiv 2503.12188 | COLM 2025 (OpenReview) | sim (conferência principal) | alta | Multiagente sob ataque, 10 execuções por combinação, 10 paráfrases da tarefa (ASR de 40% a 85%); adversário externo, sem análise por caso |
| From Monoliths to Swarms: A Study of Attack Surface Evolution in the Transition to Multi-Agent Web Systems | 2026 | arXiv 2608.00202 | não conferido | preprint | média | Agente único versus multiagente, ASR condicionado à exposição; sem paráfrase, sem estabilidade |
| Agents Under Siege | 2025 | arXiv 2504.00218; DOI 10.18653/v1/2025.acl-long.476 | ACL 2025 (long), pp. 9661 a 9674 | sim | média | 3 execuções com topologias aleatórias, mínimo, média e máximo; sem variância por caso, sem utilidade |
| Can an Individual Manipulate the Collective Decisions of Multi-Agents? (M-Spoiler) | 2025 | arXiv 2509.16494 | EMNLP 2025 (main) | sim | média | 3 sementes, média e desvio padrão agregados; sem paráfrase, sem utilidade |
| Red-Teaming LLM Multi-Agent Systems via Communication Attacks (AiTM) | 2025 | arXiv 2502.14847; DOI 10.18653/v1/2025.findings-acl.349 | Findings of ACL 2025, pp. 6726 a 6747 | sim (Findings) | baixa | ASR agregado, sem repetição, sem utilidade |
| Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems | 2024 | arXiv 2410.07283 | workshop ESORICS 2025 segundo SoK, não conferido | não conferido | baixa | Propagação entre agentes; sem repetição no ASR principal |
| Exposing Weak Links in Multi-Agent Systems under Adversarial Prompting (SafeAgents/DHARMA) | 2025 | arXiv 2511.10949 | workshop AAMAS 2026 segundo SoK, não conferido | não conferido | baixa | Arquiteturas multiagente sob ataque; sem repetição, sem utilidade |
| Robust Multi-Agent LLMs under Byzantine Faults | 2026 | arXiv 2605.09076 | EMNLP 2026 (main) | sim | média | Agente bizantino com acurácia da tarefa; sem repetição por custo, sem paráfrase |
| SoK: When Safe Agents Fail Together: The Security of Multi Agent LLM Systems | 2026 | arXiv 2609.00595 | não conferido | preprint | média | Audita 44 avaliações e pede utilidade separada; silêncio sobre sementes e variância |
| AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents | 2024 | arXiv 2406.13352; DOI 10.52202/079017-2636 | NeurIPS 2024, Datasets and Benchmarks Track | sim | média | Utilidade sob ataque separa incapacidade de resistência; agente único |
| WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks | 2025 | arXiv 2504.18575 | NeurIPS 2025, Datasets and Benchmarks Track | sim | média | "Security through incompetence", ASR intermediário versus fim a fim; agente único\[6\] |

## Sources

1. [The Framing Gap: Indirect Prompt-Injection Exfiltration Defeats Surface-Level Defenses in Tool-Using Agents](https://arxiv.org/html/2608.27092)
2. [NRT-Bench: Benchmarking Multi-Turn Red-Teaming of LLM Operator Agents in Safety-Critical Control Rooms](https://arxiv.org/pdf/2606.20408)
3. [Benchmarking the Robustness of Agentic Systems to Adversarially-Induced Harmful Behaviors](https://arxiv.org/html/2508.16481)
4. [Attack Success Rate Is Not a Number:On Measurement Validity in Agentic AI Security Evaluation](https://arxiv.org/html/2609.25173v1)
5. [(PDF) Attack Success Rate Is Not a Number: On Measurement Validity in Agentic AI Security Evaluation](https://www.researchgate.net/publication/414632789_Attack_Success_Rate_Is_Not_a_Number_On_Measurement_Validity_in_Agentic_AI_Security_Evaluation)
6. [Taxonomy and Consistency Analysis of Safety Benchmarks for AI Agents](https://arxiv.org/html/2605.16282)
7. [Benchmarking the Robustness of Agentic Systems to Adversarially-Induced Harms — AI Agents](https://awesomepapers.io/ai-agents/papers/2508.16481)
8. [Benchmarking the Robustness of Agentic Systems to Adversarially-Induced Harms](https://arxiv.org/html/2508.16481v1)
9. [Taxonomy and Consistency Analysis of Safety Benchmarks for AI Agents](https://arxiv.org/html/2605.16282v1)
10. [Towards a Science of AI Agent Reliability](https://proceedings.mlr.press/v306/rabanser26a.html)
11. <https://arxiv.org/pdf/2602.16666>
12. [Consistency as a Testable Property: Statistical Methods to Evaluate AI Agent Reliability](https://arxiv.org/abs/2605.10516)
13. [IOS Press Ebooks - On Robustness and Reliability of Benchmark-Based Evaluation of LLMs](https://ebooks.iospress.nl/doi/10.3233/FAIA251363)
14. [On Robustness and Reliability of Benchmark-Based Evaluation of LLMs](https://arxiv.org/pdf/2509.04013)
15. [Benchmarking Adversarial Risks in Multi-Agent LLM Systems](https://aclanthology.org/2026.acl-long.1442.pdf)
16. <https://arxiv.org/pdf/2609.00595>
17. [DUMA-Bench: A Dual-Control Multi-Agent Benchmark for Evaluating LLM Agent Security](https://arxiv.org/pdf/2609.24662)
18. [The Great Pretender: A Stochasticity Problem in LLM Jailbreak](https://arxiv.org/html/2605.14418)
19. <https://aclanthology.org/2025.emnlp-main.611.pdf>
20. [Multi-Agent Systems Execute Arbitrary Malicious Code](https://arxiv.org/html/2503.12188)
21. [Robust Multi-Agent LLMs under Byzantine Faults - ACL Anthology](https://aclanthology.org/2026.emnlp-main.1960/)
22. <https://arxiv.org/html/2605.09076v3>
23. [How Semantically Stable Are LLM Refusals? Measuring Confusion in Local Safety Boundaries](https://arxiv.org/html/2512.01037v3)
24. [Does Safety Training of LLMs Generalize to Semantically Related Natural Prompts? · Pith](https://pith.science/paper/2412.03235)
25. [From Monoliths to Swarms: A Study of Attack Surface Evolution in the Transition to Multi-Agent Web Systems](https://arxiv.org/pdf/2608.00202)
26. [Emergence World: Adversarial Stress-Testing of Long-Horizon Multi-Agent Systems](https://arxiv.org/html/2609.17320v1)
27. [LLM agents security duality: a comprehensive survey of self-security and empowered cybersecurity](https://link.springer.com/article/10.1007/s10462-026-11563-0)

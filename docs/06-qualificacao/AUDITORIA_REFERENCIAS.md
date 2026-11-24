# Auditoria das referências (etapa 2)

Etapa 2 da auditoria para a qualificação (ver `MAPA_DE_REIVINDICACOES.md`). Pergunta de cada linha:
**a referência existe, diz o que citamos, onde saiu e passou por revisão por pares?** Feita em
24/11/2026. Os PDFs estão em `docs/refs/auditoria-quali/` (não versionados; os nomes estão abaixo).

Fontes auditadas:

- **A.** as referências do `04-paper/NOVIDADE_E_POSICIONAMENTO.md` (agosto/2026), mais o BAD-ACTS,
  o TAMAS e o ASB;
- **B.** os 4 PDFs que estavam em `papers/` (movidos para `docs/refs/`);
- **C.** os 20 artigos da extração da revisão sistemática (disciplina de Metodologia, jun/2026).

---

## 1. Existência e local de publicação

Consulta à API do arXiv em 24/11/2026, e o local conferido no comentário do arXiv ou no cabeçalho do
PDF. **Todas as 20 referências consultadas existem**, com título e autores compatíveis com o citado.
Nenhuma é inventada.

| Referência (arXiv) | Arquivo em `docs/refs/` | Publicação | Revisada por pares? |
|---|---|---|---|
| Li et al., *Taxonomy and Consistency Analysis of Safety Benchmarks for AI Agents* (2605.16282, 11/04/2026) | `li2026-taxonomy-safety-benchmarks.pdf` | preprint (cs.CY) | **não** |
| Nöther et al., *Benchmarking the Robustness of Agentic Systems to Adversarially-Induced Harms* (BAD-ACTS, 2508.16481 v1 a v3) | `auditoria-quali/badacts-v{1,2,3}.pdf` | v3: COLM 2026 (ver Seção 2) | sim (v3) |
| Rabanser et al., *Towards a Science of AI Agent Reliability* (2602.16666) | `auditoria-quali/rabanser2026-agent-reliability.pdf` | ICML 2026, PMLR 306 (confirmado nos anais em 24/11) | sim |
| Raj et al., *Consistency as a Testable Property* (2605.10516) | `auditoria-quali/raj2026-consistency-testable.pdf` | NeurIPS 2026, pôster (confirmado em 24/11) | sim |
| Potamitis et al., *ReasonBENCH* (2512.07795) | `auditoria-quali/potamitis2025-reasonbench.pdf` | preprint | não |
| Yagubyan, *How Consistent Are LLM Agents?* (2605.28840) | `auditoria-quali/yagubyan2026-how-consistent.pdf` | preprint, autor único | não |
| Lunardi et al., *On Robustness and Reliability of Benchmark-Based Evaluation of LLMs* (2509.04013) | `auditoria-quali/lunardi2025-robustness-benchmarks.pdf` | ECAI 2025 | sim |
| Mitra, *Spark-LLM-Eval* (2603.28769) | `auditoria-quali/mitra2026-spark-llm-eval.pdf` | preprint, autor único | não |
| Miller, *Adding Error Bars to Evals* (2411.00640) | `auditoria-quali/miller2024-error-bars.pdf` | preprint (Anthropic), autor único | não |
| Debenedetti et al., *AgentDojo* (2406.13352) | `auditoria-quali/agentdojo.pdf` | NeurIPS 2024, Datasets and Benchmarks | sim |
| Zhang et al., *Agent Security Bench (ASB)* (2410.02644) | `auditoria-quali/asb.pdf` | ICLR 2025 | sim |
| Zhang et al., *Agent-SafetyBench* (2412.14470) | `auditoria-quali/zhang2024-agent-safetybench.pdf` | preprint | não |
| Kavathekar et al., *TAMAS* (2511.05269) | `auditoria-quali/tamas.pdf` | ICML 2025, workshop MAS | parcial (workshop) |
| Venkatesh et al., *CASPIAN* (2605.19240) | `auditoria-quali/venkatesh2026-caspian.pdf` | preprint | não |
| Mohammadi et al., *Evaluation and Benchmarking of LLM Agents: A Survey* (2507.21504) | `auditoria-quali/mohammadi2025-agent-eval-survey.pdf` | a revisão sistemática diz "KDD 2025"; ver Seção 2 | a confirmar |
| Xie et al., detecção de cliente adversarial por monitoramento em aprendizado federado (2310.01537) | `auditoria-quali/xie2023-federated-spc.pdf` | preprint | não |
| Jia et al., ataques a detectores de anomalia em sistemas ciberfísicos (2105.10707) | `auditoria-quali/jia2021-cps-cusum.pdf` | Int. J. Critical Infrastructure Protection, 2021 | sim (periódico) |
| Shayegani et al., *Survey of Vulnerabilities in LLMs Revealed by Adversarial Attacks* (2310.10844) | `shayegani2023-survey-adversarial.pdf` | preprint | não |
| Dong et al., *Building Guardrails for Large Language Models* (2402.01822) | `dong2024-guardrails.pdf` | ICML 2024 (PMLR 235) | sim |
| Wang et al., survey de alinhamento (2407.16216) | `wang2024-survey-alignment.pdf` | preprint | não |

Observações:

- **O Li et al., âncora da lacuna, é preprint.** Já se sabia; agora está registrado. Ele não pode ser
  a única sustentação da lacuna (furo F2 do mapa).
- **Dois concorrentes da lacuna passaram por revisão por pares** (Rabanser, ICML 2026; Raj, se o
  "NeurIPS 2026" do comentário indicar aceite). Isso é bom para citar (são fortes) e exige diferenciação cuidadosa: são
  os que a banca mais provavelmente conhece.
- **O survey de alinhamento mudou de título.** O PDF em `papers/` é a v1 (*A Comprehensive Survey of
  LLM Alignment Techniques: RLHF, RLAIF, PPO, DPO and More*); a versão atual no arXiv (v4) se chama
  *Reinforcement Learning for LLM Post-Training: A Survey*, com 12 autores. Citar a versão usada, com
  o número da versão.
- **O "trabalho da Frontiers (2026)"** do `NOVIDADE_E_POSICIONAMENTO.md` 4.2 não tem título, autores
  nem identificador. Não dá para conferir; sai do texto até ser localizado.

---

## 2. O que cada referência diz, conferido no original

Leitura feita em três grupos, cada um por um subagente, com citação literal e página; as citações
marcadas com (✓) foram conferidas de novo no PDF por amostragem. Páginas são as do PDF.

### 2.1 Concorrentes da lacuna de robustez (C4 do mapa)

| Referência e afirmação de agosto | Veredito | Evidência |
|---|---|---|
| **Rabanser et al. (Princeton, ICML 2026)**: confiabilidade em consistência, robustez, previsibilidade e segurança; 12 métricas de engenharia de segurança crítica | **confirmado** | "four key dimensions: consistency, robustness, predictability, and safety"; "twelve metrics" (p. 1) |
| ... avalia 14 modelos | **errado**: são 15 | "Evaluating 15 models across two complementary benchmarks" (p. 1) (✓) |
| ... agente único e não adversarial | **confirmado, e mais forte do que se dizia** | "We do not evaluate adversarial attacks or broader socio-technical concepts like value alignment" (p. 2) (✓); usa K = 5 execuções e paráfrases (p. 5); deixa "Robustness to [...] Adversaries" (E.3) e "Multi-Agent Reliability" (E.4) como **problemas abertos** (p. 24-25) |
| **Raj et al. (NeurIPS 2026)**: estatísticas U; consistência observável (saída) × interna (trajetória) | **confirmado** | "leveraging U-statistics for output-level reliability" (p. 1); "decomposes consistency into observable and internal dimensions" (p. 3). Rodapé "40th Conference on Neural Information Processing Systems (NeurIPS 2026)" (p. 1) (✓), formato de versão final; conferir na lista de aceitos antes de citar como publicado |
| ... adversarial? multiagente? | **parcial / não** | tem uma perturbação "injection" ("Adversarial preamble prepended to the task description", p. 23), mas é ruído ("system log follows >>> https://irrelevant.site", p. 25) e mede sucesso na tarefa, não segurança; agente único |
| **ReasonBench**: repete cada configuração e reporta IC; "a melhor estratégia vence só 77%" | **confirmado** | "We repeat each configuration 30 times and report stratified-bootstrap confidence intervals" (p. 3); "wins only 77% of head-to-head runs against its nearest competitor" (p. 1); estratégias de raciocínio, sem ataque nem multiagente |
| **Yagubyan**: 1.140 traços; consistência estrutural × paramétrica; IC de 95% | **confirmado** | "across 1,140 total agent traces" (p. 1); sem ataque e sem multiagente, só invocações idênticas repetidas |
| **Lunardi et al.**: paráfrase das perguntas de 6 benchmarks, 34 LLMs; ranking estável, queda absoluta | **confirmado** | "rankings remain relatively stable [...] absolute effectiveness scores change, and decline significantly" (p. 1). ECAI 2025 só pelo comentário do arXiv (o PDF não traz); perguntas e respostas, sem agentes |
| **Mohammadi et al.**: agentes são não determinísticos e exigem consistência entre execuções, "mas a área raramente mede" | **parcial**: a segunda metade não está lá | "they must demonstrate consistent performance across repeated runs" (p. 4); diz que medir é caro e que "Some efforts have begun to tackle this challenge" (p. 8). Publicação **confirmada**: KDD '25, doi 10.1145/3711896.3736570 (p. 1) |

**Leitura: nenhum dos seis ocupa a interseção** (segurança sob ataque × multiagente × repetição ou
paráfrase). Todos fazem a metade metodológica (repetir, parafrasear, IC) sem ataque, ou a metade
adversarial sem estabilidade. O achado mais útil para a quali: **o concorrente mais forte (Rabanser,
ICML 2026) exclui ataques por escrito e lista robustez a adversários e confiabilidade multiagente
como problemas abertos.** É uma frase de terceiro, revisada por pares, que sustenta a lacuna junto
com o Li et al. (preprint), e responde em parte ao furo F2 do mapa.

Correções a fazer no `NOVIDADE_E_POSICIONAMENTO.md`: 15 modelos (não 14); a frase do Mohammadi sobre
"raramente mede" sai.

Pistas para a etapa 3 (citadas nesses PDFs, não lidas): *Can we trust AI agents? An experimental
study towards trustworthy LLM-based multi-agent systems for AI ethics* (arXiv:2411.08881); Bogavelli
et al. 2026, robustez a perturbações entre formatos e línguas (arXiv:2601.06341); *The attacker moves
second* (arXiv:2510.09023); ataques adaptativos contra defesas de injeção indireta (arXiv:2503.00061).

### 2.2 Estatística na avaliação e precedentes de controle estatístico (C5 do mapa)

| Afirmação de agosto | Veredito | Evidência |
|---|---|---|
| Spark-LLM-Eval põe IC por bootstrap e teste de significância em toda métrica | **confirmado** | "every reported metric includes bootstrap confidence intervals, and model comparisons come with appropriate significance tests (paired t-tests, McNemar's test, or Wilcoxon signed-rank [...])" (p. 1) |
| ... e diz que "a maioria dos frameworks entrega estimativas pontuais e considera o trabalho concluído" | **parcial**: a frase não existe | o texto é "many evaluation frameworks report only point estimates" (p. 3) (✓). Citar esta, não a de agosto |
| ... e não trata de agentes, ataques, cartas ou fatorial | **confirmado** | agentes só como trabalho futuro (p. 13) |
| Miller: "avaliações são experimentos" e a literatura ignorou a análise experimental | **confirmado** | "evaluations are experiments; but the literature on evaluations has largely ignored the literature from other sciences on experiment analysis and planning" (p. 1) (✓) |
| Miller recomenda... | recomenda erro padrão pelo TLC, **erro padrão agrupado**, **reamostrar respostas** (cada pergunta K vezes), diferenças pareadas e análise de poder (p. 2, 5); **nada** de cartas de controle, SPC ou fatorial | útil para o método: o erro padrão agrupado é uma resposta parcial à objeção de independência (C15) |
| Xie et al.: CUSUM em aprendizado federado, citando Montgomery | **confirmado** | CUSUM não paramétrico (p. 11); cita o ISQC de Montgomery (2020) (p. 23). Detecção de ataque, não avaliação; não é LLM |
| Jia et al.: CUSUM com limites de controle em sistemas ciberfísicos | **confirmado, com ressalva** | limites UCL/LCL (p. 6), mas o CUSUM é o detector que o artigo **ataca**, vindo de trabalho anterior; não é a contribuição deles |
| CASPIAN (multiagente, adversarial) | não usa controle estatístico | monitoramento por turno com regra espectral determinística (p. 6); IC por bootstrap sobre os traços (p. 9); sem repetição nem paráfrase. Mede a qualidade de um **detector** de cascata, não a estabilidade do ASR |

**Busca de termos nos 18 PDFs:** "Shewhart", "Western Electric", "factorial design" e "design of
experiments" têm **zero** ocorrências. Usos reais de SPC/CUSUM só em Xie e Jia (fora de LLM). Dois
vizinhos:

- **Rabanser et al. (ICML 2026)** cita controle estatístico de processo só como analogia de motivação:
  "Industrial process control relies on consistent control loop responses, often monitored via
  statistical process control techniques" (p. 21) (✓). **Isso pesa a favor**: o concorrente mais forte
  conhece a analogia e não a aplicou.
- **Yagubyan (2026)** usa ANOVA de um fator com η² para comparar modelos na reprodutibilidade de
  agentes com ferramentas (p. 5); sem segurança, sem fatorial, sem cartas.

**Leitura:** a afirmação (1) de agosto, "IC e teste já são correntes", vale em parte; o próprio Miller
diz que "error bars remain noticeably absent" (p. 1). A afirmação (2), "ninguém aplicou cartas de
controle ou fatorial à avaliação de segurança de agentes", **não é contradita por nenhum dos 18**, mas
18 PDFs escolhidos por uma pesquisa anterior não são uma busca: a confirmação fica para a etapa 3. Isso
conta para a condição 1 de promoção da Seção 8 do mapa, ainda não para cumpri-la.

Pistas para a etapa 3 (citadas nesses PDFs, não lidas): Madaan et al. 2024, *Quantifying Variance in
Evaluation Benchmarks* (arXiv:2406.10229); Blackwell, Barry e Cohn 2024, *Towards reproducible LLM
evaluation: Quantifying uncertainty in LLM benchmark scores* (arXiv:2410.03492); Biderman et al. 2024,
*Lessons from the trenches on reproducible evaluation of language models* (arXiv:2405.14782).

### 2.3 Medidas de utilidade sob ataque e execuções por caso (C1, C9 a C11 do mapa)

**BAD-ACTS (as três versões).**

| Afirmação | Veredito | Evidência |
|---|---|---|
| v3 publicada no COLM 2026; v1 e v2 só arXiv | **confirmado** | "Published as a conference paper at COLM 2026" (v3, p. 1); a v3 muda o título para "...Adversarially-Induced Harmful Behaviors" |
| v3 mede a qualidade do plano com juiz LLM de 1 a 5, sem adversário, sem validação humana | **confirmado** | "quality of a plan across 500 episodes per environment with no adversarial presence using an LLM-Judge [...] (average quality=3.56/5)" (§4.2, p. 9); nenhuma comparação com humano para esse juiz; v1 e v2 não têm medida de qualidade |
| rejeitou juiz LLM para o ataque: 80% contra 98% das palavras-chave | **confirmado** | "98% agreement with the human evaluation across 100 randomly sampled trajectories of the keyword-based evaluation compared to the 80% agreement of the LLM-judge" (§3.3, p. 7) |
| **o BAD-ACTS reporta ASR de uma execução** | **ERRADO** | "repeat each experiment three times with distinct seeds, and report the mean and standard error" (nas **três versões**) (✓). Tabelas 13 e 14 da v3 (p. 56-57) trazem o erro padrão; não há intervalo de confiança nem análise por caso |
| números do BAD-ACTS como o Li et al. resume (188 ações, 17 categorias, 5 sistemas, 8 LLMs, ASR de 3% a 53%) | **parcial / contradito** | batem com a **v2**, não com a v3; e os "53% (Llama-3.1-8B)" do Li et al. **não existem**: na v2 o Llama-8B tem 0,393 no geral; perto de 53% estão GPT-4.1 (0,527) e Llama-70B (0,523). A v3 tem 238 ações (937 no conjunto estendido) e ASR entre 40% e 90% |

Consequências: **(1)** nunca citar números do BAD-ACTS pelo resumo do Li et al.; citar o próprio
BAD-ACTS, v3, com a versão. **(2)** A afirmação C1 tem de mudar no caso do BAD-ACTS: ele repete três
vezes e reporta média e erro padrão **do ASR agregado**. O que ele não faz, e o trabalho faz, é olhar
**se a conclusão de cada caso muda** entre repetições (taxa de troca, estabilidade do quadrante),
reescrever o pedido ou o ataque, e separar ruído de efeito. O Li et al. classifica o BAD-ACTS como
cobertura **parcial** de R10, o que é coerente com isso. O `CLAUDE.md` e a introdução de julho falam
em "ASR único": corrigir.

**TAMAS** (preprint no PDF; o comentário do arXiv diz workshop MAS do ICML 2025).

- O Effective Robustness Score é a média harmônica de segurança e PNA: ERS = 2·Seg·PNA / (Seg + PNA)
  (Ap. C.4, p. 18).
- **A PNA é medida sem ataque**: "the system's ability to correctly invoke the tools required to
  complete benign user instructions in the absence of any attack" (Ap. C.2, p. 17) (✓). É
  casamento de chamadas de ferramenta, sem validação humana.
- Quem é validado é o juiz de **segurança** (GPT-4o): F1 médio de 89,17% em 140 registros rotulados por
  humanos (p. 17).
- Não declara repetições por caso. Reporta IC por bootstrap entre domínios (D.3, p. 18).

**AgentDojo** (NeurIPS 2024, Datasets and Benchmarks).

- Mede utilidade sob ataque de fato: "the fraction of security cases [...] where the agent solves the
  user task correctly, without any adversarial side effects" (§3.4, p. 6).
- A verificação é uma "deterministic binary function" sobre o estado do ambiente antes e depois
  (p. 4). O artigo rejeita o juiz LLM porque o ataque poderia "hijack the evaluation model" (p. 4).
  **Esse é um argumento a enfrentar no desenho da medida híbrida**: o juiz lê episódios com ataque
  (o teste de injeção do `MEDIDA_UTILIDADE_HIBRIDA.md` responde a isso).
- IC binomial sobre os casos (p. 15, 20). Não declara repetições.

**ASB** (ICLR 2025).

- A PNA é a tarefa completa **sem ataque nem defesa** (Tab. 4, p. 8).
- NRP = PNA × (1 − ASR): combina utilidade sem ataque com o ASR, sem medir a utilidade sob ataque
  diretamente. Tudo é verificado por chamada de ferramenta.
- Não declara repetições.

**Agent-SafetyBench** (preprint).

- A segurança é julgada por um Qwen-2.5-7B ajustado com 4.000 rótulos humanos, com 91,5% de acurácia
  em 200 interações de outro modelo (§3.3, p. 6).
- A utilidade ("helpfulness") é julgada pelo GPT-4o, com "94% accuracy based on manual validation",
  sem o n (§4.4, p. 8).
- Agente único, sem ataque explícito; temperatura 0, provavelmente uma execução por caso.

**Síntese dos cinco:**

| Benchmark | Multiagente | Adversarial | Utilidade **sob ataque** | Como confere | Entrega aberta | Utilidade validada contra humano | Execuções por caso |
|---|---|---|---|---|---|---|---|
| BAD-ACTS v3 | sim | sim | não (só sem adversário) | juiz LLM, 1 a 5 | sim | não | 3, com erro padrão |
| TAMAS | sim | sim | não (PNA sem ataque) | chamada de ferramenta | não | não | não declara |
| AgentDojo | não | sim | **sim** | estado do ambiente | não | não se aplica | não declara |
| ASB | não | sim | indireta (NRP) | chamada de ferramenta | não | não | não declara |
| Agent-SafetyBench | não | parcial | não | juiz GPT-4o | parcial | 94%, n não informado | 1 (provável) |

**Leitura: o recorte estreito da medida (C11 do mapa) continua de pé nesta amostra.** Nenhum dos
cinco junta entrega aberta, multiagente, utilidade medida sob ataque e validação cega contra humano em
conjunto guardado. O mais próximo é o próprio BAD-ACTS v3 (entrega aberta, multiagente, juiz LLM),
mas só sem adversário e sem validação. O AgentDojo é o único que mede utilidade sob ataque, em agente
único e pelo estado do ambiente, que é justamente o que uma entrega aberta não permite. Essa frase,
com as citações acima, é a base do parágrafo de relacionados da medida.

---

## 3. A revisão sistemática não cobre o tema de hoje

A extração de junho tem 20 artigos. Classificados pelo que o trabalho atual precisa:

| Grupo | Artigos | Uso na quali |
|---|---|---|
| Benchmarks de segurança de agente único | E01 AgentDojo, E02 InjecAgent, E03 ASB, E04 AgentHarm, E05 AgentPoison, E06 WASP, E07 ATBench, E08 injeção indireta (KDD 2025), E09 backdoor (NeurIPS 2024), E18 CVE-Bench | relacionados (segurança de agentes, ASR, utilidade sob ataque) |
| Surveys de agentes | E19 avaliação de agentes (Mohammadi), E20 agentes confiáveis | relacionados (panorama) |
| Fundamentos de LLM (alinhamento, guardrails, vulnerabilidades) | E11 Shayegani, E12 Dong, E13 Wang, E14 Bai et al. 2022 (RLHF), E15 Constitutional AI | capítulo de conceitos |
| Defesa e governança | E16 SecureGov-Agent, E17 AgentSentinel | relacionados, periférico |
| Método de avaliação | E10 raciocínio e ação em agentes (2023) | periférico |

**O que falta na revisão, e é o centro do trabalho atual:**

1. **Nenhum benchmark multiagente.** O BAD-ACTS, o TAMAS, o SafeAgents/DHARMA e os outros 6 do grupo
   R5 do Li et al. (PsySafe, AgentLeak, MultiAgentFraudBench, ColludeBench, Colosseum, MAGPIE) não
   estão entre os 20. A monografia de julho os cita fora da revisão.
2. **Nenhum trabalho de consistência ou robustez sob repetição** (Rabanser, Raj, ReasonBench,
   Yagubyan, Lunardi), que são os concorrentes diretos da pergunta escolhida (enquadramento A).
3. **Nenhum trabalho de estatística aplicada à avaliação** (Miller, Spark-LLM-Eval).
4. **Nenhum trabalho de validação de medida contra humano ou de juiz LLM** (os 36 da
   `pesquisa-juiz-llm/SINTESE.md` e os da `pesquisa-avaliacao-hibrida/SINTESE.md` estão fora).

Isso não invalida a revisão: ela foi feita em junho, para outra pergunta (mapear benchmarks de
segurança). Mas, como está, **ela não sustenta a lacuna da pergunta de hoje**. Duas saídas, para o
autor e a orientadora decidirem:

- **(a) estender a revisão** com uma segunda rodada de busca, com as strings da pergunta nova
  (multiagente, consistência, repetição, paráfrase, utilidade sob ataque), no mesmo protocolo. Dá à
  quali um capítulo de relacionados com método declarado. Custo: refazer busca, triagem e extração.
- **(b) manter a revisão como está** (relacionados de segurança de agentes em geral) e tratar o resto
  como **revisão narrativa dirigida**, declarada como tal, com as referências conferidas nesta
  auditoria e na etapa 3.

A etapa 3 (busca adversarial) produz de qualquer modo a lista de candidatos que a saída (a) usaria.

---

## 4. Pendências desta etapa

- Registrar cada referência conferida no `docs/refs/REGISTRO_REFERENCIAS.md` (que hoje diz
  "Pendente" para o BAD-ACTS e o Li et al.).
- Pista nova para a etapa 3: *ReliabilityBench: Evaluating LLM Agent Reliability Under Production-Like Stress Conditions* (arXiv 2601.06112), apareceu na busca de 24/11.
- Correções a propagar: `NOVIDADE_E_POSICIONAMENTO.md` (15 modelos no Rabanser; frase do Mohammadi;
  frase do Spark-LLM-Eval; "trabalho da Frontiers" sem referência; TAMAS como concorrente da medida);
  `CLAUDE.md` e textos que dizem que o BAD-ACTS reporta "um ASR" (ele repete 3 vezes); linhas C1, C4,
  C5, C9 e C11 do `MAPA_DE_REIVINDICACOES.md`.
- A revisão sistemática não cobre o tema de hoje (Seção 3): decisão (a) estender ou (b) narrativa,
  para a reunião 8.
- As pistas das Seções 2.1 e 2.2 alimentam os prompts da etapa 3.

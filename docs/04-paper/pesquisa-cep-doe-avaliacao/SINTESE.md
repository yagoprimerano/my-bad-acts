# Síntese: controle estatístico e delineamento de experimentos na avaliação de LLM (pesquisa 3 da etapa 3)

Pesquisa disparada em 24/11/2026 com o `PROMPT.md` desta pasta: (a) procurar quem já aplicou cartas
de controle ou fatorial à avaliação de LLM ou de agentes (linhas C5 e C15 do
`06-qualificacao/MAPA_DE_REIVINDICACOES.md`); (b) trazer a literatura estatística sobre a objeção de
independência. Entradas brutas: `chatgpt_deep_research_2026-11-24.md` e
`claude_research_2026-11-24.md`.

**Esta síntese é o único arquivo citável da pasta.** Cada trabalho abaixo foi aberto em 24/11/2026:
metadados pelo arXiv, Crossref, PubMed ou OpenReview; local na página dos anais (PMLR, ACL Anthology,
pôster do NeurIPS ou do ICLR), nunca pelo comentário do arXiv; números e frases no PDF. Os periódicos
de estatística pagos (Wiley, Taylor & Francis) devolveram 403: para eles, só metadados e resumo, marcados
"texto não aberto". Os PDFs estão em `docs/refs/auditoria-quali/` (fora do git). Nenhuma referência
com identificador era inventada. As seções e páginas do Montgomery citadas pelos relatórios conferem
com a `06-qualificacao/REVISAO_METODOLOGICA.md`, Seção 8.

---

## 1. Resultado

| Ideia do método | Precedente? | O mais próximo | O que continua nosso |
|---|---|---|---|
| **Cartas de controle na avaliação experimental de segurança de agentes** | **não encontrado** | Helm, Priebe, Duderstadt, "Control Charts for Multi-Agent Systems", **NeurIPS 2026** (pôster; OpenReview e rodapé da v2), que é **monitoramento**: cartas de Shewhart sobre um resumo de embeddings das respostas, não sobre taxa de sucesso de ataque | carta sobre o veredito de ataque por caso, como diagnóstico de Fase I e controle da ordem de execução (`REVISAO_METODOLOGICA.md` 1.4) |
| **Fatorial e ANOVA na avaliação de LLM** | **sim, revisado** | Tian et al., ICML 2026 (PMLR 306:120838-120872): ANOVA sobre um 2^10, citando o Montgomery; Luo et al., EMNLP 2026 (pp. 26314-26338): fatorial registro × estrutura em **jailbreak**; CAFE, EMNLP 2026 Demos | **fatorial de defesa × perturbação em sistema multiagente sob ataque**: não encontrado |
| **Decomposição de variância com item, variante de prompt e réplica aleatórios** (a leitura "R&R" da `REVISAO_METODOLOGICA.md` 1.5) | **sim, revisado** | Messing, "Hidden Measurement Error in LLM Pipelines Distorts Annotation, Evaluation, and Benchmarking", **NeurIPS 2026** (pôster), modelo misto com essas três facetas cruzadas, por REML, com aplicação de segurança (AILuminate) | resposta binária de sucesso de ataque num multiagente com adversário interno; paráfrase do **ataque** ao lado da tarefa; interesse no caso, não só na média; o vocabulário do estudo R&R do ISQC 8.7 |

**Consequência para o mapa:** a leitura de componentes de variância **não é novidade de método**. Ela
fica como o método certo para responder à QA1, citando o Messing como precedente. A Seção 8 do mapa
(o que promoveria a contribuição de método de volta) perde o candidato que a etapa 4 tinha proposto:
a contribuição de método fica **rebaixada de vez**, e o que há de novo é a aplicação ao recorte
(multiagente, adversário interno, B1 e B2, veredito por caso).

**Frases para o texto:**

- "Não encontramos, até 24/11/2026, uso de cartas de controle na avaliação experimental de segurança
  de agentes; o trabalho mais próximo usa cartas adaptativas para monitorar sistemas multiagentes
  (Helm et al., 2026)."
- "Delineamentos fatoriais já foram aplicados à avaliação de LLM (Tian et al., 2026) e a jailbreak
  (Luo et al., 2026); não encontramos fatorial de defesa × perturbação em sistema multiagente sob
  ataque."
- "Seguimos a decomposição de variância de Messing (2026), adaptada à resposta binária de um sistema
  multiagente sob ataque."

---

## 2. Os três trabalhos que o texto tem de citar

**Messing (arXiv 2604.11581, aceito no NeurIPS 2026, conferência principal; citar a v8 ou a dos
anais).**

- **O que decompõe:** a variância do escore de um "pipeline" de avaliação, num modelo linear misto:
  item, variante de prompt e réplica aleatórios, temperatura e modelo fixos, interações de segunda
  ordem, por REML (Seção 3.1 e 3.3). "Replications are repeated model calls".
- **Números conferidos na v8:**
  - "naive standard errors are 53 - 70% smaller than the corrected SE" (resumo);
  - no AILuminate, "The 3-judge panel contributes 43.8% of the variance with item×judge adding another
    16.7%. On the other hand, prompt wording contributes less than 0.5%" (Seção 3);
  - "Readers should treat rerun-only intervals as lower bounds on the uncertainty" (Seção 5).
  Na v1, o "53 - 70%" não existe e as porcentagens são outras.
- **O que não faz:**
  - não usa "gauge R&R" nem "measurement system analysis" (usa teoria da generalizabilidade);
  - não tem ataque nem multiagente (agente só na reanálise do Terminal-Bench, onde o "harness" conta
    como variante de prompt, Seção 3.1);
  - no AILuminate quem varia é o **juiz**, com as respostas fixas; no BAD-ACTS o veredito é
    determinístico e quem varia é o próprio sistema avaliado.
- **Um achado que temos de enfrentar:** nas aplicações dele, o ruído de réplica fica abaixo de 0,5% da
  variância da média, e o autor conclui que "temperature and further replications were much less
  important" (3.3). Isso vai contra a premissa da dissertação de que a repetição importa. A diferença
  de objeto (juiz variando sobre respostas fixas × sistema estocástico variando sobre casos fixos)
  explica a divergência só em parte. O piloto (caso 0 do B2 oscilando, caso 3 no teto) e a triagem
  dão a primeira resposta empírica. **Escrever essa discussão no capítulo de método.**

**Helm, Priebe, Duderstadt (arXiv 2605.11135, aceito no NeurIPS 2026, conferência principal; citar a
v2).**

- **O que faz:**
  - "we extend the process-theoretic notion of adaptive control charts to multi-agent systems to
    enable automated monitoring" (resumo);
  - Shewhart sobre a trajetória do "iso-mirror" (3.3);
  - agentes adversários que defeccionam devagar escapam: "monitors with fixed baselines flag legitimate
    learning, while monitors with adaptive baselines admit slow adversaries. We conjecture this holds
    for any monitor" (resumo); o mesmo vale para o CUSUM (5.1, só na v2).
- **O que não faz:** carta sobre taxa de sucesso de ataque; avaliação experimental com réplicas; LLM
  real nas réplicas ("we replace the LLM call with the proxy function", nota 3).
- **O argumento que ele dá ao nosso desenho:** num benchmark o sistema não deve aprender entre
  execuções, então limites **fixos** (Fase I) são os certos, e uma mudança é sinal, não deriva
  legítima. Isso sustenta a resposta à objeção (b) da `REVISAO_METODOLOGICA.md` 1.2.

**Luo et al., "Voices Across Registers" (EMNLP 2026, DOI 10.18653/2026.emnlp-main.1148).** É o
precedente revisado de fatorial em segurança: "a factorial decomposition shows the gain is carried by
register rather than length or structure" (resumo), com regressão logística GEE agrupada por
comportamento. É LLM isolado, sem agentes. A análise dele (logística com agrupamento) é a que a M4 da
revisão metodológica recomenda para o nosso 2².

---

## 3. A objeção de independência: o que a literatura acrescenta ao Montgomery

A resposta da `REVISAO_METODOLOGICA.md` Seção 1 se sustenta. Os relatórios acrescentam:

- **Casos heterogêneos (a):** cartas ajustadas ao risco.
  - Steiner, Cook, Farewell, Treasure, "Monitoring surgical performance using risk-adjusted
    cumulative sum charts", *Biostatistics* 1(4):441-452, 2000, DOI 10.1093/biostatistics/1.4.441
    (PubMed; texto não aberto): "adjusts for each patient's pre-operative risk [...] ideally suited
    for settings where there is a variable mix of patients over time".
  - Steiner, Cook, Farewell, *Medical Decision Making* 21(3):163-169, 2001, a versão para desfecho
    binário.
  - Revisão: Grigg e Farewell, "An Overview of Risk-Adjusted Charts", *JRSS A* 167(3):523-539, 2004
    (metadados).
- **Proporção perto de 0 (o ASR com defesa ligada):** Szarka e Woodall, "A Review and Perspective on
  Surveillance of Bernoulli Processes", *QREI* 27(6):735-752, 2011, DOI 10.1002/qre.1256 (metadados e
  resumo). No próprio ISQC: 10.11.7, p. 501.
- **Modelo por trás da API (b):** Blackwell, Barry, Cohn (arXiv 2410.03492, preprint): com T = 0 e
  semente fixa, o mesmo GPT-3.5 pela Azure e pela OpenAI deu médias 0,833 e 0,840 (n = 90),
  "statistically significantly different (t = 2.51, p = 0.013)" (Seção 4). É evidência de que o
  provedor muda a distribuição. **Atenção:** o Blackwell **recomenda** T = 0 com semente fixa,
  enquanto o Miller (arXiv 2411.00640, preprint, sem local encontrado) diz o contrário: "we advise
  against this practice, unless the purpose is to study the model at the new temperature" (3.3). A
  dissertação segue o Miller, porque a estocasticidade é o objeto; dizer isso e citar os dois.
- **Dependência na trajetória (c):** Yagubyan (arXiv 2605.28840, preprint): "60 % of first-divergence
  events occur within the first two pipeline steps" (5.3). São eventos de divergência, não fração da
  variância (o próprio autor se contradiz no "Finding 3"). Serve para dizer que a trajetória herda o
  começo, o que reforça usar o episódio como unidade.
- **Controvérsias:** Woodall, "Controversies and Contradictions in Statistical Process Control",
  *JQT* 32(4):341-350, 2000 (metadados). A frase sobre a carta de amplitude móvel ser "ineffective",
  atribuída pelo relatório do Claude, **não foi conferida** (veio de trecho do ResearchGate, sem
  contexto). Não citar sem abrir o artigo.

Contra o uso de cartas em ML não há trabalho dedicado. O mais forte é o Helm (limites adaptativos
absorvem adversários lentos), que, como visto, apoia os limites fixos num benchmark.

---

## 4. Variação entre execuções como objeto (P3)

- **Messing**, acima, é o central.
- **ReasonBench** (Potamitis et al., arXiv 2512.07795; workshop P-AGI do ICLR 2026, conferido no
  OpenReview; os dois relatórios e a `AUDITORIA_REFERENCIAS.md` diziam preprint): "30 independent
  trials" e "A hierarchical decomposition attributes three-quarters of score variance to benchmark,
  system, and item structure, with a persistent residual that single-run evaluation silently absorbs"
  (resumo). A decomposição é sequencial, em ordem fixa (4.3).
- **GuidedBench** (arXiv 2502.16903; ICLR 2026 segundo o comentário do arXiv, anais não abertos): modelo
  misto `S ∼ 1 + (1|victim) + (1|topic)` para juízes de jailbreak (Ap. E.2).
- **Broadwater**, "Evaluating Reliability Gaps in Large Language Model Safety via Repeated Prompt
  Sampling" (IEEE CCAI 2026, pp. 930-938): falhas de segurança como Bernoulli e binomial sob
  amostragem repetida, em chat.
- **Madaan et al.** (arXiv 2406.10229; workshop RegML do NeurIPS 2024): a "seed variance" é de semente
  de **treino**, não de inferência (2.1). Pouco útil.
- **Pistas a ler, não abertas** (citadas pelo Messing):
  - Wang, "Measuring all the noises of LLM Evals" (arXiv 2512.21326);
  - Keller et al., NIST AI 800-3, "Expanding the AI evaluation toolbox with statistical models"
    (2026, DOI 10.6028/NIST.AI.800-3): GLMM com componentes entre e dentro de itens. Se confirmado,
    é a referência institucional para a análise da `REVISAO_METODOLOGICA.md` M4 e 1.5.

---

## 5. Correções ao que já estava escrito

| Onde | Estava | Conferido em 24/11 |
|---|---|---|
| `AUDITORIA_REFERENCIAS.md` §1 | Xie et al. (2310.01537): preprint | *IISE Transactions* 57(7):743-755, 2025, DOI 10.1080/24725854.2024.2367224; e usa CUSUM (Seção 3.2) |
| `AUDITORIA_REFERENCIAS.md` §1 | ReasonBench: preprint | workshop P-AGI do ICLR 2026 |
| `REVISAO_METODOLOGICA.md` 1.5 | decomposição R&R "candidato mais forte para a contribuição de método" | tem precedente revisado (Messing, NeurIPS 2026): fica como método, não como contribuição |
| `MAPA_DE_REIVINDICACOES.md` C5 | "ninguém aplicou cartas de controle **e fatorial**" | fatorial em avaliação de LLM já existe (Tian, Luo); a afirmação fica só para cartas na avaliação experimental e para o 2² de defesa × perturbação em multiagente |
| relatório do Claude | Helm e Messing: preprints | os dois aceitos no NeurIPS 2026 (conferência principal) |
| relatório do Claude | o mais próximo em fatorial é o MMJailBench | é o Luo (revisado); o MMJailBench (arXiv 2608.25490, preprint) não tem ANOVA nem repetição |
| relatório do ChatGPT | Bogdanov et al. no ICLR 2026, com Manakina como primeira autora | workshop do ICLR 2026; primeiro autor Bogdanov |

---

## 6. Tabela dos trabalhos conferidos

| Título (curto) | Ano | Identificador | Local (conferido em) | Revisado? | Relevância | Faz / não faz |
|---|---|---|---|---|---|---|
| Hidden Measurement Error in LLM Pipelines (Messing) | 2026 | arXiv 2604.11581 (v8) | NeurIPS 2026 (pôster, rodapé da v8) | sim | alta | componentes de variância item × variante × réplica; sem ataque, sem multiagente |
| Control Charts for Multi-Agent Systems (Helm et al.) | 2026 | arXiv 2605.11135 (v2) | NeurIPS 2026 (pôster, OpenReview) | sim | alta | cartas para monitorar multiagente com adversário; não é avaliação experimental |
| Voices Across Registers (Luo et al.) | 2026 | 10.18653/2026.emnlp-main.1148 | EMNLP 2026 (Anthology) | sim | alta | fatorial em jailbreak, logística GEE; LLM isolado |
| Beyond Benchmarks: Causally Faithful Evaluation (Tian et al.) | 2026 | PMLR 306:120838-120872 | ICML 2026 (PMLR) | sim | alta | ANOVA sobre 2^10, cita Montgomery; não é segurança |
| CAFE | 2026 | 10.18653/2026.emnlp-demos.50 | EMNLP 2026 Demos (Anthology) | sim (demos) | média | fatorial com efeitos mistos em pipeline RAG |
| Evaluation of Multi-Turn Consistency in LLM Agents (Bogdanov et al.) | 2026 | arXiv 2609.29508 | workshop ICLR 2026 | sim (workshop) | média | fatorial completo, multiagente, sem ataque |
| MMJailBench | 2026 | arXiv 2608.25490 | preprint | não | baixa | 272 × 6 × 5 × 2 sem ANOVA nem repetição |
| ReasonBench | 2026 | arXiv 2512.07795 | workshop P-AGI, ICLR 2026 (OpenReview) | sim (workshop) | média | 30 execuções, decomposição hierárquica |
| GuidedBench | 2025 | arXiv 2502.16903 | ICLR 2026 (não aberto nos anais) | provável | baixa | modelo misto para juízes de jailbreak |
| Evaluating Reliability Gaps... Repeated Prompt Sampling (Broadwater) | 2026 | 10.1109/CCAI69603.2026.11642011 | IEEE CCAI 2026 (Crossref) | sim | baixa | segurança como Bernoulli sob repetição, chat |
| Towards Reproducible LLM Evaluation (Blackwell et al.) | 2024 | arXiv 2410.03492 | preprint | não | média | 1 a 30 repetições; Azure × OpenAI; recomenda T = 0 |
| Adding Error Bars to Evals (Miller) | 2024 | arXiv 2411.00640 | preprint (sem local encontrado) | não | média | erro padrão agrupado; contra baixar a temperatura |
| Quantifying Variance in Evaluation Benchmarks (Madaan et al.) | 2024 | arXiv 2406.10229 | workshop RegML, NeurIPS 2024 | sim (workshop) | baixa | variância de semente de treino |
| How Consistent Are LLM Agents? (Yagubyan) | 2026 | arXiv 2605.28840 | preprint | não | baixa | divergência nos primeiros passos |
| Towards a Science of AI Agent Reliability (Rabanser et al.) | 2026 | PMLR 306:102769-102820 | ICML 2026 | sim | média | SPC só como analogia (Ap. D.2) |
| Designing monitoring strategies for deployed ML (Feng et al.) | 2024 | PMLR 236:587-608 | CLeaR 2024 | sim | baixa | SPC e causalidade no monitoramento de ML implantado |
| Adversarial Client Detection... (Xie et al.) | 2025 | 10.1080/24725854.2024.2367224 | *IISE Transactions* 57(7) (Crossref) | sim | baixa | CUSUM não paramétrico contra clientes adversários, fora de LLM |
| Adversarial Attacks and Mitigation for Anomaly Detectors of CPS (Jia et al.) | 2021 | 10.1016/j.ijcip.2021.100452 | *IJCIP* 34 (Crossref) | sim | baixa | ataque a detector com CUSUM |
| Monitoring surgical performance using risk-adjusted CUSUM (Steiner et al.) | 2000 | 10.1093/biostatistics/1.4.441 | *Biostatistics* 1(4) (PubMed) | sim | média | carta ajustada ao risco; texto não aberto |
| Risk-adjusted monitoring of binary surgical outcomes (Steiner et al.) | 2001 | PMID 11386623 | *Med. Decis. Making* 21(3) (PubMed) | sim | média | idem, desfecho binário; texto não aberto |
| An Overview of Risk-Adjusted Charts (Grigg, Farewell) | 2004 | 10.1111/j.1467-985x.2004.0apm2.x | *JRSS A* 167(3) (Crossref) | sim | média | revisão; texto não aberto |
| A Review and Perspective on Surveillance of Bernoulli Processes (Szarka, Woodall) | 2011 | 10.1002/qre.1256 | *QREI* 27(6) (Crossref) | sim | média | processos de Bernoulli de alta qualidade; texto não aberto |
| Controversies and Contradictions in SPC (Woodall) | 2000 | 10.1080/00224065.2000.11980013 | *JQT* 32(4) (Crossref) | sim | baixa | texto não aberto; frase do MR não conferida |
| The Use of Control Charts in Health-Care... (Woodall) | 2006 | 10.1080/00224065.2006.11918593 | *JQT* 38(2) (Crossref) | sim | baixa | texto não aberto |
| Monitoring univariate processes using control charts (Zwetsloot, Jones-Farmer, Woodall) | 2023 | 10.1080/08982112.2023.2238049 | *Quality Engineering* 36(3) (Crossref) | sim | baixa | Fase I e II; acesso aberto, baixar à mão |
| Time-Series Modeling for SPC (Alwan, Roberts) | 1988 | 10.1080/07350015.1988.10509640 | *JBES* 6(1) (Crossref) | sim | baixa | autocorrelação; texto não aberto |

Não conferido: texto integral dos artigos de periódico de estatística; anais do NeurIPS 2026 (o
congresso é em dezembro; conferidos a página do pôster e o rodapé do PDF); versão IISE do Xie; o
apêndice suplementar do Messing; uma afirmação do relatório do ChatGPT sobre monitoramento em medicina
sem obra identificável (não citável). O Żatuchin (arXiv 2607.13304) mudou de título e retirou
afirmações na v2: não citar.

---

## 7. O que muda na dissertação

1. **C5** encolhe: "não encontramos cartas de controle na avaliação experimental de segurança de
   agentes, nem fatorial de defesa × perturbação em multiagente sob ataque". Fatorial e ANOVA em
   avaliação de LLM não são novos.
2. **A contribuição de método fica rebaixada de vez** (Seção 8 do mapa). As três condições para
   promovê-la falham ou ficam fracas: há precedente para a decomposição (Messing), as cartas têm
   pouco poder com os tamanhos do plano (`REVISAO_METODOLOGICA.md` 1.1), e o fatorial tem precedente
   em jailbreak.
3. **O método fica mais defensável**, porque cada peça agora tem referência revisada: a decomposição
   (Messing), a logística com agrupamento (Luo), os limites fixos (Helm), as cartas ajustadas ao risco
   (Steiner).
4. **O achado do Messing sobre réplicas (< 0,5%)** tem de ser discutido no capítulo de método; é a
   objeção mais forte à premissa "repetir importa", e o definitivo é o que a responde.
5. **Temperatura:** seguir o Miller e declarar o Blackwell como posição contrária (`REVISAO_METODOLOGICA.md` M9).
6. Ler na íntegra antes da quali: Messing, Helm e Luo; tentar o NIST AI 800-3.

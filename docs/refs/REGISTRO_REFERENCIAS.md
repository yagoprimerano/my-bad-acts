# Registro de referências

Uma entrada por artigo ou livro usado como referência no trabalho. Os arquivos (PDF, epub) ficam em
`docs/refs/` e são gitignored; **este registro é versionado** e é a matéria-prima da seção de
trabalhos relacionados do paper e da dissertação.

Cada entrada diz quando a referência foi útil e por quê. Uma referência usada em mais de um momento
ganha uma linha nova em "Quando foi útil", não uma entrada nova.

## Formato

```
### <Autores, ano>. <Título>
- Identificador: arXiv / DOI / ISBN / link
- Publicação: local (conferência, periódico, workshop) e se passou por revisão por pares, ou "preprint"
- Arquivo local: docs/refs/<nome> (ou "não baixado")
- Conferido no original: sim (data) / não (só resumo, só relatório de pesquisa)
- Quando foi útil:
  - <AAAA-MM-DD>: <para que decisão ou texto>, em <arquivo do repositório, seção>
- Por que importa: <uma ou duas frases>
- Para o paper: trabalhos relacionados / método / ameaça à validade / comparação; <onde entra>
```

## Pendente

Feito em 24/11/2026: as obras das três sínteses da etapa 3 e as da `pesquisa-avaliacao-hibrida/SINTESE.md`
ganharam entrada (seções "Etapa 3 da auditoria" e "Avaliação híbrida"); a lista completa das obras,
com arquivo local, URL e onde cada uma é citada, está em `MANIFESTO.csv` (recriar a pasta com
`python scripts/fetch_refs.py`). Continua pendente:

- o campo "Publicação" nas entradas de antes de 24/11 (livros, artigos de estatística, pesquisa do
  juiz) e, na seção "Avaliação híbrida", conferir o local nos anais (veio do cabeçalho do PDF);
- **baixar à mão** o Zwetsloot et al. (2023), de acesso aberto mas bloqueado ao download automático
  (403 da Taylor & Francis). O Khan et al. (2026) já está na pasta (PDF da MDPI), mas a MDPI também
  bloqueia o download automático: numa máquina nova, baixá-lo à mão;
- ler antes de citar: o NIST AI 800-3 (componentes entre e dentro de itens), o Wang (2025) e o Larsen
  (2025), hoje conferidos só no resumo; o De Mast e Van Wieringen (2007) e os periódicos de
  estatística da etapa 3, que são pagos (obter pela biblioteca da USP, nunca por fonte pirata);
- as pistas não registradas: Biderman et al. (2024), arXiv 2405.14782, citado como pista em
  `06-qualificacao/AUDITORIA_REFERENCIAS.md` 2.2 (PDF já baixado, não lido); AgentBoard (arXiv
  2401.13178), citado nas referências de `MEDIDA_UTILIDADE_HIBRIDA.md` sem conferência na síntese; e a
  pesquisa `pesquisa-amostra-validacao/`, que não tem `SINTESE.md` (dela só a Tabela 3 do
  AgentRewardBench foi conferida, e o Cochran tem entrada própria).

## Livros de estatística

### Montgomery, D. C. (2013). *Design and Analysis of Experiments*, 8ª ed. Wiley.
- Identificador: ISBN 978-1-118-14692-7
- Arquivo local: `docs/refs/Design and Analysis of Experiments, 8th Edition (...).pdf`
- Conferido no original: sim
- Quando foi útil:
  - antes de 28/10/2026: o desenho do `02-experimentos/PLANO_EXPERIMENTAL.md` e dos blocos da
    triagem (fatorial 2², réplica × repetição, paráfrase como fator de ruído); ver `README.md` aqui
  - 2026-10-28: tamanho da reserva de teste (`MEDIDA_UTILIDADE_HIBRIDA.md`, 7.1.1). O livro trata a
    binomial só na transformação arco-seno, sem intervalo para uma proporção; registrado que se usou
    Wilson
  - 2026-10-28: significado dos níveis de precisão e κ (`MEDIDA_UTILIDADE_HIBRIDA.md`, 7.5): Seção 1.4
    (capacidade do sistema de medição no planejamento), Exemplo 13.1 (repetibilidade e
    reprodutibilidade, como analogia), Seções 2.4.1 e 2.4.3 (erros tipo I e II, curva OC)
- Por que importa: autoridade indicada pela orientadora para todo o desenho experimental.
- Para o paper: método (desenho dos experimentos).

### Ramírez, B. S. & Ramírez, J. G. (2018). *Douglas Montgomery's Introduction to Statistical Quality Control: A JMP Companion*. SAS Institute.
- Identificador: ISBN 978-1-63526-022-9
- Arquivo local: `docs/refs/Douglas Montgomery's Introduction to Statistical Quality (...).epub`
- Conferido no original: sim (2026-10-28)
- Quando foi útil:
  - 2026-10-28: descoberto que **não é o ISQC**, e sim um manual de JMP que remete ao ISQC 7ª ed.
    Para citar o ISQC (Montgomery, *Introduction to Statistical Quality Control*) é preciso obter o
    livro; o `README.md` desta pasta o descreve como se fosse o ISQC
- Por que importa: o ISQC é a outra autoridade indicada pela orientadora (cartas de controle e
  repetibilidade em `analyze_experiment_stats.py spc`).
  - 2026-10-28: usado para localizar as seções do ISQC sobre medição por atributo (cap. 5 do
    Companion → ISQC 8.7.5). Depois que o ISQC foi obtido, deixou de ser citado. Imprecisão
    registrada: diz que o κ vai de 0 a 1 (o κ pode ser negativo)
- Para o paper: não citar; citar o ISQC.

### Montgomery, D. C. (2013). *Introduction to Statistical Quality Control*, 7ª ed. Wiley.
- Identificador: ISBN 978-1-118-14681-1 (confere com o metadado do PDF)
- Arquivo local: `docs/refs/montgomery-isqc-7ed.pdf` (774 p., texto extraível com `pdftotext`)
- Conferido no original: sim (2026-10-28)
- Quando foi útil:
  - 2026-10-28: significado dos níveis de precisão e κ (`MEDIDA_UTILIDADE_HIBRIDA.md`, 7.5): 8.7.1
    (objetivo de um estudo do sistema de medição; repetibilidade, reprodutibilidade, viés), 8.7.4
    (risco do produtor δ e do consumidor β), 8.7.5 e Tabelas 8.13/8.14 (medição por atributo:
    avaliação às cegas, padrão por consenso de painel, % de concordância com IC exato, sem κ e sem
    limiar), 4.3.5 (IC para proporção; binomial com n pequeno), 7.2.4 (curva OC pela binomial). A
    conta da Tabela 8.14 foi refeita (Clopper-Pearson, 23 de 30 → 57,72% a 90,07%) e bate
  - 2026-10-28: corrigida a nota da 7.1.1 do mesmo documento, que dizia que os livros não trazem
    intervalo para uma proporção
- Por que importa: a outra autoridade indicada pela orientadora; a Seção 8.7.5 é o desenho mais
  próximo da validação da medida de utilidade (a medida como avaliador, o rótulo humano como padrão).
- Para o paper: método (validação da medida como estudo de capacidade do sistema de medição);
  leitura de controle de processo (`analyze_experiment_stats.py spc`). **Pendente:** conferir as
  citações do ISQC em `docs/03-metricas/METRICAS_ROBUSTEZ.md` (caps. 6 e 7), feitas sem o livro.


### Cochran, W. G. (1977). *Sampling Techniques*, 3ª ed. Wiley.
- Identificador: ISBN 0-471-16240-X
- Arquivo local: `docs/refs/Sampling Techniques.djvu` (tem camada de texto; sem `djvutxt` na
  máquina, o texto foi extraído pela `libdjvulibre` via ctypes)
- Conferido no original: sim (12/11/2026), seções 4.9, 5.3, 5.11, 5A.1, 5A.13 e 12.1 a 12.2
- Quando foi útil:
  - 2026-11-12: igual × proporcional na repartição dos guardados por modelo (reunião 7, slide 25).
    4.9: estimativa por subgrupo exige amostra própria em cada um. 5A.13: quando os estratos são
    domínios de estudo, com custo e variância parecidos, a regra dá o mesmo tamanho a todos. 5A.1:
    o ótimo é "plano" (desvio máximo g aumenta a variância em no máximo g²; aqui g ≈ 20%, aumento
    médio < 1%). 5.3: a média geral se recupera com os pesos dos estratos. 5.11: com proporções
    entre 0,1 e 0,9, ótima e proporcional quase coincidem
  - 2026-11-12: a citação "Neyman (1938); Cochran cap. 12" como precedente da fase 2 foi
    **retirada**: o cap. 12 é amostragem dupla para estratificação (uma primeira amostra barata
    estima o tamanho dos estratos), não um reforço de amostra nos estratos finalistas
- Por que importa: é a autoridade que faltava para alocação de amostra estratificada; os dois livros
  do Montgomery não tratam de proporcional × igual
- Para o paper: método; justificativa da repartição igual dos guardados e da reponderação da média

## Artigos de estatística (concordância e intervalos)

### Cohen, J. (1960). A coefficient of agreement for nominal scales.
- Identificador: *Educational and Psychological Measurement* 20(1), 37-46. DOI 10.1177/001316446002000104
- Arquivo local: não baixado
- Conferido no original: não
- Quando foi útil:
  - 2026-10-28: definição do κ (`MEDIDA_UTILIDADE_HIBRIDA.md`, 7.5), que os livros do Montgomery
    não trazem; já usado antes no `score` do lote 1 (`VALIDACAO_PROXY_UTILIDADE.md`, 7)
- Por que importa: o κ é a medida de concordância de toda a validação (medida × humano, humano × humano).
- Para o paper: método.

### Landis, J. R.; Koch, G. G. (1977). The measurement of observer agreement for categorical data.
- Identificador: *Biometrics* 33(1), 159-174. DOI 10.2307/2529310
- Arquivo local: não baixado
- Conferido no original: não
- Quando foi útil:
  - 2026-10-28: faixas de leitura do κ (quase perfeita, substancial, moderada) na 7.5
- Por que importa: vocabulário comum para o κ; os autores chamam as faixas de arbitrárias, por isso
  não é usado como limiar.
- Para o paper: método.

### Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference.
- Identificador: *Journal of the American Statistical Association* 22(158), 209-212. DOI 10.1080/01621459.1927.10502953
- Arquivo local: não baixado
- Conferido no original: não
- Quando foi útil:
  - 2026-10-28: intervalo principal da 7.1.1 e da 7.5; é o de `wilson_interval` em
    `scripts/analyze_experiment_stats.py`, usado também no `score` do lote 1
- Por que importa: intervalo para proporção com amostras pequenas, usado em toda a validação.
- Para o paper: método.

### Clopper, C. J.; Pearson, E. S. (1934). The use of confidence or fiducial limits illustrated in the case of the binomial.
- Identificador: *Biometrika* 26(4), 404-413. DOI 10.1093/biomet/26.4.404
- Arquivo local: não baixado
- Conferido no original: não
- Quando foi útil:
  - 2026-10-28: intervalo exato reportado ao lado do de Wilson na 7.5, por ser o que o ISQC usa
    (Tabela 8.14) e recomenda para n pequeno (4.3.5)
- Por que importa: liga a validação ao método do ISQC.
- Para o paper: método.

### De Mast, J.; Van Wieringen, W. N. (2007). Measurement system analysis for categorical measurements: agreement and kappa-type indices.
- Identificador: *Journal of Quality Technology* 39(3), 191-202
- Arquivo local: não baixado
- Conferido no original: não (só a citação no ISQC, 8.7.5 e referências)
- Quando foi útil:
  - 2026-10-28: indicado pelo ISQC para índices do tipo kappa em medição categórica; citado na 7.5
    e na pergunta 7 da Seção 9 (outros livros) como candidato a leitura
- Por que importa: é a ponte entre a análise de sistemas de medição do Montgomery e o κ, o ponto que
  os livros não cobrem. **Baixar e ler antes de citar no paper.**
- Para o paper: método, se lido.

## Pesquisa sobre o juiz LLM (conferida em 29/10/2026)

Todas as entradas desta seção foram conferidas no original para
`docs/04-paper/pesquisa-juiz-llm/SINTESE.md` (passo 6 da Seção 10 de `MEDIDA_UTILIDADE_HIBRIDA.md`:
escolher o juiz; slide do juiz da reunião 6). Arquivos em `docs/refs/pesquisa-juiz-llm/<arXiv>.pdf`.
As que decidem a recomendação têm entrada completa; as demais estão na tabela do fim da seção.

### Dziemian et al. (2026). How Vulnerable Are AI Agents to Indirect Prompt Injections? Insights from a Large-Scale Public Competition.
- Identificador: arXiv 2603.15714
- Arquivo local: `docs/refs/pesquisa-juiz-llm/2603.15714.pdf`
- Conferido no original: sim (2026-10-29)
- Quando foi útil:
  - 2026-10-29: comparação de robustez a injeção entre as três famílias candidatas a juiz
    (Claude Haiku 4.5 1,3%, DeepSeek V3.1 5,4%, Gemini 2.5 Pro 8,5%), SINTESE.md 2.5
- Por que importa: a comparação mais limpa e maior (272 mil tentativas) entre os três; mede agentes
  atacados, não juízes.
- Para o paper: método (escolha do juiz); ameaça à validade (a transferência para o papel de juiz é inferência).

### Lù et al. (2025). AgentRewardBench: Evaluating Automatic Evaluations of Web Agent Trajectories.
- Identificador: arXiv 2504.08942
- Arquivo local: `docs/refs/pesquisa-juiz-llm/2504.08942.pdf`
- Conferido no original: sim (2026-10-20, na síntese da avaliação híbrida; de novo em 2026-10-29)
- Quando foi útil:
  - 2026-10-20: regras com recall baixo, juiz com precisão baixa (`pesquisa-avaliacao-hibrida/SINTESE.md`)
  - 2026-10-29: juízes testados (Claude 3.7 Sonnet 69,4% de precisão; sem DeepSeek nem Gemini), SINTESE.md 2.1
- Por que importa: a tarefa publicada mais próxima da nossa (juiz de trajetórias de agentes).
- Para o paper: trabalhos relacionados; método.

### Caldwell et al. (2025). PentestJudge: Judging Agent Behavior Against Operational Requirements.
- Identificador: arXiv 2508.02921
- Arquivo local: `docs/refs/pesquisa-juiz-llm/2508.02921.pdf`
- Conferido no original: sim (2026-10-29)
- Quando foi útil:
  - 2026-10-29: F1 por juiz (Claude 3.7 Sonnet 0,83; Gemini 2.5 0,71 a 0,72), SINTESE.md 2.1
- Por que importa: única comparação direta encontrada entre Claude e Gemini como juízes de agente.
- Para o paper: trabalhos relacionados.

### Norman, Rivera & Hughes (2026). Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models.
- Identificador: arXiv 2606.19544 (UC Berkeley)
- Arquivo local: `docs/refs/pesquisa-juiz-llm/2606.19544.pdf`
- Conferido no original: sim (2026-10-29)
- Quando foi útil:
  - 2026-10-29: os três candidatos praticamente empatam em κ no MT-Bench (≈0,49 a 0,51); concordância
    bruta ≈0,85 esconde κ ≈0,5, SINTESE.md 2.1
- Por que importa: compara os três no mesmo protocolo; mostra por que reportar κ e não só concordância.
- Para o paper: método (por que κ).

### Yang et al. (2026). Quantifying and Mitigating Self-Preference Bias of LLM Judges. *Information Sciences*.
- Identificador: arXiv 2604.22891
- Arquivo local: `docs/refs/pesquisa-juiz-llm/2604.22891.pdf`
- Conferido no original: sim (2026-10-29)
- Quando foi útil:
  - 2026-10-29: β de autopreferência (DeepSeek-V3.2 +0,226; Claude-Sonnet-4.5 −0,229); decomposição
    reduz o viés em 31,5%, SINTESE.md 2.2
- Por que importa: medida de autopreferência por modelo; apoia as perguntas atômicas.
- Para o paper: método (juiz fora das famílias avaliadas; perguntas atômicas).

### Li et al. (2026). Preference Leakage: A Contamination Problem in LLM-as-a-judge. ICLR 2026.
- Identificador: arXiv 2502.01534
- Arquivo local: `docs/refs/pesquisa-juiz-llm/2502.01534.pdf`
- Conferido no original: sim (2026-10-29)
- Quando foi útil:
  - 2026-10-29: risco indireto de afinidade entre juiz e modelos treinados com dados dele, SINTESE.md 2.2
- Por que importa: é o risco que sobra mesmo com juiz de outra família.
- Para o paper: ameaça à validade.

### Keeman & Keeman (2026). aipsy-judge: A Specialized, Psychologist-Corrected Local Judge for the Psychological Safety of Conversational AI.
- Identificador: arXiv 2608.24899
- Arquivo local: `docs/refs/pesquisa-juiz-llm/2608.24899.pdf`
- Conferido no original: sim (2026-10-29)
- Quando foi útil:
  - 2026-10-29: Gemini como juiz é o mais leniente e tem prêmio de +0,99 nas próprias gerações; um dos
    motivos para deixar o Gemini de fora, SINTESE.md 2.2 e 4
- Por que importa: único dado específico de viés do Gemini como juiz.
- Para o paper: método (escolha do juiz).

### Chen et al. (2026). IterInject: Indirect Prompt Injection Against LLM Agents via Feedback-Guided Iterative Optimization.
- Identificador: arXiv 2605.24659
- Arquivo local: `docs/refs/pesquisa-juiz-llm/2605.24659.pdf`
- Conferido no original: sim (2026-10-29)
- Quando foi útil:
  - 2026-10-29: delimitadores cortam o ataque no DeepSeek de 32,9% para 15,3% (fixo) e de 47,8% para
    18,8% (otimizado), mas não zeram; justifica o teste de injeção, SINTESE.md 2.5 e 4
- Por que importa: mede o efeito da mitigação que o nosso desenho usa.
- Para o paper: método (mitigações do juiz).

### Li, Fung, Weiss et al. (2025). A Benchmark for Evaluating Outcome-Driven Constraint Violations in Autonomous AI Agents.
- Identificador: arXiv 2512.20798
- Arquivo local: `docs/refs/pesquisa-juiz-llm/2512.20798.pdf`
- Conferido no original: sim (2026-10-29)
- Quando foi útil:
  - 2026-10-29: painel de juízes com exclusão da autoavaliação (muda 1,9% das classificações); modelos
    DeepSeek excluídos "in adherence to institutional policy", SINTESE.md 2.2 e 4
- Por que importa: precedente de política institucional contra o DeepSeek, a perguntar à orientadora.
- Para o paper: método.

### Documentação oficial dos provedores (consultada em 29/10/2026)
- Identificador: Anthropic, *Pricing*, *Model deprecations*, *Model IDs and versioning*, página do
  Claude Haiku 5.5 (docs.claude.com); DeepSeek, *Models & Pricing* e *Change Log* (api-docs.deepseek.com);
  Google, *Gemini API pricing* e *Release notes* (ai.google.dev)
- Arquivo local: não baixado (páginas web; os trechos citados estão na SINTESE.md 2.4 e 3)
- Conferido no original: sim (2026-10-29)
- Quando foi útil:
  - 2026-10-29: preços, ID fixo e aposentadoria do Haiku 5.5 (não antes de 07/10/2027), "omit
    temperature", troca silenciosa de modelo no DeepSeek e no Gemini, preço do Gemini dobrando em
    01/01/2027, SINTESE.md 2.4 e 3
- Por que importa: a reprodutibilidade é a diferença decisiva entre os candidatos. Páginas mudam;
  reconferir antes de submeter o artigo.
- Para o paper: método (versão do juiz, reprodutibilidade).

### Demais referências conferidas na mesma síntese (29/10/2026)

| referência | arXiv | uso na SINTESE.md |
|---|---|---|
| LLM-as-a-Judge in Healthcare: A Scoping Analysis | 2605.25273 | 2.1: DeepSeek-V3 κ 0,59 (IC 0,37 a 0,82, N = 49) |
| JudgeArena | 2608.02620 | 2.1: κ de todos os juízes entre 0,11 e 0,17 na tarefa |
| STAGE | 2601.08510 | 2.1: DeepSeek-V4-Pro validado como juiz (90,3%) |
| Is Deep Research Reliable? | 2607.20891 | 2.1: DeepSeek-V4 Pro κ 0,993 |
| From Production Traffic to Post-Training | 2609.01572 | 2.1: critério explícito melhora o juiz |
| Estonian Native LLM Benchmark | 2510.21193 | 2.1: Claude 3.7 Sonnet como juiz |
| Benchmarking LLM Judges for Mobile Agent Evaluation | 2608.11434 | 2.1 |
| Zheng et al., Judging LLM-as-a-Judge (MT-Bench) | 2306.05685 | 2.1: 85% GPT-4 × humanos |
| CyclicJudge | 2603.01865 | 2.2: autoviés do Claude Sonnet 4.6 |
| GAUGE | 2609.12191 | 2.2: autopreferência de família |
| Ye et al., Justice or Prejudice? | 2410.02736 | 2.2 |
| CheckEval | 2403.18771 | 2.3 (já na síntese de 20/10) |
| TICK | 2410.03608 | 2.3 (já na síntese de 20/10) |
| Towards a Reliable and Practical Eval Pipeline | 2609.00805 | 2.3 |
| LLM-42 | 2601.17768 | 2.4: custo do modo determinístico |
| Beyond Reproducibility | 2601.06118 | 2.4 |
| DREAM | 2512.19016 | 2.5 |
| TRAP | 2512.23128 | 2.5 |
| AgentSys | 2602.07398 | 2.5 |
| Defenses & Enablers For Skill Injection Attacks | 2606.01567 | 2.5 |
| AutoDojo | 2606.15057 | 2.5 |
| JudgeDeceiver | 2403.17710 | 2.5 |
| The Attacker Moves Second | 2510.09023 | 2.5 |
| Investigating the Vulnerability of LLM-as-a-Judge (juízes Qwen2.5-3B e Falcon3-3B) | 2505.13348 | 5: erro do relatório do Claude |
| AgentDojo | 2406.13352 | 5: o número do relatório não bate com a versão atual |
| MINJA | 2503.03704 | 5 |
| Lessons from Defending Gemini | 2505.14534 | 6: não lido a fundo |

## Auditoria para a qualificação (conferida em 24/11/2026)

Detalhe e citações literais em `docs/06-qualificacao/AUDITORIA_REFERENCIAS.md`. Os três surveys
gerais que estavam em `papers/` (Shayegani et al. 2023, arXiv 2310.10844, preprint; Dong et al. 2024,
arXiv 2402.01822, ICML 2024; Wang et al. 2024, arXiv 2407.16216, preprint, hoje com outro título na v4)
foram conferidos só quanto à existência e ao local; servem ao capítulo de conceitos.

### Nöther, J. et al. (2025-2026). Benchmarking the Robustness of Agentic Systems to Adversarially-Induced Harms (BAD-ACTS).
- Identificador: arXiv 2508.16481 (v1 22/08/2025, v2 07/10/2025, v3 07/08/2026; a v3 muda o título para "...Harmful Behaviors")
- Publicação: v3: COLM 2026, revisada por pares (OpenReview e cabeçalho do PDF; antes rejeitado no ICLR 2026); v1 e v2 preprint
- Arquivo local: `docs/refs/auditoria-quali/badacts-v{1,2,3}.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - antes de 24/11/2026: base de todo o fork (`CLAUDE.md`)
  - 2026-10-20: regras com 98% de concordância com humanos contra 80% do juiz LLM (§3.3); utilidade só por juiz de nota 1 a 5, sem adversário e sem validação humana (§4.2) (`04-paper/pesquisa-avaliacao-hibrida/SINTESE.md` 1 e 2)
  - 2026-10-28: a medida de qualidade 1-5 só existe na v3 (`04-paper/NOVIDADE_E_POSICIONAMENTO.md` 9)
  - 2026-11-24: conferido que **repete cada experimento três vezes e reporta média e erro padrão** (nas três versões) e que o juiz de qualidade da v3 não tem validação humana (`06-qualificacao/AUDITORIA_REFERENCIAS.md` 2.3)
  - 2026-11-24: só há três versões no arXiv; a v3 tem 238 ações e a média por posição foi para a Tabela 13, com os números da Tabela 2 da v2; o `datasets/BAD-ACTS.csv` do fork é o de 188 ações (v1/v2), então o nosso ASR por posição compara com a Tabela 2 da v2 ou a Tabela 13 da v3; exemplo revisado de repetição só agregada (`04-paper/pesquisa-lacuna-robustez-multiagente/SINTESE.md` 1 e 3)
- Por que importa: é o benchmark estendido. Números mudam muito entre v2 e v3 (ASR de 40% a 90% na v3): citar sempre a versão.
- Para o paper: método e relacionados; nunca citar seus números pelo resumo do Li et al.

### Li, M. Q.; Fung, B. C. M. et al. (2026). Taxonomy and Consistency Analysis of Safety Benchmarks for AI Agents.
- Identificador: arXiv 2605.16282 (11/04/2026)
- Publicação: preprint (cs.CY)
- Arquivo local: `docs/refs/li2026-taxonomy-safety-benchmarks.pdf` (cópia idêntica em `docs/refs/auditoria-quali/`)
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - antes de 24/11/2026: âncora da lacuna R10 (`CLAUDE.md`, monografia de julho)
  - 2026-11-23: conferido R10 = 0 primários e 7 parciais (BAD-ACTS entre eles), W de Kendall = 0,10 (p = 0,94) (`06-qualificacao/MAPA_DE_REIVINDICACOES.md` C1 a C3)
  - 2026-11-24: o resumo que faz do BAD-ACTS tem número que não existe ("53% Llama-3.1-8B")
  - 2026-11-24: frases conferidas para a C1: "very little repeated-perturbation testing" (Gap 4, p. 20) e "a few benchmarks report multi-run variance—none treat robustness as a first-class safety property" (p. 25) (`04-paper/pesquisa-lacuna-robustez-multiagente/SINTESE.md` P6)
- Por que importa: a taxonomia que define R10 e mostra que nenhum benchmark é primário nela.
- Para o paper: introdução e lacuna; fonte única e preprint, citar junto do Rabanser et al.

### Rabanser, S. et al. (2026). Towards a Science of AI Agent Reliability.
- Identificador: arXiv 2602.16666 (v3)
- Publicação: ICML 2026, PMLR 306:102769-102820, revisada por pares (confirmado em 24/11/2026: proceedings.mlr.press/v306/rabanser26a.html)
- Arquivo local: `docs/refs/auditoria-quali/rabanser2026-agent-reliability.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: 4 dimensões, 12 métricas, **15 modelos** (não 14), K = 5 execuções e paráfrases; "We do not evaluate adversarial attacks" (p. 2); robustez a adversários e confiabilidade multiagente como problemas abertos (p. 24-25) (`AUDITORIA_REFERENCIAS.md` 2.1)
  - 2026-11-24: conferido de novo: "extending these metrics to multi-agent systems" (p. 23) e "prompt injection affects consistency" (p. 24) como abertos; é a motivação revisada da C1 pela regra de citação (`04-paper/pesquisa-lacuna-robustez-multiagente/SINTESE.md` P6); controle estatístico de processo só como analogia, Ap. D.2 (`04-paper/pesquisa-cep-doe-avaliacao/SINTESE.md` 6)
- Por que importa: concorrente conceitual mais forte e, ao mesmo tempo, a melhor sustentação revisada por pares da lacuna.
- Para o paper: relacionados e lacuna

### Raj, H. et al. (2026). Consistency as a Testable Property: Statistical Methods to Evaluate AI Agent Reliability.
- Identificador: arXiv 2605.10516 (v2)
- Publicação: NeurIPS 2026, pôster, revisada por pares (confirmado em 24/11/2026: neurips.cc/virtual/2026/poster/155880); também IIMB Working Paper 741
- Arquivo local: `docs/refs/auditoria-quali/raj2026-consistency-testable.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: estatísticas U, consistência observável × interna; tem uma perturbação "injection" que é ruído e mede tarefa, não segurança; agente único
  - 2026-11-24: local confirmado de novo no OpenReview ("NeurIPS 2026 poster") (`04-paper/pesquisa-lacuna-robustez-multiagente/SINTESE.md` 4 e 5)
- Por que importa: o mais próximo do enquadramento estatístico; sem segurança sob ataque nem multiagente.
- Para o paper: relacionados

### Potamitis, N. et al. (2025). ReasonBENCH: Benchmarking the (In)Stability of LLM Reasoning.
- Identificador: arXiv 2512.07795 (v2)
- Publicação: workshop P-AGI do ICLR 2026 (OpenReview), revisado (workshop); a etapa 2 dizia preprint
- Arquivo local: `docs/refs/auditoria-quali/potamitis2025-reasonbench.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: 30 repetições por configuração com IC por bootstrap estratificado; "wins only 77% of head-to-head runs" (p. 1)
  - 2026-11-24: decomposição hierárquica (sequencial, ordem fixa, 4.3) que atribui três quartos da variância a benchmark, sistema e item, com resíduo que a execução única absorve (`04-paper/pesquisa-cep-doe-avaliacao/SINTESE.md` 4)
- Por que importa: precedente de repetição com IC; estratégias de raciocínio, sem ataque.
- Para o paper: relacionados

### Yagubyan, A. (2026). How Consistent Are LLM Agents? Measuring Behavioral Reproducibility in Multi-Step Tool-Calling.
- Identificador: arXiv 2605.28840
- Publicação: preprint, autor único independente
- Arquivo local: `docs/refs/auditoria-quali/yagubyan2026-how-consistent.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: 1.140 traços, IC de 95%, ANOVA de um fator; sem ataque e sem multiagente
  - 2026-11-24: "60 % of first-divergence events occur within the first two pipeline steps" (5.3): eventos, não fração da variância; apoia o episódio como unidade na objeção (c) (`04-paper/pesquisa-cep-doe-avaliacao/SINTESE.md` 3)
- Por que importa: reprodutibilidade de agentes com ferramentas por repetição idêntica.
- Para o paper: relacionados; peso baixo (preprint, autor único)

### Lunardi, R. et al. (2025). On Robustness and Reliability of Benchmark-Based Evaluation of LLMs.
- Identificador: arXiv 2509.04013
- Publicação: ECAI 2025, DOI 10.3233/FAIA251363 (Crossref), revisada por pares; volume e páginas na IOS Press não conferidos
- Arquivo local: `docs/refs/auditoria-quali/lunardi2025-robustness-benchmarks.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: paráfrase de 6 benchmarks, 34 LLMs, ranking estável e queda absoluta
  - 2026-11-24: local confirmado pelo Crossref; serve à M10 da revisão metodológica (paráfrase muda o número sem mudar o ranking) (`04-paper/pesquisa-lacuna-robustez-multiagente/SINTESE.md` P2)
- Por que importa: paráfrase muda o resultado absoluto: apoio ao B1/B2; perguntas e respostas, sem agentes.
- Para o paper: relacionados (motivação do B1/B2)

### Mohammadi, M. et al. (2025). Evaluation and Benchmarking of LLM Agents: A Survey.
- Identificador: arXiv 2507.21504; doi 10.1145/3711896.3736570
- Publicação: KDD '25 (ACM SIGKDD), revisada por pares
- Arquivo local: `docs/refs/auditoria-quali/mohammadi2025-agent-eval-survey.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: agentes devem ser consistentes entre execuções repetidas (p. 4), medir é caro (p. 8); a frase "a área raramente mede" do documento de agosto **não está** no texto
- Por que importa: survey revisado por pares sobre avaliação de agentes.
- Para o paper: relacionados (panorama)

### Mitra, S. (2026). Spark-LLM-Eval: A Distributed Framework for Statistically Rigorous Large Language Model Evaluation.
- Identificador: arXiv 2603.28769
- Publicação: preprint, autor único
- Arquivo local: `docs/refs/auditoria-quali/mitra2026-spark-llm-eval.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: IC por bootstrap e testes em toda métrica; a frase certa é "many evaluation frameworks report only point estimates" (p. 3)
- Por que importa: exemplo de rigor estatístico genérico na avaliação.
- Para o paper: relacionados; peso baixo

### Miller, E. (2024). Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations.
- Identificador: arXiv 2411.00640
- Publicação: preprint (Anthropic), autor único; nenhum local de publicação encontrado em 24/11/2026
- Arquivo local: `docs/refs/auditoria-quali/miller2024-error-bars.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: "evaluations are experiments" (p. 1); recomenda erro padrão agrupado, reamostrar respostas, diferenças pareadas e análise de poder; nada de cartas de controle ou fatorial
  - 2026-11-24: Seção 3.3 contra baixar a temperatura ("we advise against this practice, unless the purpose is to study the model at the new temperature"); a dissertação segue o Miller e declara o Blackwell como posição contrária (`04-paper/pesquisa-cep-doe-avaliacao/SINTESE.md` 3; `06-qualificacao/REVISAO_METODOLOGICA.md` M9)
- Por que importa: a referência mais citada sobre estatística em avaliação de LLM; o erro padrão agrupado é parte da resposta à objeção de independência.
- Para o paper: método

### Xie, X. et al. (2023). Adversarial Client Detection via Non-parametric Subspace Monitoring in the Internet of Federated Things.
- Identificador: arXiv 2310.01537; DOI 10.1080/24725854.2024.2367224
- Publicação: *IISE Transactions* 57(7):743-755, 2025 (Crossref), periódico revisado; a etapa 2 dizia preprint. O PDF local é a v1 do arXiv; a versão IISE não foi aberta
- Arquivo local: `docs/refs/auditoria-quali/xie2023-federated-spc.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: CUSUM não paramétrico, cita o ISQC de Montgomery; detecção de ataque, não avaliação; não é LLM
  - 2026-11-24: local corrigido e uso de CUSUM confirmado (Seção 3.2) (`04-paper/pesquisa-cep-doe-avaliacao/SINTESE.md` 5 e 6)
- Por que importa: precedente de controle estatístico contra ataque, fora de LLM.
- Para o paper: relacionados do método

### Jia, Y. et al. (2021). Adversarial Attacks and Mitigation for Anomaly Detectors of Cyber-Physical Systems.
- Identificador: arXiv 2105.10707
- Publicação: International Journal of Critical Infrastructure Protection 34:100452 (2021), periódico
- Arquivo local: `docs/refs/auditoria-quali/jia2021-cps-cusum.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: CUSUM com UCL/LCL, mas é o detector que o artigo ataca, não a contribuição
  - 2026-11-24: DOI 10.1016/j.ijcip.2021.100452 conferido no Crossref; relevância baixa (`04-paper/pesquisa-cep-doe-avaliacao/SINTESE.md` 6)
- Por que importa: precedente fraco de controle estatístico em segurança.
- Para o paper: relacionados do método; citar com a ressalva

### Venkatesh, K. et al. (2026). CASPIAN: Online Detection and Attribution of Cascade Attacks in LLM Multi-Agent Systems.
- Identificador: arXiv 2605.19240
- Publicação: preprint
- Arquivo local: `docs/refs/auditoria-quali/venkatesh2026-caspian.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: detector de cascata por regra espectral, avaliado em TAMAS e ACIArena; não mede estabilidade do ASR
- Por que importa: multiagente adversarial, mas sobre detecção.
- Para o paper: relacionados

### Debenedetti, E. et al. (2024). AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents.
- Identificador: arXiv 2406.13352 (v3)
- Publicação: NeurIPS 2024, Datasets and Benchmarks, revisada por pares; DOI 10.52202/079017-2636 (Crossref)
- Arquivo local: `docs/refs/auditoria-quali/agentdojo.pdf` (cópia idêntica em `docs/refs/pesquisa-juiz-llm/2406.13352.pdf`)
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-10-20: utilidade por "deterministic binary function" em benchmark de ataque (§1 e §3.1) (`04-paper/pesquisa-avaliacao-hibrida/SINTESE.md` 2)
  - 2026-11-24: conferido: utility under attack por função determinística sobre o estado do ambiente (§3.4); rejeita juiz LLM porque o ataque pode sequestrá-lo (p. 4); IC binomial; não declara repetições
  - 2026-11-24: "models with low utility often fail at correctly executing the attacker's goal, even when the prompt injection succeeds" (p. 7), apoio revisado à C6 (`04-paper/pesquisa-lacuna-robustez-multiagente/SINTESE.md` P5)
  - 2026-11-24: **corrigido**: a função recebe também `model_output` ("by inspecting the model output and the mutations in the environment state", §3.1, p. 4); e deixou de ser "o único" que mede utilidade sob ataque (`04-paper/pesquisa-utilidade-sob-ataque/SINTESE.md` 2 e 3)
- Por que importa: o precedente mais citado de utilidade sob ataque (não o único, ver a etapa 3); agente único.
- Para o paper: relacionados da medida; argumento a enfrentar no desenho do juiz

### Zhang, H. et al. (2025). Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents.
- Identificador: arXiv 2410.02644
- Publicação: ICLR 2025, revisada por pares
- Arquivo local: `docs/refs/auditoria-quali/asb.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: PNA sem ataque; NRP = PNA × (1 − ASR); tudo por chamada de ferramenta; não declara repetições
  - 2026-11-24: local reconferido (ICLR 2025), só quanto a existência; relevância baixa para a lacuna (`04-paper/pesquisa-lacuna-robustez-multiagente/SINTESE.md` 5)
- Por que importa: combina utilidade sem ataque com ASR.
- Para o paper: relacionados da medida

### Kavathekar, I. et al. (2025). TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems.
- Identificador: arXiv 2511.05269; DOI 10.18653/v1/2026.acl-long.1442
- Publicação: ACL 2026 Long, pp. 31238-31268 (ACL Anthology), revisada por pares; a etapa 2 dizia workshop MAS do ICML 2025, pelo comentário do arXiv. Citar a versão dos anais
- Arquivo local: `docs/refs/auditoria-quali/kavathekar2026-tamas-acl.pdf` (anais) e `docs/refs/auditoria-quali/tamas.pdf` (arXiv v1)
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: ERS = média harmônica de segurança e PNA; **PNA medida sem ataque**, por chamada de ferramenta; juiz de segurança com F1 de 89,17% contra humano; não declara repetições
  - 2026-11-24: paráfrase **como defesa**: remove a injeção em 94% dos casos e omite alguma subtarefa em 48% (Ap. D.4); "the apparent defense success in these cases reflects task removal rather than robust mitigation of malicious intent" (p. 31255), o melhor apoio revisado à C6 e à QA3 em multiagente (`04-paper/pesquisa-lacuna-robustez-multiagente/SINTESE.md` 1)
  - 2026-11-24: na versão dos anais o juiz de segurança tem 120 registros, dois anotadores e desempate, κ 0,77, F1 89,13% (Ap. C.1); a v1 dizia 140 e 89,17% (`04-paper/pesquisa-utilidade-sob-ataque/SINTESE.md` P3)
- Por que importa: o concorrente multiagente mais próximo da medida de utilidade.
- Para o paper: relacionados da medida

### Zhang, Z. et al. (2024). Agent-SafetyBench: Evaluating the Safety of LLM Agents.
- Identificador: arXiv 2412.14470 (v2)
- Publicação: workshop AAAI 2026 Trust and Control in Agentic AI (n.º 30 da lista de aceitos, página do workshop), revisado (workshop); se o workshop é arquivado não foi conferido; a etapa 2 dizia preprint
- Arquivo local: `docs/refs/auditoria-quali/zhang2024-agent-safetybench.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: juiz de segurança ajustado (91,5% em 200 de outro modelo); utilidade por GPT-4o com 94% em validação manual sem n; agente único
  - 2026-11-24: o 94% do juiz de utilidade está no §4.4 da v2, sem n, sem κ e sem conjunto separado; local corrigido (`04-paper/pesquisa-utilidade-sob-ataque/SINTESE.md` P3)
- Por que importa: exemplo de juiz validado contra humano em agentes.
- Para o paper: relacionados da medida

## Etapa 3 da auditoria (conferida em 24/11/2026)

Uma entrada por obra conferida nas três sínteses da etapa 3 que ainda não tinha entrada:
`docs/04-paper/pesquisa-lacuna-robustez-multiagente/SINTESE.md` (lacuna),
`docs/04-paper/pesquisa-utilidade-sob-ataque/SINTESE.md` (utilidade) e
`docs/04-paper/pesquisa-cep-doe-avaliacao/SINTESE.md` (método). As obras que já tinham entrada
(BAD-ACTS, Li et al., Rabanser, Raj, ReasonBench, Yagubyan, Lunardi, Miller, Xie, Jia, AgentDojo, ASB,
TAMAS, Agent-SafetyBench) ganharam uma linha em "Quando foi útil" nas seções acima. O local de
publicação foi conferido nos anais (ACL Anthology, PMLR, OpenReview, listas do neurips.cc e do
iclr.cc, Crossref, PubMed), nunca só pelo comentário do arXiv. Os arquivos estão em
`docs/refs/auditoria-quali/`; a lista completa, com a URL de cada PDF aberto, está em
`docs/refs/MANIFESTO.csv`.

### Lacuna de robustez em multiagente sob ataque

#### Triedman, H.; Jha, R.; Shmatikov, V. (2025). Multi-Agent Systems Execute Arbitrary Malicious Code.
- Identificador: arXiv 2503.12188 (v2)
- Publicação: COLM 2025 (OpenReview, venue COLM 2025), revisada por pares
- Arquivo local: `docs/refs/auditoria-quali/triedman2025-mas-malicious-code.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: derruba a versão ampla da lacuna: 10 paráfrases da consulta do usuário, 20 execuções cada, "ASR ranging from 40% to 85%" (§6.4); o bloco B1 deixa de ser inédito como ideia (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` 1, P3 e 6)
- Por que importa: é o vizinho mais próximo do B1: paráfrase da tarefa em multiagente sob ataque. Falta: o adversário é externo (arquivo ou página), não há análise por caso, a tarefa não é medida sob ataque, e paráfrase e repetição não são separadas.
- Para o paper: trabalhos relacionados (um dos cinco que o texto tem de citar); define o que é novo no B1

#### Khan, AlKhanbashi, Mohamed (2026). Evaluating Indirect Prompt Injection Defenses in Tool-Using LLM Agents: Security, Utility, and Replication.
- Identificador: DOI 10.3390/computers15090570
- Publicação: *Computers* 15(9):570, 2026 (MDPI; PDF da editora e Crossref), periódico revisado
- Arquivo local: `docs/refs/auditoria-quali/khan2026-ipi-replication.pdf` (a MDPI bloqueia download automático: baixar à mão)
- Conferido no original: sim (2026-11-24), pela pesquisa da lacuna; a pesquisa da utilidade leu só o resumo
- Quando foi útil:
  - 2026-11-24: duas réplicas com "the same benchmark version, task set, prompts, model snapshot, and temperature settings" (§5.5), resultado por item (Fig. 4), ASR condicionado à viabilidade com canários, "goal feasibility is an important confound" (§5.2, p. 20) (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` 1 e P5)
  - 2026-11-24: entre os que medem utilidade sob ataque (`pesquisa-utilidade-sob-ataque/SINTESE.md` P1)
- Por que importa: o mais próximo de repetição por caso em agentes, e um método (canário de viabilidade) a comparar com o nosso quadrante. Falta: agente único (AgentDojo banking), duas repetições, ataques raríssimos, sem paráfrase.
- Para o paper: trabalhos relacionados (lacuna e C6); comparação de método com o quadrante

#### Zhang (2026). Does Safety Reasoning Travel? A Multilingual Measurement of Prompt-Injection Attacks and Runtime Monitors.
- Identificador: DOI 10.18653/2026.oracle-main.13 (sem "v1")
- Publicação: workshop ORACLE 2026, pp. 194-204 (ACL Anthology), revisado (workshop)
- Arquivo local: `docs/refs/auditoria-quali/zhang2026-oracle.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: redação do invólucro da injeção com objetivo "byte-identical"; ASR de 0,264 a 0,491 (GPT-4o-mini) e 0,340 a 0,623 (GPT-4.1-mini) (Tab. 7); casos repartidos entre os invólucros (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` 1, P2 e 4)
- Por que importa: o vizinho do B2 (redação do ataque). Falta: agente único, temperatura 0 sem repetição, e os 320 casos são repartidos entre redações, o que mistura redação e subconjunto.
- Para o paper: trabalhos relacionados; argumento a favor de aplicar todas as variantes a todos os casos

#### Pathade, Pawar, Patil (2026). Attack Success Rate Is Not a Number: On Measurement Validity in Agentic Security.
- Identificador: arXiv 2609.25173
- Publicação: preprint
- Arquivo local: `docs/refs/auditoria-quali/pathade2026-asr-not-number.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: defesas separadas por 5 pontos ficam invertidas "about 21% of the time" (§V-A), só analítico ("we report no empirical ranking inversion", §VIII); 58,0% de 50 trabalhos sem variância nem repetição (§IV-D, Tab. II) (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` P4 e P6)
- Por que importa: apoio à C1 e versão analítica da C17. Falta: inversão empírica, multiagente.
- Para o paper: introdução e motivação, como trabalho recente (preprint)

#### Larsen, E. (2025). The Instability of Safety: How Random Seeds and Temperature Expose Inconsistent LLM Refusal Behavior.
- Identificador: arXiv 2512.12066 (v4, 14/10/2026)
- Publicação: preprint, autor único
- Arquivo local: `docs/refs/auditoria-quali/larsen2025-instability-safety.pdf` (baixado em 24/11/2026)
- Conferido no original: só resumo (a SINTESE conferiu a página do arXiv; o PDF baixado em 24/11 confirma no resumo 876 prompts, 4 temperaturas × 5 sementes e "18–28%")
- Quando foi útil:
  - 2026-11-24: precedente mais direto de estabilidade de segurança por caso sob repetição, em chat; índice de estabilidade por prompt (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` P1)
- Por que importa: mostra a troca de decisão por prompt sob semente e temperatura. Falta: agentes, multiagente, ataque por agente interno, paráfrase. **Ler na íntegra antes da quali.**
- Para o paper: trabalhos relacionados (estabilidade sob repetição)

#### Aleksandrov, I. et al. (2026). DUMA-Bench: A Dual-Control Multi-Agent Benchmark for Evaluating LLM Agent Security.
- Identificador: arXiv 2609.24662
- Publicação: preprint (o comentário do arXiv diz Findings, mas não está nos Findings of ACL 2026 do Anthology)
- Arquivo local: `docs/refs/auditoria-quali/aleksandrov2026-duma-bench.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: "n = 5 independent runs" por configuração; pass^1 0,722 para pass^5 0,596 (§4.4, Ap. C) (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` P1)
- Por que importa: repetição em segurança de agente. Falta: é agente com usuário simulado, não time com adversário interno.
- Para o paper: trabalhos relacionados; relevância média

#### Lee et al. (2026). NRT-Bench: Benchmarking Multi-Turn Red-Teaming of LLM Operator Agents.
- Identificador: arXiv 2606.20408 (v3)
- Publicação: workshop do KDD 2026 (OpenReview; anais não conferidos)
- Arquivo local: `docs/refs/auditoria-quali/lee2026-nrt-bench.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: time de cinco agentes; a mesma defesa ajuda um modelo e prejudica outro, mas "Each is run at a single fixed seed" (p. 5) (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` P3 e P4)
- Por que importa: exemplo de conclusão multiagente que o próprio desenho não separa do ruído, que é a pergunta da dissertação.
- Para o paper: trabalhos relacionados; motivação

#### Rahman et al. (2026). The Framing Gap: Indirect Prompt-Injection Exfiltration Defeats Surface-Level Defenses in Tool-Using Agents.
- Identificador: arXiv 2608.27092
- Publicação: preprint
- Arquivo local: `docs/refs/auditoria-quali/rahman2026-framing-gap.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: "per-wording rates span 0–100%" com 20 execuções pareadas por célula; oscilação de 13 pontos entre execuções idênticas (p. 6); ressalva "Variant-level pooled rates are properties of the wordings we chose" (p. 2) (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` P1 e P2)
- Por que importa: redação do ataque e repetição juntas, em agente único. A ressalva sobre as redações escolhidas vale para o B2.
- Para o paper: trabalhos relacionados; ameaça à validade (generalização das variantes)

#### Evtimov et al. (2025). WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks.
- Identificador: arXiv 2504.18575 (v3)
- Publicação: NeurIPS 2025, Datasets and Benchmarks (OpenReview e lista do neurips.cc), revisado
- Arquivo local: `docs/refs/auditoria-quali/evtimov2025-wasp.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: "We term this phenomenon 'security through incompetence'" (p. 8), apoio revisado à C6 e à QA3 (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` P5)
  - 2026-11-24: "Utility-under-attack" só existia na v2; a v3 mede utilidade só sem ataque (§3.4), então fica fora da lista de quem mede utilidade sob ataque (`pesquisa-utilidade-sob-ataque/SINTESE.md` P1)
- Por que importa: dá nome ao confundimento entre ASR baixo e incompetência.
- Para o paper: trabalhos relacionados (C6); citar a v3

#### Shahroz et al. (2025). Agents Under Siege: Breaking Pragmatic Multi-Agent LLM Systems with Optimized Prompt Attacks.
- Identificador: DOI 10.18653/v1/2025.acl-long.476
- Publicação: ACL 2025 Long, pp. 9661-9674 (ACL Anthology), revisado
- Arquivo local: `docs/refs/auditoria-quali/shahroz2025-agents-under-siege.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: "three times with randomized multi-agent topologies" (p. 6), só agregado; o "mínimo, média e máximo" do relatório do Claude não existe (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` P3)
- Por que importa: multiagente sob ataque com repetição só agregada, como o BAD-ACTS.
- Para o paper: trabalhos relacionados; relevância média

#### Liu, F. et al. (2025). Can an Individual Manipulate the Collective Decisions of Multi-Agents? (M-Spoiler)
- Identificador: DOI 10.18653/v1/2025.emnlp-main.611
- Publicação: EMNLP 2025, pp. 12158-12182 (ACL Anthology), revisado
- Arquivo local: `docs/refs/auditoria-quali/liu2025-m-spoiler.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: "three evaluations using different random seeds and report the mean and standard deviation" (§4.1) (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` P3)
- Por que importa: agente interno manipulando o coletivo, com repetição só agregada.
- Para o paper: trabalhos relacionados; relevância média

#### Lee, H.; Yun, V.-D.; Panagou, D. et al. (2026). Robust Multi-Agent LLMs under Byzantine Faults.
- Identificador: DOI 10.18653/2026.emnlp-main.1960; arXiv 2605.09076
- Publicação: EMNLP 2026, pp. 44639-44657 (ACL Anthology), revisado
- Arquivo local: `docs/refs/auditoria-quali/lee2026-byzantine.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: agente bizantino com tarefa, sem repetição; a frase de custo do relatório do Claude justifica subconjuntos do MATH (§5.2), não falta de repetição (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` 4)
- Por que importa: agente interno defeituoso em multiagente, revisado; sem estabilidade.
- Para o paper: trabalhos relacionados; relevância média

#### Yang et al. (2026). SoK: When Safe Agents Fail Together: The Security of Multi Agent LLM Systems.
- Identificador: arXiv 2609.00595
- Publicação: preprint
- Arquivo local: `docs/refs/auditoria-quali/yang2026-sok-safe-agents.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: audita 44 avaliações de multiagente sem falar de sementes nem de variância; pede que "Benign task utility should be reported separately from security outcomes" (§6.2) (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` P6)
- Por que importa: o silêncio de um SoK sobre variância apoia a C1; o pedido de utilidade separada apoia a medida.
- Para o paper: introdução, como trabalho recente

#### Chen, F.; Rabanser, S. et al. (2026). Emerging Trends in AI Agent Evaluation.
- Identificador: relatório do grupo SAgE de Princeton, 19/10/2026 (sem DOI nem arXiv; URL de origem não registrada)
- Publicação: relatório técnico, sem revisão
- Arquivo local: `docs/refs/auditoria-quali/chen2026-emerging-trends.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: "Conduct repeated runs to measure consistency for each task, and report how many runs were conducted" (§1d, p. 14) e "Multi-agent contexts introduce additional sources of variance" (p. 13) (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` P6)
- Por que importa: recomendação de repetição por tarefa, do mesmo grupo do Rabanser.
- Para o paper: introdução, como relatório não revisado

#### Malla et al. (2026). From Monoliths to Swarms: A Study of Attack Surface Evolution.
- Identificador: arXiv 2608.00202
- Publicação: preprint
- Arquivo local: `docs/refs/auditoria-quali/malla2026-monoliths-swarms.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: ASR condicionado à exposição ao ataque (p. 9) (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` P5)
- Por que importa: outra forma de separar ASR de exposição; relevância baixa.
- Para o paper: relacionados (C6), opcional

#### Anonto, R. A. et al. (2026). How Semantically Stable Are LLM Refusals? (ParaGuard)
- Identificador: arXiv 2512.01037 (v3)
- Publicação: não conferida (o DSAA 2026 não foi confirmado)
- Arquivo local: `docs/refs/auditoria-quali/anonto2026-paraguard.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: paráfrase em chat; o objeto é recusa **excessiva** de pedidos benignos, não aceitação de pedido danoso (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` P2)
- Por que importa: precedente de paráfrase sobre recusa, com objeto diferente; relevância baixa.
- Para o paper: relacionados, com a ressalva do objeto

#### Monteuuis et al. (2026). The Great Pretender: A Stochasticity Problem in LLM Jailbreak.
- Identificador: arXiv 2605.14418
- Publicação: preprint (desk-rejected no ICLR 2027)
- Arquivo local: `docs/refs/auditoria-quali/monteuuis2026-great-pretender.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: a queda do ASR com repetição é "caused entirely by judge stochasticity" (p. 8); corrige o relatório do Claude (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` 4)
- Por que importa: reforça a escolha do fork por veredito determinístico (palavra-chave): a variação medida é do sistema, não do juiz.
- Para o paper: método (por que o veredito é determinístico); relevância baixa

#### Conferidos só quanto à existência e ao local (relevância baixa)
- He, P. et al. (2025). *Red-Teaming LLM Multi-Agent Systems via Communication Attacks* (AiTM). arXiv 2502.14847; Findings of ACL 2025, DOI 10.18653/v1/2025.findings-acl.349. Arquivo: `auditoria-quali/he2025-aitm.pdf` (baixado em 24/11). Útil em 2026-11-24: multiagente sob ataque, ASR agregado sem repetição (`pesquisa-lacuna-robustez-multiagente/SINTESE.md` 5). Para o paper: relacionados.
- Lee, D. et al. (2024). *Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems*. arXiv 2410.07283; local não conferido. Arquivo: `auditoria-quali/lee2024-prompt-infection.pdf` (baixado em 24/11). Mesmo uso. Para o paper: relacionados (propagação entre agentes).
- Arora, N. et al. (2025). *Exposing Weak Links in Multi-Agent Systems under Adversarial Prompting* (SafeAgents/DHARMA). arXiv 2511.10949; workshop AAMAS 2026. Arquivo: `auditoria-quali/arora2025-safeagents.pdf` (baixado em 24/11). Mesmo uso; também no grupo R5 do Li et al. (`06-qualificacao/AUDITORIA_REFERENCIAS.md` 3). Para o paper: relacionados.
- Akkil, D. et al. (2026). *Emergence World: Adversarial Stress-Testing of Long-Horizon Multi-Agent Systems*. arXiv 2609.17320; preprint. Arquivo: `auditoria-quali/akkil2026-emergence-world.pdf` (baixado em 24/11). Mesmo uso.

#### Pistas do prompt da lacuna, conferidas pela página do arXiv (nenhuma ameaça a lacuna)
- Siqueira de Cerqueira, J. A. et al. (2024). *Can We Trust AI Agents? A Case Study of an LLM-Based Multi-Agent System for Ethical AI*. arXiv 2411.08881. Arquivo: `auditoria-quali/cerqueira2024-trust-ai-agents.pdf`. Multiagente sem ataque.
- Bogavelli, T. et al. (2026). *Evaluating Robustness of Large Language Models in Enterprise Applications*. arXiv 2601.06341. Arquivo: `auditoria-quali/bogavelli2026-enterprise-robustness.pdf`. Consistência sob formato e língua, sem ataque nem agentes.
- Gupta, A. (2026). *ReliabilityBench: Evaluating LLM Agent Reliability Under Production-Like Stress Conditions*. arXiv 2601.06112. Arquivo: `auditoria-quali/gupta2026-reliabilitybench.pdf`. pass^k e perturbações equivalentes em agente, capacidade e não segurança; **entra ao lado do Rabanser** como confiabilidade sem ataque. Para o paper: relacionados.
- Zhan, Q. et al. (2025). *Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents*. arXiv 2503.00061. Arquivo: `auditoria-quali/zhan2025-adaptive-attacks-ipi.pdf`. Ataques adaptativos; não trata repetição nem paráfrase. (O *The Attacker Moves Second*, arXiv 2510.09023, da mesma pista, já está na tabela da pesquisa do juiz.)
- Todas: publicação não conferida; conferido no original: só metadados (página do arXiv), PDF baixado em 24/11; útil em 2026-11-24 em `pesquisa-lacuna-robustez-multiagente/SINTESE.md` 4.

### Utilidade sob ataque validada contra humano

#### Gomaa, A.; Salem, A.; Abdelnabi, S. (2026). ConVerse: Benchmarking Contextual Safety in Agent-to-Agent Conversations.
- Identificador: DOI 10.18653/v1/2026.findings-eacl.170
- Publicação: Findings of EACL 2026, pp. 3246-3268 (ACL Anthology), revisado
- Arquivo local: `docs/refs/auditoria-quali/gomaa2026-converse.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: um dos três mais próximos da C11: plano de viagem sob ataque, casado por LLM com um catálogo de 158 a 184 opções; validação humana (um autor) só dos ataques (`pesquisa-utilidade-sob-ataque/SINTESE.md` 1)
- Por que importa: o único com entrega aberta (em parte) e utilidade sob ataque. Falta: o adversário é agente externo, não membro do time; a utilidade não é validada contra humano.
- Para o paper: relacionados da medida (um dos três a citar, com o eixo que lhe falta)

#### An, H. et al. (2026). ACIArena: Toward Unified Evaluation for Agent Cascading Injection (ex-MASpi).
- Identificador: DOI 10.18653/v1/2026.acl-long.457; arXiv 2604.07775
- Publicação: ACL 2026 Long, pp. 10049-10066 (ACL Anthology), revisado
- Arquivo local: `docs/refs/auditoria-quali/an2026-aciarena-maspi.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: seis sistemas multiagentes, "Utility under Attack (UA)" (§4); "we avoid domains that rely on open-ended evaluations" (§3); κ 0,92 valida o juiz de ataque, não a utilidade (`pesquisa-utilidade-sob-ataque/SINTESE.md` 1 e P2)
- Por que importa: multiagente com utilidade sob ataque, revisado. Falta: tarefas verificáveis (evita entrega aberta de propósito) e utilidade sem validação humana.
- Para o paper: relacionados da medida; a frase sobre evitar entrega aberta apoia a C10

#### Sehwag et al. (2026). ASPI: Seeking Ambiguity Clarification Amplifies Prompt Injection Vulnerability in LLM Agents.
- Identificador: arXiv 2605.17324
- Publicação: preprint (Scale AI)
- Arquivo local: `docs/refs/auditoria-quali/sehwag2026-aspi.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: 200 episódios atacados, 3 avaliadores, κ humano-LLM 0,540 e Fleiss 0,505 para utilidade (Ap. F.7); "agreement is lower [...] reflecting the more subjective nature of utility judgments" (`pesquisa-utilidade-sob-ataque/SINTESE.md` 1)
- Por que importa: o único que valida um rótulo de utilidade sob ataque contra humanos. Falta: agente único, cegueira não declarada, sem fase de desenvolvimento descrita. Sugere esperar κ moderado entre humanos (medir autor × Pedro primeiro).
- Para o paper: relacionados da medida; expectativa de κ para a validação

#### Khalifa, M. et al. (2026). Gaming the Judge: How Unfaithful Chain-of-Thought Can Undermine Agent Evaluation.
- Identificador: DOI 10.18653/2026.findings-emnlp.1636
- Publicação: Findings of EMNLP 2026, pp. 34789-34825 (ACL Anthology), revisado
- Arquivo local: `docs/refs/auditoria-quali/khalifa2026-gaming-judge.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: reescrever só o raciocínio do agente sobe o falso positivo de juízes de tarefa até 117% (relativo), em 800 trajetórias web; corrige o relatório do Claude (`pesquisa-utilidade-sob-ataque/SINTESE.md` P5 e 3)
- Por que importa: precedente revisado de manipulação de juiz de tarefa numa avaliação offline. Falta: não é injeção vinda de agente adversário dentro do episódio, que é o teste da M8.5.
- Para o paper: método (teste de contaminação do juiz); ameaça à validade

#### Zhu, Y. et al. (2025). Establishing Best Practices for Building Rigorous Agentic Benchmarks (ABC).
- Identificador: arXiv 2507.02825 (v5)
- Publicação: NeurIPS 2025 (pôster, lista do neurips.cc), revisado
- Arquivo local: `docs/refs/auditoria-quali/zhu2025-abc-checklist.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: "τ-bench counts empty responses as successful"; juiz LLM do WebArena sem validação, "1.4–5.2% performance overestimate" (resumo) (`pesquisa-utilidade-sob-ataque/SINTESE.md` P4)
- Por que importa: apoio revisado à C8 (o proxy otimista, κ 0,15) e à C10.
- Para o paper: introdução e método (por que validar a medida)

#### Lin, J. et al. (2026). VIGIL: Defending LLM Agents Against Tool Stream Injection via Verify-Before-Commit.
- Identificador: DOI 10.18653/v1/2026.acl-long.443
- Publicação: ACL 2026 Long, pp. 9764-9785 (ACL Anthology), revisado
- Arquivo local: `docs/refs/auditoria-quali/lin2026-vigil.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: UA estrita, "completes the user task while simultaneously neutralizing the malicious instruction" (§5.1) (`pesquisa-utilidade-sob-ataque/SINTESE.md` P1)
- Por que importa: mais um que mede utilidade sob ataque; agente único, tarefa verificável.
- Para o paper: relacionados da medida; relevância média

#### Zhang et al. (2025). MCP Security Bench (MSB): Benchmarking Attacks Against Model Context Protocol.
- Identificador: arXiv 2510.15994 (v2)
- Publicação: ICLR 2026 (pôster, lista do iclr.cc), revisado
- Arquivo local: `docs/refs/auditoria-quali/zhang2025-msb.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: PUA e NRP = PUA × (1 − ASR) (§5.2) (`pesquisa-utilidade-sob-ataque/SINTESE.md` P1)
- Por que importa: utilidade sob ataque por função determinística; agente único.
- Para o paper: relacionados da medida; relevância média

#### Advani, L. (2026). From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents.
- Identificador: arXiv 2606.09863
- Publicação: preprint (o workshop FAGEN do ICML 2026 não é arquivado nem lista aceitos)
- Arquivo local: `docs/refs/auditoria-quali/advani2026-false-success.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: nenhum juiz passa de AUROC 0,65 na detecção de falso sucesso no τ²-bench; "judges do not lack information, they fail to use it" (§4.3); o κ 0,86 é humano × regex, não entre humanos (`pesquisa-utilidade-sob-ataque/SINTESE.md` P4)
- Por que importa: o juiz sozinho não detecta falso "concluído"; apoia o E com regras.
- Para o paper: método, como trabalho recente

#### Zarif, F. et al. (2026). Ignored, Not Refused: What Low Prompt-Injection Success Rates Hide in Small Tool-Using Agents.
- Identificador: arXiv 2610.23254
- Publicação: preprint
- Arquivo local: `docs/refs/auditoria-quali/zarif2026-ignored.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: "In 21.7% of AgentDojo episodes, the agent stays safe but does not complete the user's task (S0 U0)" (§1); a mesma observação da C6, em agente único (`pesquisa-utilidade-sob-ataque/SINTESE.md` P6)
- Por que importa: tira do quadrante a pretensão de novidade; ele entra como ferramenta, citando este.
- Para o paper: relacionados (C6), como trabalho recente

#### Demais conferidos na pesquisa da utilidade (relevância baixa, todos preprints, conferidos no PDF em 24/11/2026)
- Nagaraja, N. et al. (2026). *When Prompts Control Robots: Prompt Injection Attacks in Multi-Agent Robotic Systems*. arXiv 2608.00747. Arquivo: `auditoria-quali/nagaraja2026-robots.pdf`. Quatro desfechos verificados por estado em multiagente robótico (P6). Para o paper: relacionados (C6).
- Nguyen, T. D. et al. (2026). *INFUSE: A Unified Surface Benchmark for Indirect Prompt Injection in Agentic Systems*. arXiv 2610.20776. Arquivo: `auditoria-quali/nguyen2026-infuse.pdf`. Utilidade sob ataque; 219 itens, três anotadores, "judge outputs hidden", κ 0,851, mas para o ASR (P1, P3).
- Li, H. et al. (2026). *AgentDyn: Are Your Agent Security Defenses Deployable in Real-World Dynamic Environments?* arXiv 2602.03117. Arquivo: `auditoria-quali/li2026-agentdyn.pdf`. UuA em tarefas "open-ended" no sentido de replanejamento, não de entrega aberta (P1).
- Gao, Y. (2026). *How Reliable Is Your Jailbreak Judge?* arXiv 2606.25487. Arquivo: `auditoria-quali/gao2026-jailbreak-judge.pdf`. Juízes de ASR mudam de veredito de 57% a 100% das vezes com moldura benigna (P5).
- Terekhov, M. et al. (2025). *Adaptive Attacks on Trusted Monitors Subvert AI Control Protocols*. arXiv 2510.09462. Arquivo: `auditoria-quali/terekhov2025-adaptive-monitors.pdf`. Monitor em tempo de execução: 375 de 375 rotulados como benignos (P5).
- Isbarov, J.; Kantarcioglu, M. (2026). *Bypassing AI Control Protocols via Agent-as-a-Proxy Attacks*. arXiv 2602.05066. Arquivo: `auditoria-quali/isbarov2026-agent-proxy.pdf`. Os 99,0% são contra PromptGuard 2 + AlignmentCheck juntos (P5).
- Remedios et al. (2026). *Red-Teaming Auto Mode: Improving Blocking Classifiers Against Malign Coding Agents*. arXiv 2609.19587. Arquivo: `auditoria-quali/remedios2026-auto-mode.pdf`. Monitor em tempo de execução, 79% (P5).
- Niu et al. (2026). *Scope-Gap Injection: Exploiting Evaluator Channel Blind Spots*. arXiv 2610.34777. Arquivo: `auditoria-quali/niu2026-scope-gap.pdf`. Evasão por canal não inspecionado.
- Todas: útil em 2026-11-24 em `pesquisa-utilidade-sob-ataque/SINTESE.md` (seção indicada); para o paper, relacionados (juiz contaminável, C6), como trabalho recente.

### Método: controle estatístico e delineamento na avaliação

#### Messing, S. (2026). Hidden Measurement Error in LLM Pipelines Distorts Annotation, Evaluation, and Benchmarking.
- Identificador: arXiv 2604.11581 (v8; a v1 também está guardada)
- Publicação: NeurIPS 2026, conferência principal (pôster; rodapé da v8), revisado. Citar a v8 ou a dos anais
- Arquivo local: `docs/refs/auditoria-quali/messing2026-hidden-measurement.pdf` (v8) e `messing2026-hidden-measurement-v1.pdf`
- Conferido no original: sim (2026-11-24), na v8
- Quando foi útil:
  - 2026-11-24: modelo misto com item, variante de prompt e réplica aleatórios, por REML (3.1, 3.3); "naive standard errors are 53 - 70% smaller than the corrected SE" (resumo, só na v8); no AILuminate, painel de juízes 43,8% e redação < 0,5% da variância (Seção 3); "rerun-only intervals as lower bounds" (Seção 5) (`pesquisa-cep-doe-avaliacao/SINTESE.md` 1 e 2)
  - 2026-11-24: rebaixa a decomposição R&R de contribuição para método (`06-qualificacao/REVISAO_METODOLOGICA.md` 1.5; `MAPA_DE_REIVINDICACOES.md` Seção 8)
- Por que importa: precedente revisado da decomposição de variância que a QA1 pede. Falta: ataque, multiagente; quem varia é o juiz, não o sistema. O achado de que réplicas pesam < 0,5% é a objeção mais forte à premissa "repetir importa" e tem de ser discutido.
- Para o paper: método (seguir a decomposição dele); ameaça à validade (réplicas pouco importam nele)

#### Helm, H.; Priebe, C.; Duderstadt, B. (2026). Control Charts for Multi-Agent Systems.
- Identificador: arXiv 2605.11135 (v2; a v1 também está guardada)
- Publicação: NeurIPS 2026, conferência principal (pôster, OpenReview e rodapé da v2), revisado. Citar a v2
- Arquivo local: `docs/refs/auditoria-quali/helm2026-control-charts.pdf` (v2) e `helm2026-control-charts-v1.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: Shewhart sobre a trajetória do "iso-mirror" para **monitorar** multiagente; "monitors with adaptive baselines admit slow adversaries" (resumo); CUSUM só na v2 (5.1); sem LLM real nas réplicas (nota 3) (`pesquisa-cep-doe-avaliacao/SINTESE.md` 1 e 2)
- Por que importa: o mais próximo de cartas de controle em multiagente com adversário. Falta: carta sobre taxa de sucesso de ataque e avaliação experimental com réplicas. Dá o argumento dos limites fixos (Fase I) num benchmark.
- Para o paper: relacionados do método; resposta à objeção (b) da `REVISAO_METODOLOGICA.md` 1.2

#### Luo et al. (2026). Voices Across Registers: Corpus-Conditioned Vernacular Jailbreaks against Aligned LLMs.
- Identificador: DOI 10.18653/2026.emnlp-main.1148
- Publicação: EMNLP 2026, pp. 26314-26338 (ACL Anthology), revisado
- Arquivo local: `docs/refs/auditoria-quali/luo2026-voices-registers.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: "a factorial decomposition shows the gain is carried by register rather than length or structure" (resumo), logística GEE agrupada por comportamento (`pesquisa-cep-doe-avaliacao/SINTESE.md` 1 e 2)
- Por que importa: precedente revisado de fatorial em segurança, e a análise (logística com agrupamento) que a M4 recomenda para o nosso 2². Falta: agentes e multiagente.
- Para o paper: relacionados do método; modelo de análise do fatorial

#### Tian, Z. et al. (2026). Beyond Benchmarks: Toward Causally Faithful Evaluation of Large Language Models.
- Identificador: PMLR 306:120838-120872
- Publicação: ICML 2026 (PMLR), revisado
- Arquivo local: `docs/refs/auditoria-quali/tian2026-causally-faithful.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: ANOVA sobre um 2^10 citando o Montgomery; derruba "ninguém aplicou fatorial" da C5 (`pesquisa-cep-doe-avaliacao/SINTESE.md` 1 e 5)
- Por que importa: fatorial e ANOVA em avaliação de LLM já são revisados. Falta: segurança, ataque, multiagente.
- Para o paper: relacionados do método

#### Lukassen, F. et al. (2026). CAFE: A Compound-AI Factorial Evaluation Framework.
- Identificador: DOI 10.18653/2026.emnlp-demos.50
- Publicação: EMNLP 2026 System Demonstrations (ACL Anthology), revisado (demos)
- Arquivo local: `docs/refs/auditoria-quali/lukassen2026-cafe.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: fatorial com efeitos mistos em pipeline RAG (`pesquisa-cep-doe-avaliacao/SINTESE.md` 1 e 6)
- Por que importa: ferramenta de fatorial para sistemas compostos; sem ataque. Relevância média.
- Para o paper: relacionados do método

#### Bogdanov et al. (2026). Evaluation of Multi-Turn Consistency in LLM Agents.
- Identificador: arXiv 2609.29508
- Publicação: workshop do ICLR 2026 (Logical Reasoning of LLMs, cabeçalho do PDF), revisado (workshop); o relatório do ChatGPT dava ICLR principal e outra primeira autora
- Arquivo local: `docs/refs/auditoria-quali/bogdanov2026-multiturn-consistency.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: fatorial completo em multiagente, sem ataque (`pesquisa-cep-doe-avaliacao/SINTESE.md` 5 e 6)
- Por que importa: fatorial sobre consistência de agentes; falta o ataque.
- Para o paper: relacionados do método; relevância média

#### Broadwater, K. (2026). Evaluating Reliability Gaps in Large Language Model Safety via Repeated Prompt Sampling.
- Identificador: DOI 10.1109/CCAI69603.2026.11642011; arXiv 2604.09606
- Publicação: IEEE CCAI 2026, pp. 930-938 (Crossref), revisado. O PDF local é a v1 do arXiv
- Arquivo local: `docs/refs/auditoria-quali/broadwater2026-reliability-gaps.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: falhas de segurança como Bernoulli e binomial sob amostragem repetida, em chat (`pesquisa-cep-doe-avaliacao/SINTESE.md` 4)
- Por que importa: o modelo de Bernoulli do veredito repetido, revisado; em chat. Relevância baixa.
- Para o paper: método (modelo do veredito)

#### Blackwell, R. E.; Barry, J.; Cohn, A. G. (2024). Towards Reproducible LLM Evaluation: Quantifying Uncertainty in LLM Benchmark Scores.
- Identificador: arXiv 2410.03492 (v2)
- Publicação: preprint
- Arquivo local: `docs/refs/auditoria-quali/blackwell2024-reproducible.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: com T = 0 e semente fixa, o mesmo GPT-3.5 pela Azure e pela OpenAI deu 0,833 e 0,840, "statistically significantly different (t = 2.51, p = 0.013)" (Seção 4); **recomenda** T = 0, ao contrário do Miller (`pesquisa-cep-doe-avaliacao/SINTESE.md` 3; `REVISAO_METODOLOGICA.md` M9)
- Por que importa: evidência de que o provedor muda a distribuição (objeção b) e a posição contrária sobre temperatura, a declarar.
- Para o paper: método (temperatura); ameaça à validade (modelo por trás da API)

#### Demais conferidos na pesquisa de método (relevância baixa ou média)
- Wang, T. et al. (2026). *MMJailBench: A Factorized Benchmark for Disentangling Multimodal Jailbreak Vulnerabilities*. arXiv 2608.25490, preprint. Arquivo: `auditoria-quali/wang2026-mmjailbench.pdf`. Conferido no PDF: 272 × 6 × 5 × 2 sem ANOVA nem repetição; não é o precedente de fatorial (o Luo é) (Seção 5).
- Huang et al. (2025). *GuidedBench: Measuring and Mitigating the Evaluation Discrepancies of Jailbreak Methods*. arXiv 2502.16903 (v3); ICLR 2026 pelo cabeçalho do PDF, anais não abertos. Arquivo: `auditoria-quali/huang2025-guidedbench.pdf`. Modelo misto `S ∼ 1 + (1|victim) + (1|topic)` para juízes de jailbreak (Ap. E.2) (Seção 4).
- Madaan, L. et al. (2024). *Quantifying Variance in Evaluation Benchmarks*. arXiv 2406.10229; workshop RegML do NeurIPS 2024. Arquivo: `auditoria-quali/madaan2024-variance.pdf`. A "seed variance" é de semente de treino, não de inferência (2.1); pouco útil (Seção 4).
- Feng, J. et al. (2024). *Designing monitoring strategies for deployed machine learning algorithms: navigating performativity through a causal lens*. PMLR 236:587-608, CLeaR 2024, revisado. Arquivo: `auditoria-quali/feng2024-monitoring-performativity.pdf`. SPC e causalidade no monitoramento de ML implantado (Seção 6).
- Todas: conferido no original sim (2026-11-24); útil em 2026-11-24 em `pesquisa-cep-doe-avaliacao/SINTESE.md` (seção indicada); para o paper, relacionados do método.

#### Pistas citadas pelo Messing, baixadas em 24/11/2026 (ler antes de citar)
- Wang, S. I. (2025). *Measuring all the noises of LLM Evals*. arXiv 2512.21326 (v3, 13/10/2026); preprint, local não conferido. Arquivo: `auditoria-quali/wang2025-noises-llm-evals.pdf`. Conferido no original: só resumo (ruído de predição, ruído de dados e ruído total pela lei da variância total). Útil em 2026-11-24 como pista (`pesquisa-cep-doe-avaliacao/SINTESE.md` 4). Para o paper: método, se lido.
- Keller, D.; Kwegyir-Aggrey, K.; Steed, R.; Rao, A. K.; Sharp, J. L.; Bergman, A. S. (2026). *Expanding the AI Evaluation Toolbox with Statistical Models* (NIST AI 800-3). DOI 10.6028/NIST.AI.800-3; relatório técnico do NIST, fevereiro de 2026 (aprovado pelo Editorial Review Board em 29/01/2026). Arquivo: `auditoria-quali/keller2026-nist-ai-800-3.pdf`. Conferido no original: só resumo e sumário: confirma que trata de GLMM para estimar acurácia generalizada e a incerteza (cap. 4 e 5); os componentes entre e dentro de itens ainda não foram conferidos no texto. Útil em 2026-11-24 (`pesquisa-cep-doe-avaliacao/SINTESE.md` 4 e 7). Por que importa: candidato a referência institucional da análise da M4 e da 1.5 da `REVISAO_METODOLOGICA.md`. Para o paper: método, depois de lido.

#### Periódicos de estatística (texto não aberto; só metadados e resumo)
Todos com acesso pago (ou bloqueado ao download automático) e **não baixados**; conferidos em 24/11/2026
pelo Crossref ou PubMed, em `pesquisa-cep-doe-avaliacao/SINTESE.md` 3 e 6. Não citar frase sem abrir
o artigo.
- Steiner, Cook, Farewell, Treasure (2000). *Monitoring surgical performance using risk-adjusted cumulative sum charts*. *Biostatistics* 1(4):441-452, DOI 10.1093/biostatistics/1.4.441 (PubMed). Cartas ajustadas ao risco, "ideally suited for settings where there is a variable mix of patients" (resumo): resposta à objeção (a), casos heterogêneos. Para o paper: método (`REVISAO_METODOLOGICA.md` 1).
- Steiner, Cook, Farewell (2001). *Risk-adjusted monitoring of binary surgical outcomes*. *Medical Decision Making* 21(3):163-169, PMID 11386623. A versão para desfecho binário. Para o paper: método.
- Grigg, Farewell (2004). *An Overview of Risk-Adjusted Charts*. *JRSS A* 167(3):523-539, DOI 10.1111/j.1467-985x.2004.0apm2.x. Revisão. Para o paper: método.
- Szarka, Woodall (2011). *A Review and Perspective on Surveillance of Bernoulli Processes*. *QREI* 27(6):735-752, DOI 10.1002/qre.1256. Proporção perto de zero (ASR com defesa ligada); no ISQC, 10.11.7, p. 501. Para o paper: método.
- Woodall (2000). *Controversies and Contradictions in Statistical Process Control*. *JQT* 32(4):341-350, DOI 10.1080/00224065.2000.11980013. A frase sobre a carta MR "ineffective" **não foi conferida**: não citar sem abrir.
- Woodall (2006). *The Use of Control Charts in Health-Care and Public-Health Surveillance*. *JQT* 38(2), DOI 10.1080/00224065.2006.11918593. Relevância baixa.
- Zwetsloot, Jones-Farmer, Woodall (2023). *Monitoring univariate processes using control charts* (título curto da síntese). *Quality Engineering* 36(3), DOI 10.1080/08982112.2023.2238049. **Acesso aberto**, mas a Taylor & Francis devolveu 403 ao download automático em 24/11: baixar à mão pelo navegador e salvar como `auditoria-quali/zwetsloot2023-control-charts.pdf`. Fase I e II. Para o paper: método.
- Alwan, Roberts (1988). *Time-Series Modeling for Statistical Process Control*. *JBES* 6(1), DOI 10.1080/07350015.1988.10509640. Autocorrelação (objeção c). Relevância baixa.

#### Não citar
- Żatuchin, D. (2026). arXiv 2607.13304. A v1 (*Where Does the Noise Come From? A Variance-Components Decomposition...*) e a v2 (*Query Language Sensitivity in Automated Sentiment Scores...*) estão em `auditoria-quali/zatuchin2026-noise-v{1,2}.pdf`. A v2 mudou o título e retirou afirmações (`pesquisa-cep-doe-avaliacao/SINTESE.md` 6).

## Avaliação híbrida (conferida em 20/10/2026, registrada em 24/11/2026)

Obras conferidas em `docs/04-paper/pesquisa-avaliacao-hibrida/SINTESE.md` (desenho da medida B + C,
`docs/02-experimentos/MEDIDA_UTILIDADE_HIBRIDA.md`). Os PDFs usados em 20/10 não ficaram guardados;
os de arXiv foram baixados de novo em 24/11/2026 para `docs/refs/auditoria-quali/`. AgentDojo,
AgentRewardBench, BAD-ACTS e as que já estavam na tabela da pesquisa do juiz (CheckEval, TICK,
Zheng et al., JudgeDeceiver) ganharam linha nas suas entradas ou já a tinham. O campo "Publicação"
vem da síntese e do cabeçalho do PDF, não dos anais.

### Andriushchenko, M. et al. (2024). AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents.
- Identificador: arXiv 2410.09024 (v3)
- Publicação: ICLR 2025 (cabeçalho do PDF), revisado
- Arquivo local: `docs/refs/auditoria-quali/andriushchenko2024-agentharm.pdf`
- Conferido no original: sim (2026-10-20)
- Quando foi útil:
  - 2026-10-20: "The majority of our grading criteria checks are predefined, manually written conditions [...] A semantic LLM judge is used whenever it is necessary" (§3.1.3); um juiz por pergunta; o juiz não vê mensagens do usuário (apêndice) (`pesquisa-avaliacao-hibrida/SINTESE.md` 1 e 2; `MEDIDA_UTILIDADE_HIBRIDA.md`, referências)
- Por que importa: o precedente principal da divisão B + C, em benchmark de segurança, com a mesma justificativa. Agrega por fração (crédito parcial), não por E; validação só por exame manual.
- Para o paper: método (divisão do trabalho entre código e juiz)

### Xu, F. F. et al. (2024). TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks.
- Identificador: arXiv 2412.14161 (v3)
- Publicação: preprint pela síntese (não conferido nos anais)
- Arquivo local: `docs/refs/auditoria-quali/xu2024-theagentcompany.pdf`
- Conferido no original: sim (2026-10-20)
- Quando foi útil:
  - 2026-10-20: "we first use deterministic keyword matches and then use LLM as a fallback" (ap. E); sucesso só se todos os checkpoints passam (§4.1) (`pesquisa-avaliacao-hibrida/SINTESE.md` 2)
- Por que importa: precedente do escalonamento código primeiro, juiz depois, e do E para o binário.
- Para o paper: método

### Yu, B. et al. (2026). CXBench: A Benchmark for Process-Compliant LLM Agents in Regulated Customer-Experience Workflows.
- Identificador: arXiv 2610.25954
- Publicação: preprint (submetido em 19/10/2026)
- Arquivo local: `docs/refs/auditoria-quali/yu2026-cxbench.pdf`
- Conferido no original: sim (2026-10-20)
- Quando foi útil:
  - 2026-10-20: "Both the deterministic component and the LLM-judge component must pass" (§3); juiz calibrado em 120 traços, "not an independent held-out validation set" (`pesquisa-avaliacao-hibrida/SINTESE.md` 1 a 3)
- Por que importa: precedente direto do E lógico entre código e juiz; reconhece a falta de teste separado, que o lote 2 cobre.
- Para o paper: método (regra de combinação); posicionamento da validação

### Chen, T. et al. (2026). KnowU-Bench: Towards Interactive, Proactive, and Personalized Mobile Agent Evaluation.
- Identificador: arXiv 2604.08455
- Publicação: preprint
- Arquivo local: `docs/refs/auditoria-quali/chen2026-knowu-bench.pdf`
- Conferido no original: sim (2026-10-20)
- Quando foi útil:
  - 2026-10-20: média ponderada S = λ S_rule + (1 − λ) S_llm, com λ pela proporção de requisitos (§3.4), mas sucesso só com S > 0,99 (§4.1); validação em 26 trajetórias, sem κ (`pesquisa-avaliacao-hibrida/SINTESE.md` 1 a 3)
- Por que importa: o único precedente de média ponderada, e na prática exige as duas partes inteiras; é a versão mais forte da sugestão da orientadora.
- Para o paper: método (por que E e não média)

### Yao, S. et al. (2024). τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.
- Identificador: arXiv 2406.12045
- Publicação: preprint pela síntese (não conferido nos anais)
- Arquivo local: `docs/refs/auditoria-quali/yao2024-tau-bench.pdf`
- Conferido no original: sim (2026-10-20)
- Quando foi útil:
  - 2026-10-20: "r = r_action × r_output ∈ {0, 1}", produto de binários (`pesquisa-avaliacao-hibrida/SINTESE.md` 2)
  - 2026-11-24: o ABC (Zhu et al.) mostra que o τ-bench conta resposta vazia como sucesso (`pesquisa-utilidade-sob-ataque/SINTESE.md` P4)
- Por que importa: E como produto; e exemplo de medida de sucesso que superestima.
- Para o paper: método; ameaça à validade (medidas que superestimam)

### Levy, I. et al. (2024). ST-WebAgentBench: A Benchmark for Evaluating Safety and Trustworthiness in Web Agents.
- Identificador: arXiv 2410.06703 (v7)
- Publicação: ICLR 2026 (cabeçalho do PDF), revisado
- Arquivo local: `docs/refs/auditoria-quali/levy2024-st-webagentbench.pdf`
- Conferido no original: sim (2026-10-20)
- Quando foi útil:
  - 2026-10-20: "CuP_t = C_t 1[Σ V = 0]", sucesso só com zero violações (§3.3) (`pesquisa-avaliacao-hibrida/SINTESE.md` 2)
- Por que importa: portão, o mesmo princípio do E.
- Para o paper: método

### Zhou, S. et al. (2023). WebArena: A Realistic Web Environment for Building Autonomous Agents.
- Identificador: arXiv 2307.13854 (v4)
- Publicação: ICLR 2024 (cabeçalho do PDF), revisado
- Arquivo local: `docs/refs/auditoria-quali/zhou2023-webarena.pdf`
- Conferido no original: sim (2026-10-20)
- Quando foi útil:
  - 2026-10-20: fuzzy_match com gpt-4-0613, validado em 40 exemplos (39 iguais ao humano) (§3.2, ap. A.8) (`pesquisa-avaliacao-hibrida/SINTESE.md` 2)
  - 2026-11-24: juiz sem validação, superestimação de 1,4 a 5,2% segundo o ABC (`pesquisa-utilidade-sob-ataque/SINTESE.md` P4)
- Por que importa: híbrido com validação pequena; e onde o BenchJack mostrou a injeção no juiz.
- Para o paper: método; ameaça à validade

### Ruan, Y. et al. (2023). Identifying the Risks of LM Agents with an LM-Emulated Sandbox (ToolEmu).
- Identificador: arXiv 2309.15817 (v2)
- Publicação: ICLR 2024 (cabeçalho do PDF), revisado
- Arquivo local: `docs/refs/auditoria-quali/ruan2023-toolemu.pdf`
- Conferido no original: sim (2026-10-20)
- Quando foi útil:
  - 2026-10-20: κ juiz × humano 0,478 e humano × humano 0,480 (segurança); 0,543 e 0,521 (utilidade) (§4.2) (`pesquisa-avaliacao-hibrida/SINTESE.md` 2 e 4)
- Por que importa: o LLM pode igualar humanos, com κ moderado; referência para ler o κ da validação.
- Para o paper: método (expectativa de κ)

### Wang et al. (2026). Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack.
- Identificador: arXiv 2605.12673
- Publicação: preprint
- Arquivo local: `docs/refs/auditoria-quali/wang2026-benchjack.pdf`
- Conferido no original: sim (2026-10-20)
- Quando foi útil:
  - 2026-10-20: no WebArena "The agent's stop-string is interpolated verbatim into the judge's prompt; there are no delimiters" (§4.1, ap. B.4); notas quase perfeitas em 9 de 10 benchmarks sem resolver tarefa (resumo) (`pesquisa-avaliacao-hibrida/SINTESE.md` 1 e 2)
- Por que importa: a injeção no juiz é real e documentada; a correção (delimitar, limitar tamanho, exigir linha de veredito) é a mitigação do nosso desenho.
- Para o paper: método (mitigações do juiz); ameaça à validade

### Lidos só no resumo (20/10/2026)
- Pan, T. et al. (2026). *RubricEval: A Rubric-Level Meta-Evaluation Benchmark for LLM Judges in Instruction Following*. arXiv 2603.25133, preprint. Arquivo: `auditoria-quali/pan2026-rubriceval.pdf`. "even GPT-4o [...] achieves only 55.97% on Hard subset": ressalva de que decompor não resolve tudo; corrigiu o slide 3 da reunião 5. Para o paper: método (ressalva às perguntas atômicas).
- Saito, K. et al. (2023). *Verbosity Bias in Preference Labeling by Large Language Models*. arXiv 2310.10076, preprint. Arquivo: `auditoria-quali/saito2023-verbosity-bias.pdf`. Viés de verbosidade. Para o paper: ameaça à validade do juiz.
- Panickssery, A.; Bowman, S. R.; Feng, S. (2024). *LLM Evaluators Recognize and Favor Their Own Generations*. arXiv 2404.13076; NeurIPS 2024 segundo a pesquisa da amostra (não conferido). Arquivo: `auditoria-quali/panickssery2024-self-preference.pdf`. Autopreferência; motivo para o juiz ser de fora das famílias avaliadas. Para o paper: método.
- Raina, V.; Liusie, A.; Gales, M. (2024). *Is LLM-as-a-Judge Robust? Investigating Universal Adversarial Attacks on Zero-shot LLM Assessment*. arXiv 2402.14016; EMNLP 2024 pela síntese. Arquivo: `auditoria-quali/raina2024-judge-robust.pdf`. Frases adversárias curtas inflam a nota. Para o paper: ameaça à validade.
- Todas: conferido no original só resumo; útil em 2026-10-20 em `pesquisa-avaliacao-hibrida/SINTESE.md` 2.

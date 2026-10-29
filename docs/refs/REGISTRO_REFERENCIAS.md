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
- Arquivo local: docs/refs/<nome> (ou "não baixado")
- Conferido no original: sim (data) / não (só resumo, só relatório de pesquisa)
- Quando foi útil:
  - <AAAA-MM-DD>: <para que decisão ou texto>, em <arquivo do repositório, seção>
- Por que importa: <uma ou duas frases>
- Para o paper: trabalhos relacionados / método / ameaça à validade / comparação; <onde entra>
```

## Pendente

Preencher com as referências já usadas antes deste registro existir: o BAD-ACTS (v1, v2, v3), Li et
al. (2026) e as conferidas em `docs/04-paper/pesquisa-avaliacao-hibrida/SINTESE.md`.

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

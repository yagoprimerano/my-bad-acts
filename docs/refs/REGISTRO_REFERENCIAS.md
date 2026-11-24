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

O BAD-ACTS (v1, v2, v3) e o Li et al. (2026) foram registrados em 24/11/2026 (seção "Auditoria para
a qualificação"). Falta: as conferidas em `docs/04-paper/pesquisa-avaliacao-hibrida/SINTESE.md`, e o
campo "Publicação" nas entradas anteriores a 24/11.

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
- Publicação: v3: COLM 2026, revisada por pares; v1 e v2 preprint
- Arquivo local: `docs/refs/auditoria-quali/badacts-v{1,2,3}.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - antes de 24/11/2026: base de todo o fork (`CLAUDE.md`)
  - 2026-10-28: a medida de qualidade 1-5 só existe na v3 (`04-paper/NOVIDADE_E_POSICIONAMENTO.md` 9)
  - 2026-11-24: conferido que **repete cada experimento três vezes e reporta média e erro padrão** (nas três versões) e que o juiz de qualidade da v3 não tem validação humana (`06-qualificacao/AUDITORIA_REFERENCIAS.md` 2.3)
- Por que importa: é o benchmark estendido. Números mudam muito entre v2 e v3 (ASR de 40% a 90% na v3): citar sempre a versão.
- Para o paper: método e relacionados; nunca citar seus números pelo resumo do Li et al.

### Li, M. Q.; Fung, B. C. M. et al. (2026). Taxonomy and Consistency Analysis of Safety Benchmarks for AI Agents.
- Identificador: arXiv 2605.16282 (11/04/2026)
- Publicação: preprint (cs.CY)
- Arquivo local: `docs/refs/li2026-taxonomy-safety-benchmarks.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - antes de 24/11/2026: âncora da lacuna R10 (`CLAUDE.md`, monografia de julho)
  - 2026-11-23: conferido R10 = 0 primários e 7 parciais (BAD-ACTS entre eles), W de Kendall = 0,10 (p = 0,94) (`06-qualificacao/MAPA_DE_REIVINDICACOES.md` C1 a C3)
  - 2026-11-24: o resumo que faz do BAD-ACTS tem número que não existe ("53% Llama-3.1-8B")
- Por que importa: a taxonomia que define R10 e mostra que nenhum benchmark é primário nela.
- Para o paper: introdução e lacuna; fonte única e preprint, citar junto do Rabanser et al.

### Rabanser, S. et al. (2026). Towards a Science of AI Agent Reliability.
- Identificador: arXiv 2602.16666 (v3)
- Publicação: ICML 2026, segundo o comentário do arXiv; confirmar nos anais
- Arquivo local: `docs/refs/auditoria-quali/rabanser2026-agent-reliability.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: 4 dimensões, 12 métricas, **15 modelos** (não 14), K = 5 execuções e paráfrases; "We do not evaluate adversarial attacks" (p. 2); robustez a adversários e confiabilidade multiagente como problemas abertos (p. 24-25) (`AUDITORIA_REFERENCIAS.md` 2.1)
- Por que importa: concorrente conceitual mais forte e, ao mesmo tempo, a melhor sustentação revisada por pares da lacuna.
- Para o paper: relacionados e lacuna

### Raj, H. et al. (2026). Consistency as a Testable Property: Statistical Methods to Evaluate AI Agent Reliability.
- Identificador: arXiv 2605.10516 (v2)
- Publicação: NeurIPS 2026 (rodapé de versão final no PDF); confirmar na lista de aceitos
- Arquivo local: `docs/refs/auditoria-quali/raj2026-consistency-testable.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: estatísticas U, consistência observável × interna; tem uma perturbação "injection" que é ruído e mede tarefa, não segurança; agente único
- Por que importa: o mais próximo do enquadramento estatístico; sem segurança sob ataque nem multiagente.
- Para o paper: relacionados

### Potamitis, N. et al. (2025). ReasonBENCH: Benchmarking the (In)Stability of LLM Reasoning.
- Identificador: arXiv 2512.07795 (v2)
- Publicação: preprint
- Arquivo local: `docs/refs/auditoria-quali/potamitis2025-reasonbench.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: 30 repetições por configuração com IC por bootstrap estratificado; "wins only 77% of head-to-head runs" (p. 1)
- Por que importa: precedente de repetição com IC; estratégias de raciocínio, sem ataque.
- Para o paper: relacionados

### Yagubyan, A. (2026). How Consistent Are LLM Agents? Measuring Behavioral Reproducibility in Multi-Step Tool-Calling.
- Identificador: arXiv 2605.28840
- Publicação: preprint, autor único independente
- Arquivo local: `docs/refs/auditoria-quali/yagubyan2026-how-consistent.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: 1.140 traços, IC de 95%, ANOVA de um fator; sem ataque e sem multiagente
- Por que importa: reprodutibilidade de agentes com ferramentas por repetição idêntica.
- Para o paper: relacionados; peso baixo (preprint, autor único)

### Lunardi, R. et al. (2025). On Robustness and Reliability of Benchmark-Based Evaluation of LLMs.
- Identificador: arXiv 2509.04013
- Publicação: ECAI 2025, segundo o comentário do arXiv (o PDF não traz)
- Arquivo local: `docs/refs/auditoria-quali/lunardi2025-robustness-benchmarks.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: paráfrase de 6 benchmarks, 34 LLMs, ranking estável e queda absoluta
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
- Publicação: preprint (Anthropic), autor único
- Arquivo local: `docs/refs/auditoria-quali/miller2024-error-bars.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: "evaluations are experiments" (p. 1); recomenda erro padrão agrupado, reamostrar respostas, diferenças pareadas e análise de poder; nada de cartas de controle ou fatorial
- Por que importa: a referência mais citada sobre estatística em avaliação de LLM; o erro padrão agrupado é parte da resposta à objeção de independência.
- Para o paper: método

### Xie, X. et al. (2023). Adversarial Client Detection via Non-parametric Subspace Monitoring in the Internet of Federated Things.
- Identificador: arXiv 2310.01537
- Publicação: preprint
- Arquivo local: `docs/refs/auditoria-quali/xie2023-federated-spc.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: CUSUM não paramétrico, cita o ISQC de Montgomery; detecção de ataque, não avaliação; não é LLM
- Por que importa: precedente de controle estatístico contra ataque, fora de LLM.
- Para o paper: relacionados do método

### Jia, Y. et al. (2021). Adversarial Attacks and Mitigation for Anomaly Detectors of Cyber-Physical Systems.
- Identificador: arXiv 2105.10707
- Publicação: International Journal of Critical Infrastructure Protection 34:100452 (2021), periódico
- Arquivo local: `docs/refs/auditoria-quali/jia2021-cps-cusum.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: CUSUM com UCL/LCL, mas é o detector que o artigo ataca, não a contribuição
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
- Publicação: NeurIPS 2024, Datasets and Benchmarks, revisada por pares
- Arquivo local: `docs/refs/auditoria-quali/agentdojo.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: utility under attack por função determinística sobre o estado do ambiente (§3.4); rejeita juiz LLM porque o ataque pode sequestrá-lo (p. 4); IC binomial; não declara repetições
- Por que importa: o único que mede utilidade sob ataque de fato; agente único.
- Para o paper: relacionados da medida; argumento a enfrentar no desenho do juiz

### Zhang, H. et al. (2025). Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents.
- Identificador: arXiv 2410.02644
- Publicação: ICLR 2025, revisada por pares
- Arquivo local: `docs/refs/auditoria-quali/asb.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: PNA sem ataque; NRP = PNA × (1 − ASR); tudo por chamada de ferramenta; não declara repetições
- Por que importa: combina utilidade sem ataque com ASR.
- Para o paper: relacionados da medida

### Kavathekar, I. et al. (2025). TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems.
- Identificador: arXiv 2511.05269
- Publicação: workshop MAS do ICML 2025, segundo o comentário do arXiv (o PDF diz "Preprint")
- Arquivo local: `docs/refs/auditoria-quali/tamas.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: ERS = média harmônica de segurança e PNA; **PNA medida sem ataque**, por chamada de ferramenta; juiz de segurança com F1 de 89,17% contra humano; não declara repetições
- Por que importa: o concorrente multiagente mais próximo da medida de utilidade.
- Para o paper: relacionados da medida

### Zhang, Z. et al. (2024). Agent-SafetyBench: Evaluating the Safety of LLM Agents.
- Identificador: arXiv 2412.14470 (v2)
- Publicação: preprint
- Arquivo local: `docs/refs/auditoria-quali/zhang2024-agent-safetybench.pdf`
- Conferido no original: sim (2026-11-24)
- Quando foi útil:
  - 2026-11-24: conferido: juiz de segurança ajustado (91,5% em 200 de outro modelo); utilidade por GPT-4o com 94% em validação manual sem n; agente único
- Por que importa: exemplo de juiz validado contra humano em agentes.
- Para o paper: relacionados da medida

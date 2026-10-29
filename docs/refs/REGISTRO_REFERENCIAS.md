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

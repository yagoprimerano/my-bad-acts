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
- Para o paper: método (leitura de controle de processo), citando o ISQC, não este manual.

# Reference material

## O que deve estar aqui

Os arquivos são gitignored, então existem apenas na máquina em que foram colocados à mão. Confira
antes de assumir que estão legíveis.

| Arquivo | O que fundamenta |
|---|---|
| Montgomery, *Design and Analysis of Experiments*, 8th ed. | Todo o desenho de `docs/02-experimentos/PLANO_EXPERIMENTAL.md` e os blocos da triagem: o fatorial 2² de Defesa × Perturbação (bloco F e `analyze_experiment_stats.py factorial`), réplica contra repetição (bloco A), tamanhos amostrais, e paráfrase como fator de ruído (blocos B1/B2 e o modo `noise`). |
| Montgomery, Ramírez & Ramírez, *Introduction to Statistical Quality Control* | A leitura de controle de processo: cartas de controle e repetibilidade em `analyze_experiment_stats.py spc`, explicadas linha a linha em `docs/03-metricas/METRICAS_ROBUSTEZ.md`. |

Quando aparecer uma dúvida de desenho ("quantas réplicas", "isso é fator ou ruído", "como leio esta
carta"), a resposta vem destes dois livros, e não de intuição estatística geral.

## Como adicionar outras referências

Drop reference PDFs (and similar) here to have them read/analyzed, e.g.:

    docs/refs/li-et-al-2026.pdf

Then ask, for example: "read docs/refs/li-et-al-2026.pdf and compare its robustness
section with our extensions".

Note: reference files themselves are gitignored (see .gitignore) to avoid committing
third-party/copyrighted material. Only this README is tracked.

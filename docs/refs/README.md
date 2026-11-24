# Reference material

## O que deve estar aqui

Os arquivos são gitignored, então existem apenas na máquina em que foram colocados à mão. Confira
antes de assumir que estão legíveis.

| Arquivo | O que fundamenta |
|---|---|
| Montgomery, *Design and Analysis of Experiments*, 8th ed. | Todo o desenho de `docs/02-experimentos/PLANO_EXPERIMENTAL.md` e os blocos da triagem: o fatorial 2² de Defesa × Perturbação (bloco F e `analyze_experiment_stats.py factorial`), réplica contra repetição (bloco A), tamanhos amostrais, e paráfrase como fator de ruído (blocos B1/B2 e o modo `noise`). |
| Montgomery, *Introduction to Statistical Quality Control*, 7ª ed. (`montgomery-isqc-7ed.pdf`; o `.epub` é só o *JMP Companion* de Ramírez & Ramírez) | A validação da medida de utilidade como estudo do sistema de medição (Seção 8.7) e a leitura de controle de processo: cartas de controle e repetibilidade em `analyze_experiment_stats.py spc`, explicadas linha a linha em `docs/03-metricas/METRICAS_ROBUSTEZ.md`. |

Quando aparecer uma dúvida de desenho ("quantas réplicas", "isso é fator ou ruído", "como leio esta
carta"), a resposta vem destes dois livros, e não de intuição estatística geral.

## O que é versionado e como recriar a pasta

Só três arquivos desta pasta vão para o git: este `README.md`, o `REGISTRO_REFERENCIAS.md` (para que
cada obra foi usada e quando) e o `MANIFESTO.csv` (uma linha por obra: arquivo local, título curto,
ano, identificador, URL direta do PDF quando é de acesso aberto, tipo de acesso e os documentos do
repositório que a citam). Os PDFs, livros e demais arquivos **não** vão para o git, e não devem sair
do `.gitignore`: o repositório no GitHub é público, e redistribuir artigos e livros de terceiros
violaria direitos autorais (mesmo os de acesso aberto têm licenças próprias).

Numa máquina nova, depois do `git clone`:

    python scripts/fetch_refs.py --dry-run   # lista o que falta e o que não é baixável
    python scripts/fetch_refs.py             # baixa o que é aberto e ainda não existe

O script usa só a biblioteca padrão, nunca sobrescreve um arquivo existente e espera 3 s entre
downloads. O que ele não baixa (`acesso` = `pago`, `livro` ou `bloqueado`) tem de ser obtido à mão:
os pagos pela biblioteca da USP, os bloqueados (acesso aberto, mas a editora recusa download
automático) pelo navegador, e nunca por fonte pirata. Ao baixar uma obra nova, acrescente a linha no
`MANIFESTO.csv` e a entrada no `REGISTRO_REFERENCIAS.md`.

## Como adicionar outras referências

Drop reference PDFs (and similar) here to have them read/analyzed, e.g.:

    docs/refs/li-et-al-2026.pdf

Then ask, for example: "read docs/refs/li-et-al-2026.pdf and compare its robustness
section with our extensions".

Note: reference files themselves are gitignored (see .gitignore) to avoid committing
third-party/copyrighted material. Only this README, REGISTRO_REFERENCIAS.md and MANIFESTO.csv
are tracked.

# Índice da documentação

Mapa do que existe aqui e por onde entrar. Este fork do BAD-ACTS mede, além do ASR original,
**utilidade, trajetória e robustez**, e a documentação segue a ordem em que o trabalho acontece:
método, experimentos, leitura dos resultados, paper, apresentação.

Os diretórios são numerados **na ordem de leitura**, não por importância. `refs/` fica fora da
numeração porque é material de consulta, não uma etapa.

---

## Por onde começar, conforme o que você quer fazer

| Quero... | Comece por |
|---|---|
| entender o que este fork acrescentou ao BAD-ACTS e por quê | [`01-metodo/EXTENSIONS.md`](01-metodo/EXTENSIONS.md) |
| **rodar a triagem dos 8 modelos** (é o que está em curso) | [`02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md`](02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md) |
| preparar uma máquina nova, ou a do laboratório | [`02-experimentos/GUIA_TRIAGEM_E_EXECUCAO.md`](02-experimentos/GUIA_TRIAGEM_E_EXECUCAO.md) |
| saber quantas execuções cada experimento definitivo pede | [`02-experimentos/PLANO_EXPERIMENTAL.md`](02-experimentos/PLANO_EXPERIMENTAL.md) |
| interpretar uma linha específica da saída de um script | [`03-metricas/`](03-metricas/) |
| defender a contribuição numa banca | [`04-paper/NOVIDADE_E_POSICIONAMENTO.md`](04-paper/NOVIDADE_E_POSICIONAMENTO.md) |
| lembrar o que foi apresentado e quando | [`05-apresentacoes/`](05-apresentacoes/) |

E, para o código, o mapa de arquitetura está no [`CLAUDE.md`](../CLAUDE.md) da raiz.

---

## O mapa completo

```
docs/
├── 01-metodo/            o que o trabalho mede, e por que essas escolhas
├── 02-experimentos/      o que vai ser rodado, e como rodar
├── 03-metricas/          como ler a saída dos scripts, linha por linha
├── 04-paper/             posicionamento na literatura e alegação de contribuição
├── 05-apresentacoes/     o que já foi apresentado, por reunião
└── refs/                 bibliografia (arquivos não versionados)
```

### `01-metodo/` — o que o trabalho mede

| Arquivo | Idioma | O que é |
|---|---|---|
| [`EXTENSIONS.md`](01-metodo/EXTENSIONS.md) | EN | O que foi acrescentado ao BAD-ACTS original, e o mapeamento para as lacunas de Li et al. (2026). É o documento de entrada do fork. |
| [`EXPERIMENTO_PARAFRASE_ADVERSARIAL.md`](01-metodo/EXPERIMENTO_PARAFRASE_ADVERSARIAL.md) | PT-BR | Desenho completo do experimento **B2**, a paráfrase do objetivo adversarial, par simétrico do B1. |

### `02-experimentos/` — o que vai ser rodado, e como

| Arquivo | O que é |
|---|---|
| [`PROTOCOLO_TRIAGEM_8_MODELOS.md`](02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md) | **Protocolo T3**, a triagem em curso: 4 modelos abertos e 5 pagos, 82 execuções cada, desenho idêntico dos dois lados, teto de US$ 10. Modelos, blocos, orçamento, comandos e regras de decisão. |
| [`PLANO_EXPERIMENTAL.md`](02-experimentos/PLANO_EXPERIMENTAL.md) | Desenho dos experimentos **definitivos**: escolha da dupla de modelos, tamanho amostral fundamentado em Montgomery, comandos prontos. A triagem é o passo anterior a este documento. |
| [`GUIA_TRIAGEM_E_EXECUCAO.md`](02-experimentos/GUIA_TRIAGEM_E_EXECUCAO.md) | Operação pura: instalar a máquina nova, servir o modelo aberto, trazer os resultados de volta, armadilhas conhecidas. |

A ordem prática é: **protocolo** decide quais modelos, **plano** decide quantas execuções, **guia**
diz como preparar a máquina.

### `03-metricas/` — como ler a saída

Estes dois explicam a saída **na ordem exata em que ela aparece na tela**. São para consultar com o
terminal aberto ao lado, não para ler de ponta a ponta.

| Arquivo | Explica a saída de |
|---|---|
| [`METRICAS.md`](03-metricas/METRICAS.md) | `evaluation/evaluate_result.py`, o relatório por arquivo de resultado |
| [`METRICAS_ROBUSTEZ.md`](03-metricas/METRICAS_ROBUSTEZ.md) | `scripts/analyze_experiment_stats.py spc`, o Experimento 1 (cartas de controle e repetibilidade) |

### `04-paper/` — onde está a novidade

| Arquivo | O que é |
|---|---|
| [`NOVIDADE_E_POSICIONAMENTO.md`](04-paper/NOVIDADE_E_POSICIONAMENTO.md) | Investigação de novidade feita antes de comprometer semanas de execução: a lacuna de robustez é real?, a estatística é novidade?, quem são os concorrentes, e quais objeções a banca vai levantar. Conclui pela reivindicação estreita (adversarial × multiagente × robustez de trajetória, quantificada por controle estatístico). |

### `05-apresentacoes/` — uma pasta por reunião

Cada reunião tem o **deck** e o **roteiro falado** que o acompanha. Os dois são fontes acopladas:
mexer em um sem mexer no outro os deixa fora de sincronia.

| Reunião | Arquivos | Assunto |
|---|---|---|
| [`reuniao-01/`](05-apresentacoes/reuniao-01/) | `apresentacao.html`, `ROTEIRO_APRESENTACAO.md`, `ROTEIRO_FALADO_50min.txt` | Primeira apresentação. Extensões, experimentos 1 a 3, alvo de ~50 min. |
| [`reuniao-02/`](05-apresentacoes/reuniao-02/) | `apresentacao.html`, `ROTEIRO_FALADO_30min.txt` | Segunda apresentação (agosto de 2026). Resultado do B2, desenho oficial do paper, pesquisa de novidade. 24 slides, alvo de ~30 min. |

> **Ressalva sobre a reunião 2:** o slide 16b reporta 37,2 mil tokens de entrada por episódio. Esse
> número está inflado cerca de 3x por contagem duplicada. O valor correto é 11,9 mil de entrada e
> 1,3 mil de saída, e a conta está no Anexo A do
> [`PROTOCOLO_TRIAGEM_8_MODELOS.md`](02-experimentos/PROTOCOLO_TRIAGEM_8_MODELOS.md).

Os decks são HTML autocontido: abra direto no navegador, sem servidor e sem dependências.
Para estimar duração de um roteiro falado, divida o número de palavras por 145.

### `refs/` — bibliografia

Material de consulta (Montgomery, artigos). Os arquivos **não são versionados** (ver `.gitignore`);
só o `README.md` da pasta é. Coloque um PDF ali e peça a leitura dele pelo caminho.

---

## Convenções

- **Idioma:** código e identificadores em inglês; documentação em PT-BR, com exceção do
  `EXTENSIONS.md`, que é o documento de entrada do fork para leitor externo.
- **Numeração das pastas:** ordem de leitura. Um número novo só entra se for uma etapa nova do
  trabalho, e não para cada arquivo.
- **Apresentações:** uma pasta por reunião, com o deck sempre chamado `apresentacao.html`. A
  identidade vem da pasta, não do nome do arquivo.
- **Nada de resultado aqui.** `results/` e `evaluation_results/` não são versionados e não moram em
  `docs/`. O que entra aqui é o que explica ou decide, não o que foi medido.

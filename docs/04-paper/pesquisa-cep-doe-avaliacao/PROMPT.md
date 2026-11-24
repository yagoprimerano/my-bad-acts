# Pesquisa externa 3 de 3 (etapa 3): controle estatístico e delineamento de experimentos na avaliação de LLM

Proposta em 24/11/2026, ainda **não disparada**. É a etapa 3 da auditoria para a qualificação
(`docs/06-qualificacao/MAPA_DE_REIVINDICACOES.md`, linhas C5 e C15, e a Seção 8, que diz o que faria as
cartas de controle voltarem a ser contribuição principal). Dois objetivos: **(a)** procurar quem já
aplicou cartas de controle ou delineamento fatorial à avaliação de LLM ou agentes (o que derrubaria a
novidade); **(b)** trazer o que a literatura diz sobre aplicar essas ferramentas quando as observações
não são independentes (o que ajuda a responder à objeção principal, na etapa 4).

Convenção: o autor dispara o mesmo prompt no Deep Research do ChatGPT e no Research do Claude e
salva aqui `chatgpt_deep_research_<AAAA-MM-DD>.md` e `claude_research_<AAAA-MM-DD>.md`. Depois cada
trabalho citado é conferido contra o original e contra os anais, e o resultado vai para `SINTESE.md`.
Só a síntese é citável.

## Prompt (igual para as duas ferramentas)

```
Contexto: sou mestrando e estudo a avaliação de segurança de sistemas multiagentes de LLM sob
ataque (benchmark BAD-ACTS, arXiv 2508.16481, COLM 2026). Minha orientadora indicou como autoridade
metodológica os livros de Douglas Montgomery: "Design and Analysis of Experiments" (8ª ed.) e
"Introduction to Statistical Quality Control" (7ª ed.). Uso: (i) repetição do mesmo caso para medir
a variação de causa comum (a estocasticidade do LLM); (ii) paráfrase da tarefa e do ataque tratada
como fator de ruído; (iii) um fatorial 2² (defesa ligada/desligada × perturbação da coordenação
sim/não) com efeitos principais e interação; (iv) cartas de controle (p e I-MR) sobre a taxa de
sucesso do ataque, para distinguir variação de causa comum de causa especial.

Duas perguntas: existe trabalho anterior que faça isso em avaliação de LLM ou de agentes? E como
lidar com a objeção de que cartas de controle supõem observações independentes de um processo
estável, quando aqui (a) casos de ataque diferentes têm dificuldades diferentes, (b) o modelo por
trás de uma API pode mudar entre execuções e (c) há dependência entre os passos de uma trajetória?

O que eu já li e conferi (não precisa repetir, mas diga se algo aqui está errado):
- Miller, "Adding Error Bars to Evals" (arXiv 2411.00640): avaliações são experimentos; recomenda
  erro padrão agrupado, reamostrar respostas, diferenças pareadas e análise de poder; não usa cartas
  de controle nem fatorial.
- Spark-LLM-Eval (arXiv 2603.28769), ReasonBench (arXiv 2512.07795), Raj et al. (NeurIPS 2026,
  estatísticas U), Yagubyan (arXiv 2605.28840, ANOVA de um fator): ICs, repetições e testes, sem
  cartas de controle nem fatorial.
- Rabanser et al. (ICML 2026) cita controle estatístico de processo só como analogia.
- Controle estatístico contra ataques fora de LLM: CUSUM em aprendizado federado (arXiv 2310.01537),
  CUSUM em sistemas ciberfísicos (arXiv 2105.10707).
- Pistas ainda não lidas: Madaan et al. 2024 "Quantifying Variance in Evaluation Benchmarks" (arXiv
  2406.10229); Blackwell, Barry e Cohn 2024 (arXiv 2410.03492); Biderman et al. 2024 "Lessons from
  the trenches on reproducible evaluation of language models" (arXiv 2405.14782).

Pesquise:

1. Trabalhos que aplicam CARTAS DE CONTROLE (Shewhart, p, np, I-MR, EWMA, CUSUM), regras de corrida
   (Western Electric, Nelson) ou a distinção causa comum × causa especial à AVALIAÇÃO de LLMs ou de
   agentes LLM, em qualquer aspecto (qualidade, segurança, regressão de modelo, monitoramento em
   produção). Separe: avaliação experimental × monitoramento de produção × detecção de ataque.
2. Trabalhos que aplicam DELINEAMENTO DE EXPERIMENTOS (fatorial completo ou fracionado, blocos,
   superfície de resposta, Taguchi, fator de ruído, ANOVA de mais de um fator) à avaliação de LLMs
   ou agentes, em especial de SEGURANÇA, ataques ou defesas.
3. Em avaliação de LLM, quem trata a variação entre execuções como objeto de estudo (componentes de
   variância, repetibilidade e reprodutibilidade, "gauge R&R", estudo de sistema de medição) em vez
   de suprimi-la com temperatura zero?
4. Literatura estatística (não precisa ser de LLM) sobre cartas de controle e experimentos quando:
   (a) as unidades são heterogêneas (subgrupo racional, cartas por estrato, cartas com limites
   ajustados ao risco, como as "risk-adjusted control charts" da saúde); (b) há autocorrelação; (c)
   os dados são binários com proporção perto de 0 ou de 1. Quais são as soluções recomendadas e as
   referências canônicas (com capítulo ou seção, inclusive no próprio Montgomery)?
5. Algum trabalho argumenta CONTRA usar controle estatístico de processo para avaliar modelos de
   aprendizado de máquina, ou mostra que dá resultados enganosos? Quais argumentos?

Para as perguntas 1 e 2, diga claramente se encontrou trabalho que aplique cartas de controle ou
fatorial à avaliação de SEGURANÇA de agentes LLM. Se não encontrou, diga "não encontrei" e liste o
mais próximo.

Regras para a resposta:
- Cite só trabalhos que você abriu. Para cada um, informe: título completo, autores, ano,
  identificador (arXiv, DOI, ISBN), LOCAL DE PUBLICAÇÃO e se passou por REVISÃO POR PARES
  (conferência principal, workshop, periódico, livro, ou só preprint). Se só encontrou no arXiv,
  diga "preprint". Não deduza o local pelo comentário do arXiv sem conferir nos anais; se não
  conferiu, diga "não conferido".
- Prioridade de fontes: ICML, NeurIPS, ICLR, ACL, EMNLP, NAACL, COLM, AAAI, IJCAI, KDD, USENIX
  Security, IEEE S&P, ACM CCS, e periódicos de estatística e qualidade (Journal of Quality
  Technology, Technometrics, Quality Engineering, Journal of the American Statistical Association,
  Statistics in Medicine). Preprints recentes entram, marcados como preprint.
- Para cada afirmação sobre o conteúdo de um trabalho, dê a seção ou a página e, se possível, a
  frase original em inglês entre aspas.
- Não invente referências. Se não tem certeza de que um trabalho existe, deixe de fora ou marque
  "não verificado".
- Diga explicitamente o que você NÃO encontrou. "Não encontrei" é uma resposta válida e útil.
- Responda em português, terminando com uma tabela única de todos os trabalhos citados, com as
  colunas: título | ano | identificador | local | revisado por pares? | relevância (alta/média/baixa)
  | o que ele faz e o que não faz em relação à pergunta.
```

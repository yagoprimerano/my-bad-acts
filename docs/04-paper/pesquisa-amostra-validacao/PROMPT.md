# Pesquisa externa: tamanho e composição da amostra de validação

Proposta em 05/11/2026, ainda **não disparada**. Serve à revisão das quantidades pedida pela
orientadora na reunião 6 (Seção 9 e Seções 7.1.2 a 7.1.4 de
`docs/02-experimentos/MEDIDA_UTILIDADE_HIBRIDA.md`). Decide entre os três desenhos da Seção 7.1.4.

Convenção: o autor dispara o mesmo prompt no Deep Research do ChatGPT e no Research do Claude e
salva aqui `chatgpt_deep_research_<AAAA-MM-DD>.md` e `claude_research_<AAAA-MM-DD>.md`. Depois as
afirmações são conferidas contra os originais e resumidas em `SINTESE.md`; só a síntese é citável.

## Prompt (igual para as duas ferramentas)

```
Contexto: num mestrado sobre segurança de agentes LLM (benchmark BAD-ACTS, sistemas multiagente),
14 modelos de linguagem geraram 686 episódios de uma tarefa de planejamento de viagem, entre 39 e
52 episódios por modelo (todos rodaram 52; os que têm menos quebraram por timeout ou erro de
chamada de ferramenta). Estou construindo uma medida automática binária de utilidade (o episódio
cumpriu a tarefa?), feita de regras determinísticas mais um juiz LLM, que será validada contra
rótulos humanos cegos numa amostra guardada, e depois aplicada aos 686 episódios para escolher
modelos por um piso de utilidade (70%). O orçamento de rotulagem humana é de ~60 a 120 episódios
por rotulador (~3,5 min cada), com dois rotuladores. A orientadora perguntou se a amostra de teste
deve ser estratificada ou balanceada por modelo, e se modelos com menos episódios ficam
favorecidos.

Pesquise e responda, citando fontes primárias (livros e artigos, com seção e página), em português:

1. Amostragem estratificada quando se quer estimar ao mesmo tempo a proporção total e a de cada
   estrato (domínio): alocação proporcional, igual, de Neyman e de compromisso (por exemplo Cochran,
   Sampling Techniques; Kish; Bankier 1988, power allocation). Quando cada uma é recomendada, e qual
   o mínimo por estrato usual para estimar uma proporção por estrato.
2. Erro de classificação diferencial versus não diferencial (epidemiologia, medição): quando um
   erro de medida que difere entre grupos distorce a comparação entre grupos e quando não. Como se
   valida um classificador ou avaliador automático para garantir que o erro não depende do grupo.
3. Como benchmarks de LLM validam um juiz LLM ou avaliador automático por modelo avaliado (não só
   no agregado): tamanhos de amostra usados, se reportam acerto por modelo ou por família, e
   evidências de que o acerto de juízes LLM varia conforme o modelo cuja saída é julgada (estilo,
   formato, comprimento), além da autopreferência.
4. Validação em duas fases (two-phase sampling, validação dirigida aos casos decisivos): rotular
   primeiro uma amostra geral e depois amostras extras só dos grupos perto de um limiar de decisão.
   Há precedente metodológico? Como se controla viés nisso?
5. Comparar proporções entre grupos de tamanhos diferentes contra um limiar fixo (70%): o que a
   literatura recomenda quando os grupos têm n desigual por perda de observações (intervalos,
   tratar perdas como fracasso, desenhos balanceados).

Para cada afirmação, indique a fonte exata. Separe o que é consenso do que é opinião de um autor.
Não invente referências; se não achar fonte, diga.
```

# Escolha do juiz LLM (DeepSeek × Claude × Gemini): síntese verificada

**29/10/2026.** Síntese dos dois relatórios de pesquisa automática desta pasta
(`claude_research_2026-10-28.md`, `chatgpt_deep_research_2026-10-28.md`), rodados com o mesmo prompt
pelo autor em 28/10/2026. Os relatórios brutos ficam aqui só como registro de onde cada afirmação
veio. **Para citar, use esta síntese**, e só as linhas da Seção 2.

**Como foi conferido.** Os 36 artigos do arXiv citados foram baixados (cópias em
`docs/refs/pesquisa-juiz-llm/`, gitignored), convertidos em texto com `pdftotext`, e cada número abaixo
foi localizado no texto original. Preços, IDs de modelo e políticas de aposentadoria foram conferidos
nas páginas oficiais dos três provedores em 29/10/2026 (Anthropic: *Pricing*, *Model deprecations*,
*Model IDs and versioning*, página do Haiku 5.5; DeepSeek: *Models & Pricing*, *Change Log*; Google:
*Gemini API pricing*, *Release notes*). Blogs, agregadores e system cards não foram abertos (Seção 6).

Serve ao passo 6 da Seção 10 de `docs/02-experimentos/MEDIDA_UTILIDADE_HIBRIDA.md` (escolher o juiz) e
ao slide do juiz da reunião 6.

**Conflito de interesse, declarado.** Um dos relatórios foi feito pelo Claude e recomenda o Claude, e
esta síntese também foi escrita com o Claude. Por isso a recomendação da Seção 4 se apoia só em fatos
conferidos (preço, política de versão, números de artigos), cada um com a fonte, e a decisão é da
orientadora. A validação no lote 2 é o teste que vale, qualquer que seja o juiz.

## 1. Conclusões

1. **Nenhum dos três candidatos foi testado como juiz de conversas multiagente com agente
   adversarial.** Os números de concordância publicados vêm de outras tarefas e variam mais com a
   tarefa do que com o modelo: só para o DeepSeek, o κ vai de 0,13 a 0,993 conforme o artigo. Não dá
   para importar um número da literatura; o acerto do juiz tem de ser medido no nosso lote 2, como já
   está no desenho.
2. **Onde há comparação direta, os três ficam próximos e nenhum é bom o bastante sozinho.** No
   AgentRewardBench (trajetórias de agentes web), nenhum juiz passa de 70% de precisão (Claude 3.7
   Sonnet, 69,4%). No PentestJudge, Claude 3.7 Sonnet tem F1 0,83 e os Gemini 2.5, 0,71 a 0,72. Isso
   reforça a divisão B + C: o juiz só responde perguntas estreitas, e nunca decide fato que está no
   registro.
3. **A diferença decisiva entre os três é a reprodutibilidade, e ela está documentada.** Na Anthropic,
   cada ID de modelo é um "pinned snapshot": o modelo por trás do ID não muda, e a aposentadoria tem
   aviso mínimo de 60 dias (o Haiku 5.5 não sai antes de 07/10/2027). No DeepSeek e no Gemini, a
   própria documentação diz que nomes antigos passam a ser atendidos por modelos novos sem o código
   mudar. Para um artigo, isso significa que o mesmo script pode medir com outro juiz daqui a três
   meses.
4. **Temperatura 0 não é opção no Claude Haiku 5.5.** A página do modelo manda omitir `temperature`,
   `top_p` e `top_k`; o raciocínio adaptativo vem ligado. E nenhum provedor garante resposta idêntica
   mesmo quando aceita temperatura 0. O desenho já mede a autoconsistência do juiz (Seção 7.3); a
   decisão P4 ("temperatura 0") precisa ser reescrita.
5. **Contra injeção de prompt, o Claude é o mais robusto dos três nas medições disponíveis, mas
   como agente atacado, não como juiz.** Na maior competição pública (Gray Swan, 272 mil tentativas):
   Claude Haiku 4.5 1,3%, DeepSeek V3.1 5,4%, Gemini 2.5 Pro 8,5% de ataques bem-sucedidos. Outros
   benchmarks vão na mesma direção. Supor que a ordem se mantém no papel de juiz é inferência.
6. **Autopreferência por família não é um risco para nós com nenhum dos três**, porque nenhum deles
   pertence às famílias avaliadas (OpenAI, Qwen, Llama, Mistral). O risco indireto (um juiz favorecer
   modelos treinados com dados dele, o "preference leakage") existe na literatura, mas não achamos
   evidência de que algum modelo avaliado tenha sido treinado com saídas desses três.
7. **Perguntas sim/não decompostas têm apoio consistente** (CheckEval, TICK, e a redução de 31,5% na
   autopreferência com decomposição). Ressalva já registrada na síntese anterior: os ganhos foram
   medidos com agregação por proporção; a nossa é por E, em que um erro do juiz numa pergunta derruba
   o veredito. Por isso o acerto é medido por subcritério.
8. **O custo não decide.** Com os preços conferidos, rodar o juiz em toda a população fica entre
   cerca de US$ 2,50 (Haiku 5.5) e US$ 30 (Gemini 3.8 Flash em 2027) no cenário dos relatórios
   (Seção 3). O DeepSeek seria gratuito para nós, pelos créditos da orientadora.

## 2. Afirmações conferidas

### 2.1 Concordância com humanos

| fonte | onde | o que diz o original | uso para nós |
|---|---|---|---|
| **AgentRewardBench**, Lù et al., arXiv 2504.08942 | resumo, §4.3, Tabela 1 | 1302 trajetórias, 12 juízes LLM; "no judge achieves above 70% precision"; GPT-4o 69,8; Claude 3.7 Sonnet 68,8 (árvore de acessibilidade) e 69,4 (captura de tela); concordância entre anotadores 89,3% | a referência mais próxima da nossa tarefa; não testa DeepSeek nem Gemini |
| **PentestJudge**, Caldwell et al., arXiv 2508.02921 | tabela de resultados | F1: claude-3-7-sonnet 0,83; claude-3-5-haiku 0,74; gemini-2.5-pro 0,71; gemini-2.5-flash 0,71; gemini-2.5-flash-lite 0,72; o único DeepSeek testado é o deepseek-r1-distill-llama-70b, com F1 0,51 | juiz de comportamento de agente contra requisitos; Claude à frente |
| **Reliability without Validity**, arXiv 2606.19544 | tabela principal | DeepSeek V3.2: κ 0,486 (MT-Bench), 0,545 (JudgeBench), 0,826 (RewardBench); Claude Opus 4.6: 0,489, 0,875, 0,879; Gemini 3.1 Pro: 0,511, 0,841, 0,898 | **os três praticamente empatam** no MT-Bench; a concordância bruta (≈0,85) esconde um κ de ≈0,5 |
| **LLM-as-a-Judge in Healthcare**, arXiv 2605.25273 | Fig. 9 | DeepSeek-V3 com o menor κ, 0,59 (IC 95% 0,37 a 0,82, N = 49); mediana de 10 estudos 0,78 | ilustra o tamanho do IC com N perto do nosso lote 2 |
| **JudgeArena**, arXiv 2608.02620 | Tabela 2 | deepseek-v3.2: κ 0,13, Spearman 0,78, US$ 0,44 por mil anotações; gemini-3.1-flash: κ 0,17; todos os juízes da tabela ficam entre 0,11 e 0,17 | o κ baixo é da tarefa (preferência entre pares), não do DeepSeek |
| **STAGE**, arXiv 2601.08510 | §3 | DeepSeek-V4-Pro concorda com o consenso humano em 90,3% (humanos entre si: 91,7%); κ por tarefa 0,82, 0,86, 0,76 | uso publicado do DeepSeek como juiz, justificado por validação |
| **Is Deep Research Reliable?**, arXiv 2607.20891 | apêndice | DeepSeek-V4 Pro: 99,7% de concordância, κ 0,993, em 300 relatórios rotulados por dois humanos | idem; tarefa binária fácil |
| **From Production Traffic to Post-Training**, arXiv 2609.01572 | Tabela 12 | juiz DeepSeek-V3-0324: κ de 0,61 para 0,68 (sumarização) e de 0,49 para 0,79 (geração) quando o julgamento passa a seguir critérios explícitos | critério escrito melhora o juiz |
| **Estonian Native LLM Benchmark**, arXiv 2510.21193 | §4 | Claude 3.7 Sonnet como juiz: Pearson 0,94, Spearman 0,92 com notas humanas | |
| **MobileJudgeBench**, arXiv 2608.11434 | §3 | 931 trajetórias de agentes móveis; concordância humana sobre sucesso 88,4%; juízes incluem Gemini 3 Flash e Claude Sonnet 4.5 | números por modelo não extraídos |
| **Zheng et al.** (MT-Bench), arXiv 2306.05685 | §4 | concordância GPT-4 × humanos de 85% (sem empates), acima da concordância entre humanos | a origem do "80 a 85%" do relatório do ChatGPT |

### 2.2 Vieses

| fonte | onde | o que diz o original | uso para nós |
|---|---|---|---|
| **Self-Preference Bias**, Yang et al., arXiv 2604.22891 | Tabela 3, §4.2 | 20 modelos; DeepSeek-V3.2 β = +0,226 (π = 0,82, "Machiavellian Judge"); DeepSeek-V3-0324 β = 0,024 (não significativo); Claude-Sonnet-4.5 β = −0,229 (π = 0,84, penaliza a si mesmo); a decomposição em dimensões reduz o viés em 31,5% em média | autopreferência varia por versão, não só por família |
| idem | §3 | juízes de referência Gemini-2.5-Pro e GPT-5-Chat-Latest, Spearman entre eles 0,658 | |
| **CyclicJudge**, arXiv 2603.01865 | tabela de viés | Claude Sonnet 4.6, autoviés de +0,412 no MindEval, "the only positive entry" da sua linha | o sinal do Claude muda com versão e tarefa |
| **GAUGE**, arXiv 2609.12191 | §4 | juiz Opus-4.8 infla agentes Claude em +0,75 numa escala de 7 em relação ao GPT-5.5 (Sonnet-4.5: +0,67); ranking preservado (ρ = 0,92) | autopreferência real, mas só importa se o juiz e o avaliado forem da mesma família |
| **aipsy-judge**, arXiv 2608.24899 | resumo, §4.2 | Gemini (2.5 Flash) como juiz: o mais leniente, prêmio de +0,99 nas próprias gerações, aponta de um terço a um quinto das falhas que os outros apontam; GPT −0,119 e Claude −0,120 | o único dado específico de viés do Gemini, e é desfavorável |
| **Preference Leakage**, Li et al., ICLR 2026, arXiv 2502.01534 | resumo, tabela | três relações entre gerador e juiz; na mesma família e mesma série, 8,9% de vazamento médio; séries diferentes, 2,8%; "a pervasive and real-world problem" | o risco indireto da conclusão 6 |
| **Justice or Prejudice?**, Ye et al., arXiv 2410.02736 | §3 | define e mede o "self-enhancement bias" entre 12 vieses | |
| **A Benchmark for ... Constraint Violations**, arXiv 2512.20798 | §4.1 e §4.3 | painel GPT-5.5, Grok-4.20, Claude-Opus-4.7, Gemini-3.1-Pro, temperatura 0; excluir a autoavaliação muda 6 de 318 classificações (1,9%), rankings idênticos; "2 DeepSeek models were excluded from this evaluation in adherence to institutional policy" | ver Seção 4, ponto 5 |

### 2.3 Perguntas atômicas

| fonte | onde | o que diz o original | uso para nós |
|---|---|---|---|
| **CheckEval**, Lee et al., EMNLP 2025, arXiv 2403.18771 | resumo | 12 modelos avaliadores; checklists binários melhoram a concordância média entre modelos em 0,45 e reduzem a variância | já citado na síntese anterior |
| **TICK**, arXiv 2410.03608 | resumo, tabelas | concordância exata com humanos de 46,4% para 52,2%; entre anotadores humanos com checklist, de 0,194 para 0,256 | ganho real, moderado |
| **Towards a Reliable and Practical Eval Pipeline**, arXiv 2609.00805 | §2 | adota o CheckEval pela concordância entre LLMs; várias perguntas funcionam como "error buffer" | o argumento vale para agregação por proporção, não por E |

### 2.4 Reprodutibilidade e versões (documentação oficial, 29/10/2026)

| provedor | o que a página diz | consequência |
|---|---|---|
| **Anthropic**, *Model IDs and versioning* | "Each Claude model ID identifies a pinned version of the model. When you use a model ID in an API request, the underlying model remains constant for the lifetime of that ID"; desde a geração 4.6, o ID sem data é o snapshot fixo | `claude-haiku-5-5` é um juiz que não muda por baixo |
| **Anthropic**, *Model deprecations* | "at least 60 days' notice before model retirement for publicly released models"; exemplo: Sonnet 4.5 avisado em 30/09/2026, aposentado em 30/11/2026 | aposentadoria avisada, e requisição a modelo aposentado falha (não troca de modelo) |
| **Anthropic**, página do Haiku 5.5 | lançado em 07/10/2026; aposentadoria "Not sooner than October 7, 2027"; "Adaptive thinking is on by default [...] Omit temperature, top_p, and top_k"; mesmo tokenizador do Claude 4.7+, cerca de 30% mais tokens | cobre o definitivo (antes de março/2027) e a revisão do artigo; **sem temperatura** |
| **DeepSeek**, *Models & Pricing* e *Change Log* | "simply use deepseek-flash to access the latest model"; hoje servido pelo DeepSeek-V4.1-Flash-1017; os nomes antigos "are still accepted, but the corresponding models have been retired; their requests are served by DeepSeek-V4.1-Flash-1017"; modo de raciocínio ligado por padrão | não há como fixar a versão pela API; dá só para registrar qual versão respondeu |
| **Google**, *Release notes* | "API requests to gemini-3.7-flash are automatically routed to gemini-3.8-flash" (08/10/2026) | idem |
| **LLM-42**, arXiv 2601.17768 | o modo determinístico custa até 56% de vazão | por isso os provedores não o usam por padrão |
| **Beyond Reproducibility**, arXiv 2601.06118 | a variação entre execuções é grande quando a probabilidade do token está entre 0,2 e 0,8 | inferência: os casos ambíguos são os que vão oscilar; a autoconsistência mede isso |

### 2.5 Injeção de prompt

| fonte | onde | o que diz o original | uso para nós |
|---|---|---|---|
| **Gray Swan IPI Arena**, Dziemian et al., arXiv 2603.15714 | resumo, Fig. 1, §4.1 | 464 participantes, 272 mil tentativas, 13 modelos; sucesso: Gemini 2.5 Pro 8,5% (1670/19630), DeepSeek V3.1 5,4% (808/15026), Claude Haiku 4.5 1,3% (177/13696), Sonnet 4.5 1,0%, Opus 4.5 0,5% | a comparação mais limpa entre os três; mede agentes, não juízes |
| **DREAM**, arXiv 2512.19016 | tabela principal | taxa de sucesso de ataque: Claude-Sonnet-4.5 24%, DeepSeek-V3.1 67%, Gemini-2.5-Pro 72%, Gemini-2.5-Flash 76% | mesma ordem |
| **TRAP**, arXiv 2512.23128 | resumo, tabela | DeepSeek-R1 43%, Gemini 2.5 Flash 30%, Claude Sonnet 3.7 20% | mesma ordem |
| **AgentSys**, arXiv 2602.07398 | tabela, sem defesa | Gemini-2.5-Pro 36,90%, Claude-3.7-Sonnet 7,84% | |
| **Skill Injection**, arXiv 2606.01567 | Tabela 2 | Sonnet-4.5 36,0%, DeepSeek-V4-Flash 52,5% sem defesa; DeepSeek cai para 2,9% a 5,0% com as defesas do artigo | defesa importa mais que o modelo |
| **AutoDojo**, arXiv 2606.15057 | §5 | ataque adaptativo leva o PIGuard de 0,0% para 28,0% de sucesso (no GPT-4o-mini) | defesa que zera ataques fixos não zera ataques adaptados |
| **IterInject**, arXiv 2605.24659 | Tabela 2 (DeepSeek) | sem defesa 32,9% (ataque fixo) e 47,8% (ataque otimizado); com delimitadores 15,3% e 18,8% | **delimitar corta pela metade, não elimina**; por isso o teste de injeção do desenho |
| **JudgeDeceiver**, CCS 2024, arXiv 2403.17710 | resumo, tabelas | ataque otimizado contra juízes: 90,8% em média, até 97,6%; ataques manuais no máximo 40,7% | exige acesso aos pesos (risco teórico para nós: o adversário do BAD-ACTS não otimiza contra o juiz) |
| **The Attacker Moves Second**, arXiv 2510.09023 | resumo | defesas com sucesso estático perto de 0% chegam a 90% a 100% sob ataque adaptativo | |

## 3. Custo, recalculado com os preços conferidos

Cenário dos relatórios (conservador, não é o nosso): 700 episódios × 2 execuções = 1400 chamadas,
12 mil tokens de entrada e 400 de saída por chamada (16,8 M de entrada, 0,56 M de saída). Sem o
desconto de lote (Batch API, 50% nos três).

| juiz | preço por milhão (entrada / saída) | total |
|---|---|---|
| Claude Haiku 5.5 | US$ 0,10 / 0,50; tokenizador +30% | cerca de US$ 2,55 |
| DeepSeek flash (V4.1-Flash-1017) | US$ 0,30 / 1,20 no pico; metade fora do pico | US$ 5,71 (pico), 2,86 (fora); **grátis com os créditos da orientadora** |
| DeepSeek v4-pro | US$ 1,32 / 3,96 no pico | US$ 24,39 |
| Gemini 3.8 Flash | US$ 0,75 / 3,75 até 31/12/2026; **US$ 1,50 / 7,50 a partir de 01/01/2027** | US$ 14,70; US$ 29,40 em 2027 |
| Claude Sonnet 5.5 | US$ 2 / 10; tokenizador +30% | cerca de US$ 51 |

O nosso caso real é diferente: o juiz lê o recorte de B (poucas mensagens), não o episódio inteiro,
mas é chamado uma vez por pergunta. Três coisas podem mudar a ordem de grandeza: o raciocínio ligado
por padrão no Haiku 5.5 e no DeepSeek (tokens de pensamento são cobrados como saída), o número de
perguntas por episódio, e o baseline "só C" da Seção 7.3, que lê o episódio inteiro. O custo real é
medido em 20 episódios no passo 7, como já planejado.

## 4. O que muda no nosso desenho

1. **Recomendação para levar à orientadora: Claude Haiku 5.5 como juiz principal**, pelo ID
   `claude-haiku-5-5`. Motivos, em ordem: o modelo por trás do ID não muda e não sai antes de
   07/10/2027 (o definitivo e a revisão do artigo cabem nesse prazo); é o mais barato dos três; e é da
   família com menor taxa de injeção nas medições disponíveis. Nenhum desses motivos é "acerta mais":
   isso só o lote 2 dirá.
2. **DeepSeek como segundo juiz, para análise de sensibilidade**, com os créditos da orientadora:
   o mesmo prompt congelado, no lote 2 (concordância entre os dois juízes) e, se os créditos
   permitirem, na reaplicação aos 686 (o piso e o par de modelos mudam se o juiz mudar?). Gravar em
   cada saída a versão que a API diz ter respondido, porque o nome `deepseek-flash` não fixa a versão.
   Não serve como juiz principal pelo mesmo motivo.
3. **Gemini fica de fora**: troca de modelo por baixo do nome, preço dobrando em 01/01/2027 (dentro do
   prazo do definitivo), e o único dado específico de viés como juiz é desfavorável (o mais leniente,
   aipsy-judge).
4. **Reescrever a P4 e a Seção 5.2**: "temperatura 0" sai. Fica: ID fixo, parâmetros de amostragem
   omitidos (o Haiku 5.5 não os aceita), nível de esforço do raciocínio fixado e registrado, prompt
   versionado com hash, todas as entradas e saídas gravadas. A autoconsistência (C rodado duas vezes
   no lote 2) passa de verificação a medida necessária, porque não há como forçar determinismo.
5. **Política institucional sobre o DeepSeek.** Um dos artigos conferidos excluiu modelos DeepSeek
   "in adherence to institutional policy". Os nossos episódios são sintéticos e não têm dado pessoal,
   então o risco parece pequeno, mas vale perguntar à orientadora se a USP ou o grupo têm alguma
   restrição.
6. **Trocar de juiz depois do lote 2 é proibido.** O relatório do Claude sugere "se o κ do Haiku
   ficar abaixo de 0,7, suba para o Sonnet". Isso fixa um limiar que a orientadora decidiu não fixar
   (resposta de 27/10) e, pior, ajusta a medida olhando o teste. Se houver troca, ela acontece antes
   do congelamento (passo 8), com base no desenvolvimento.
7. **Mitigações de injeção a acrescentar à Seção 5.3** (sugeridas pelo relatório do Claude, coerentes
   com o IterInject): delimitadores com marca aleatória por chamada; o juiz nunca vê o veredito
   esperado; teste com frases adversariais do próprio BAD-ACTS, relatando quantas vezes o veredito
   vira. Delimitar sozinho não basta (corta a taxa de ataque pela metade, não a zera).
8. **Viés de verbosidade na amostra.** Incluir no lote 2 mensagens longas e bem estruturadas que
   são intermediárias (pedido a outro agente), o caso em que um juiz atraído por texto longo erraria
   em V-ENT. O sorteio estratificado por modelo provavelmente já traz casos assim; conferir depois.
9. **Para o paper:** nenhum artigo encontrado valida um juiz LLM em conversas multiagente sob ataque.
   Escrever como "não encontramos", nunca "não existe".

## 5. Erros e divergências nos relatórios

**Relatório do ChatGPT** (mais curto, com mais erros):

- **Preço do DeepSeek errado:** usou US$ 0,006 por milhão de entrada, que é o preço com cache (cache
  hit). Sem cache é US$ 0,30 no pico. O total de "US$ 0,6" vira US$ 5,71.
- **"Não há dados de Claude ou Gemini como juízes de trajetórias de agentes":** falso
  (AgentRewardBench, PentestJudge).
- **"Não há uso documentado de DeepSeek, Claude ou Gemini como juízes em benchmarks publicados":**
  falso (TheAgentCompany usa Claude, conferido na síntese anterior; STAGE e 2607.20891 usam DeepSeek;
  2512.20798 usa Claude e Gemini).
- **"Não há estudos de afinidade de família":** o Preference Leakage (ICLR 2026) estuda exatamente isso.
- **"Temperatura 0 geralmente leva a saída determinística":** não; e no Haiku 5.5 o parâmetro nem é
  aceito.
- **"Ataques de injeção têm cerca de 50% de chance de sucesso":** sem fonte; as medições conferidas
  vão de 0,5% a 76%, conforme modelo e cenário.
- Acertou: CheckEval (0,45), Ye et al. (autoaprimoramento), MT-Bench (85%), preços do Gemini e dos
  Claude maiores.

**Relatório do Claude** (mais completo; ele mesmo marca o que não conferiu):

- **Juízes "fechados" que eram abertos:** atribui ao arXiv 2505.13348 "22 a 24% de sucesso contra
  juízes fechados". Os juízes testados são Qwen2.5-3B e Falcon3-3B, modelos pequenos e abertos.
- **IterInject:** os números de defesa citados (15,3%, 12,7%, 3,3%, 0,4%) são do ataque fixo, não do
  otimizado (18,8%, 14,9%, 4,1%, 0,4%). A conclusão não muda.
- **JudgeArena:** apresenta o κ 0,13 do DeepSeek como fraqueza dele; todos os juízes daquela tabela
  ficam entre 0,11 e 0,17. O "contra US$ 4 dos Qwen3.5" vale para os Qwen grandes; o Qwen3.5-9B custa
  US$ 0,43.
- **AgentDojo:** cita 30,52% para o Claude 3 Sonnet; a versão atual do artigo diz 26,71% (talvez a
  v1 dissesse outra coisa; a v1 não foi aberta). Modelo antigo, irrelevante para a decisão.
- **MINJA:** "sucesso de 100% contra o DeepSeek-R1"; o artigo diz injeção 100% e ataque acima de 90%.
- **Recomendação com limiar e troca depois do teste** (κ < 0,7 → Sonnet): ver Seção 4, ponto 6.
- **"Temperatura 0 se o modelo aceitar":** conferido, não aceita.
- Acertou e foi confirmado: Gray Swan, AgentRewardBench, PentestJudge, os κ do DeepSeek, os β de
  autopreferência, CyclicJudge, GAUGE, aipsy-judge, Preference Leakage, os preços dos três, a política
  de 60 dias e a troca silenciosa no DeepSeek e no Gemini. A aposentadoria do Sonnet 4.5 (30/11/2026),
  que ele deu como fonte secundária, está na página oficial.

## 6. Não conferido (não citar sem abrir a fonte)

- "Defeating Nondeterminism in LLM Inference" (Thinking Machines, blog, set/2025): 80 respostas
  distintas em 1000 execuções do Qwen3-235B com temperatura 0. Não revisado por pares; não aberto.
- Pesos abertos do DeepSeek-V4-Flash-0731 (284B parâmetros, licença MIT): só fontes secundárias.
  Se o DeepSeek de pesos abertos for considerado, conferir no Hugging Face o tamanho e se cabe na
  máquina disponível.
- System cards da Anthropic (Opus 4.5, 4.6) e números de injeção vindos de VentureBeat, The Decoder,
  stingrai e blogs sobre "Opus 4.8", "Opus 5" e "Gemini 4 Argon".
- Lessons from Defending Gemini (arXiv 2505.14534): a queda do ataque TAP de 99,8% para 53,6% aparece
  numa tabela do apêndice, mas o contexto não foi lido.
- Dorner et al. (2025), "cerca de 84% de acurácia com GPT-4 como juiz" (relatório do ChatGPT): sem
  identificador; não aberto.
- OWASP AI Agent Cheat Sheet e a afirmação de que a Anthropic recomenda modelos separados para gerar e
  avaliar: não abertos.

# Cartas de controle, delineamento de experimentos e variabilidade na avaliação de LLMs e agentes

## Escopo da busca e conclusão principal

Fiz a busca com corte em **24 de novembro de 2026**, cobrindo arXiv, OpenReview, PMLR, ACL Anthology, páginas oficiais de NeurIPS, Wiley, PubMed e literatura de controle estatístico de processos. Usei combinações de termos como *control chart*, *statistical process control*, *Shewhart*, *CUSUM*, *EWMA*, *I-MR*, *common cause*, *special cause*, *factorial design*, *full factorial*, *fractional factorial*, *design of experiments*, *variance*, *reproducibility*, *risk-adjusted control chart*, *autocorrelation*, *LLM*, *agent*, *jailbreak* e *prompt injection*. Quando encontrei PDFs e precisei de seu conteúdo, abri e inspecionei o documento; para trabalhos com página HTML oficial, preferi a versão HTML para conseguir confirmar metadados e seções. Há duas limitações importantes. Primeiro, literatura de 2026 ainda pode estar em fluxo entre preprint, aceite e publicação formal. Segundo, **não encontrar um artigo depois dessa busca é ausência de evidência, não evidência de ausência**.

A resposta curta às duas perguntas centrais é esta:

**Cartas de controle na avaliação de segurança de agentes LLM:** encontrei finalmente um trabalho extremamente próximo, *Control Charts for Multi-Agent Systems*, de Hayden Helm, Carey Priebe e Brandon Duderstadt, 2026. Ele aplica explicitamente **cartas de controle adaptativas** ao comportamento de sistemas multiagentes generativos e estuda a presença de agentes adversariais. O objetivo, porém, é **monitoramento dinâmico do sistema**, não delineamento de um benchmark de segurança com ASR por caso, réplicas, Phase I/II e cartas p ou I-MR sobre uma resposta experimental. Os autores dizem explicitamente que estendem “the process-theoretic notion of adaptive control charts to multi-agent systems” e mostram que agentes que defeccionam devagar podem escapar do monitor. citeturn390836view1turn782222academia12 Portanto, para a formulação específica que você propõe para BAD-ACTS, **não encontrei** trabalho anterior que use cartas p/I-MR, causa comum/especial e Phase I/II como parte da *avaliação experimental* de segurança de agentes LLM.

**Delineamento fatorial na segurança de LLMs/agentes:** aqui a resposta mudou bastante em 2026. Encontrei trabalhos que fazem delineamento fatorial real em LLMs e agentes, e pelo menos um em contexto diretamente relacionado a segurança. *Voices Across Registers* usa uma “factorial decomposition” para separar o efeito de registro linguístico de comprimento e estrutura sobre jailbreaks; é EMNLP 2026. citeturn584994view6 Além disso, *Evaluation of Multi-Turn Consistency in LLM Agents* declara um “full-factorial design” cruzando visibilidade social, estressores de persona e política de deliberação em 84.540 trajetórias; o artigo chama explicitamente a Seção 3.2 de “EXPERIMENTAL DESIGN (FULL-FACTORIAL PERTURBATIONS)”. citeturn763496view0turn763496view2 Esse último é de confiabilidade de agentes, não de ataque/defesa. Para **segurança de agentes sob ataque e defesa**, não encontrei um estudo que corresponda ao seu 2² defesa × perturbação de coordenação, com estimativa formal dos dois efeitos principais e da interação.

Sua leitura prévia está, no essencial, correta. Miller de fato recomenda tratamento estatístico de incerteza, reamostragem de respostas, análise pareada e poder, mas não SPC nem delineamento fatorial; a seção de power analysis explicita como aumentar replicações por pergunta reduz o efeito mínimo detectável. citeturn584994view3 Blackwell, Barry e Cohn são particularmente relevantes porque tratam explicitamente repetições do mesmo benchmark: definem \(X_{ij}\) como o resultado da pergunta \(i\) na repetição \(j\) e constroem intervalos preditivos sobre repetições futuras, em vez de fingir que a execução é determinística. citeturn584994view1 Madaan et al. não é apenas um preprint solto: encontrei registro de publicação no workshop RegML de NeurIPS 2024; o artigo mede explicitamente variância entre seeds e outras fontes de variabilidade de benchmark. citeturn104848view0 Biderman et al., pelo que consegui verificar, continua catalogado como CoRR/preprint, e não encontrei uma publicação formal em conferência principal. citeturn104848view1

## Cartas de controle em LLMs e agentes

### Avaliação experimental

Aqui a lacuna continua bastante clara. **Não encontrei** artigo que pegue um conjunto fixo de tarefas ou ataques de LLM, faça réplicas do mesmo caso e use carta p, np, I-MR, EWMA ou CUSUM para separar explicitamente **variação de causa comum da estocasticidade do modelo** de **causa especial causada por uma defesa, ataque, regressão de versão ou outra intervenção experimental**.

O trabalho mais próximo é *Control Charts for Multi-Agent Systems*. Ele não monitora ASR de uma bateria fixa de ataques. O objeto é um resumo geométrico do estado de uma população de agentes ao longo do tempo, e a contribuição é um mecanismo adaptativo de monitoramento. O artigo afirma que os métodos existentes para sistemas multiagentes abertos eram essencialmente estatísticas agregadas, inspeção qualitativa ou comparação entre dois tempos, e propõe cartas de controle adaptativas para monitoramento sistêmico. citeturn390836view1 Isso é SPC genuíno, não apenas uma metáfora, mas está conceitualmente mais perto de **surveillance/change detection** do que de uma DOE de benchmark.

Também é importante não confundir qualquer detector sequencial com SPC aplicado a avaliação. Um CUSUM que detecta intrusão, fraude ou desvio numa série temporal é uma aplicação de detecção sequencial. Para contar como precedente metodológico direto para seu uso, eu exigiria pelo menos que o *process characteristic* monitorado fosse um indicador de qualidade ou segurança do LLM/agente, que existisse uma baseline in-control e que os limites fossem interpretados em termos de variação esperada versus mudança do sistema. Esse critério elimina boa parte da literatura de “CUSUM contra ataques” que é apenas detecção de anomalia.

### Monitoramento de produção

Fora de LLMs, mas diretamente útil para defender a metodologia, há literatura de **monitoramento de ML implantado** que já importa SPC de forma explícita. Feng et al., em *Designing monitoring strategies for deployed machine learning algorithms: navigating performativity through a causal lens*, combinam causal inference e SPC para comparar seis estratégias de monitoramento de modelos implantados. A introdução chama atenção para um problema exatamente relevante para APIs de LLM: métodos de SPC usualmente assumem um cenário “ideal” no qual o algoritmo não altera o mecanismo gerador dos dados; quando há performatividade, a avaliação observacional pode ser enviesada. citeturn390836view0turn312366view2 É um trabalho revisado por pares no 3rd Conference on Causal Learning and Reasoning, PMLR 236, 2024. citeturn390836view0

Na medicina, a transposição de SPC para monitoramento de algoritmos clínicos é ainda mais explícita. A literatura descreve o objetivo como disparar um alarme quando aparece **special-cause variation** e distinguir isso de **common-cause variation** no desempenho do algoritmo. citeturn665078search6 Isso fornece um precedente conceitual muito melhor para sua interpretação de causa comum/especial do que artigos genéricos de concept drift.

### Detecção de ataque

*Control Charts for Multi-Agent Systems* é também o precedente mais forte que encontrei nesse quadrante. Os autores não apenas monitoram drift benigno. Eles constroem uma análise adversarial e demonstram que uma carta adaptativa pode deixar de sinalizar um agente que mude seu comportamento suficientemente devagar. A frase mais importante para sua tese é que o artigo encontra um trade-off entre permitir aprendizagem legítima e manter detectabilidade de adversários lentos. citeturn390836view1

Isso tem uma consequência importante para BAD-ACTS: um limite adaptativo que “aprende” continuamente a baseline pode literalmente aprender o ataque. Portanto, se seu objetivo é detectar uma mudança de segurança, a baseline de Phase II não deveria ser atualizada cegamente a cada lote. Esse é exatamente o tipo de mecanismo pelo qual uma carta tecnicamente sofisticada pode ficar menos segura.

## Delineamento de experimentos em LLMs e agentes

Há agora precedentes inequívocos para DOE formal em avaliação de LLMs.

O mais geral é *Beyond Benchmarks: Toward Causally Faithful Evaluation of Large Language Models*, ICML 2026. Os autores dizem explicitamente que combinam modelagem causal com “factorial decomposition under design of experiments”, quantificando **main and interaction effects**. citeturn390836view2 Isso é muito mais próximo de Montgomery do que uma sequência de ablações independentes. A motivação deles também coincide com a sua: resultados observados dependem não apenas do modelo, mas do dataset, prompting, decoding e stack de software/hardware, e ignorar interações entre esses componentes torna a atribuição enganosa. citeturn390836view2

*CAFE: A Compound-AI Factorial Evaluation Framework*, EMNLP 2026 System Demonstrations, torna essa ideia operacional. O usuário registra componentes substituíveis como fatores, constrói um desenho fatorial e o sistema atribui variância a fatores e **interações** com mixed-effects models. A validação é feita em um pipeline RAG sobre HotpotQA. citeturn390836view3 É especialmente relevante porque oferece um exemplo moderno de como combinar DOE com efeitos aleatórios de itens, em vez de tratar todas as respostas como observações iid.

Em agentes, *Evaluation of Multi-Turn Consistency in LLM Agents: Survival Analysis and Failure-Rationale Taxonomy*, ICLR 2026, é um exemplo explícito de desenho full factorial. A Seção 3.2 cruza visibilidade social, estressores de persona e política de deliberação, resultando em 64 combinações por família de modelo, com prompts e instrumentação mantidos constantes. citeturn763496view0turn763496view2 A análise principal é de sobrevivência/hazard, o que também é útil para sua preocupação sobre dependência temporal em trajetórias: eles não tratam cada passo como um Bernoulli independente, mas definem o primeiro evento de falha e usam hazard discreto condicionado à sobrevivência até o passo. citeturn763496view2

Na segurança, *Voices Across Registers: Corpus-Conditioned Vernacular Jailbreaks against Aligned LLMs via Fanfiction Subgenres*, EMNLP 2026, informa que uma decomposição fatorial mostra que o ganho de ASR vem do **registro**, e não de comprimento ou estrutura. citeturn584994view6 Isso é o precedente mais próximo que encontrei para análise fatorial de um mecanismo de ataque. Ainda assim, ele não parece ser um desenho de segurança de agentes com defesa × ataque × interação no sentido que você propõe.

Também encontrei *Does Safety Reasoning Travel?*, workshop ORACLE 2026, que usa uma amostra estritamente pareada de 320 cenários por célula, seis idiomas e um controle pré-registrado por paráfrase. O trabalho mostra que efeitos aparentemente atribuíveis à língua podiam ser produzidos por defeitos de tradução ou memorização do monitor. citeturn584994view7 Embora não seja apresentado como DOE Montgomery-style, metodologicamente ele reforça fortemente sua ideia de tratar **paráfrase como fator de ruído controlado**, não como mero aumento de dataset.

A distinção que eu usaria na dissertação é:

**Ablação cruzada**: executa combinações de componentes e compara médias, frequentemente sem randomização, replicação planejada, especificação de erros, análise de interação ou princípio hierárquico.

**Delineamento fatorial formal**: níveis e fatores são definidos a priori; todas as combinações relevantes são executadas ou uma fração de aliasing conhecido é usada; há replicação ou erro estimável; efeitos principais e interações são estimados num modelo explícito; randomização, blocking e estrutura de erro são justificadas.

Pelo segundo critério, Tian et al., CAFE e Manakina et al. são precedentes claros. Seu 2² também se qualifica, desde que análise e randomização acompanhem a matriz experimental.

## Variabilidade, repetibilidade e reprodutibilidade de LLMs

Aqui existe uma linha de literatura mais consolidada do que em SPC.

Madaan et al. dizem diretamente que a comunidade “rarely quantify[ies] the variance in our evaluation benchmarks” e mede variância entre seeds e monotonicidade durante treinamento. citeturn104848view0 É uma abordagem de **componentes de variabilidade de avaliação**, embora não use a terminologia Gauge R&R.

Blackwell, Barry e Cohn são ainda mais diretamente comparáveis a um estudo de repetibilidade. A Seção 3 formaliza \(n\) repetições do mesmo experimento e um score binário \(X_{i,j}\) para a pergunta \(i\) na repetição \(j\). citeturn584994view1 O ponto conceitual importante é que o objeto inferencial inclui a distribuição de scores entre execuções futuras, não apenas a média no benchmark.

Yagubyan, em *How Consistent Are LLM Agents?*, literalmente pergunta “if you run the same agent on the same task twice, do you get the same behavior?” e usa 19 tarefas, dez ferramentas simuladas determinísticas e execuções repetidas para isolar variabilidade do LLM de não determinismo ambiental. citeturn104848view4 Essa separação é muito parecida com a lógica de um estudo de sistema de medição: controlar o dispositivo externo e observar quanto da variação permanece no “instrumento” LLM/agente. O trabalho mede consistência de sequência de ferramentas e argumentos e mostra que a variação não é homogênea entre camadas do comportamento. citeturn104848view4 É preprint, não encontrei publicação revisada por pares.

Biderman et al. atacam uma camada complementar: detalhes aparentemente pequenos de implementação podem alterar avaliações, e por isso defendem especificação e reprodutibilidade da infraestrutura de avaliação. citeturn584994view2 Não é Gauge R&R, mas pode fundamentar uma decomposição conceitual entre variabilidade do modelo, do prompt, da implementação e do benchmark.

Minha leitura é que **não encontrei uma aplicação literal de Gauge R&R a LLMs**, com repeatability, reproducibility, operator/appraiser e porcentagem da variância total no formato clássico de quality engineering. Isso é uma oportunidade metodológica real. A tradução mais natural seria algo como:

\[
Y_{cprmv}
=
\mu
+\alpha_c
+\beta_p
+\gamma_r
+\delta_m
+\eta_v
+\text{interações}
+\varepsilon
\]

onde \(c\) é caso, \(p\) paráfrase, \(r\) execução, \(m\) configuração do modelo e \(v\) versão/API. Para resposta binária, em vez de ANOVA gaussiana de variâncias, eu usaria um **GLMM logístico** com efeitos aleatórios de caso, paráfrase aninhada em caso e, quando aplicável, lote/API. Isso preserva a intuição de variance components sem impor normalidade ao ASR.

## O problema das premissas de SPC

Sua objeção tem três partes diferentes e eu não as resolveria com a mesma técnica.

### Casos de ataque com dificuldades diferentes

Uma carta p ingênua sobre uma mistura variável de ataques está confundindo duas coisas: mudança do processo e mudança do *case mix*. Na saúde, o análogo clássico é exatamente monitorar resultados cirúrgicos quando pacientes têm riscos basais distintos. Steiner, Cook e Farewell propõem um **risk-adjusted CUSUM** em que a contribuição de cada caso depende do risco de falha estimado antes do procedimento. O artigo diz que o método “adjusts for the surgical risk of each patient estimated preoperatively” e, portanto, é aplicável quando o mix de pacientes varia. citeturn390836view5

Para BAD-ACTS, isso sugere três opções, em ordem de rigor:

1. manter **subgrupos racionais** com exatamente a mesma composição de casos entre pontos da carta;
2. usar cartas separadas por estrato de dificuldade/tipo de ataque;
3. ajustar cada observação por um modelo de risco do caso, por exemplo um modelo logístico hierárquico, e monitorar residual, score ou log-likelihood ratio em vez da proporção bruta.

Montgomery coloca o princípio de **rational subgroups** em *Introduction to Statistical Quality Control*, 7ª ed., §5.3.4; análise de padrões em §5.3.5, regras de sensibilização em §5.3.6 e Phase I/Phase II em §5.3.7. citeturn192494search1turn818479search1 Para processos com múltiplos fluxos, o livro ainda trata group control charts no Cap. 10, §10.3. citeturn390836view7

### A API pode mudar entre execuções

Isso não é uma violação inconveniente a ser “corrigida” estatisticamente. É justamente um candidato a **causa especial** ou **bloco**.

Se a versão puder ser identificada, registre versão, snapshot, provider, região, data, horário e parâmetros como metadados e trate a versão como bloco ou fator. Montgomery, em *Design and Analysis of Experiments*, 8ª ed., coloca blocos no Cap. 4, fatoriais nos Caps. 5 e 6, blocking/confounding de 2ᵏ no Cap. 7, robust design no Cap. 12 e random effects/variance components no Cap. 13. citeturn192494search3turn731879search9

Se a versão não puder ser identificada, você deve assumir que existe um fator latente potencialmente variável no tempo. Nesse caso:

- randomize a ordem das quatro células do 2² dentro de janelas de tempo curtas;
- execute as quatro condições do mesmo caso o mais próximo possível no tempo;
- repita o bloco em múltiplos dias;
- inclua lote/data como efeito aleatório;
- nunca interprete um salto temporal da carta como mudança intrínseca do sistema sem verificar mudança de API.

Isso é exatamente o tipo de dificuldade que torna monitoramento de ML performativo/nonstationary mais complexo do que SPC industrial clássico. Feng et al. mostram que diferentes escolhas de monitor e fonte de dados podem ter propriedades operacionais muito diferentes quando o modelo interage com o processo gerador de dados. citeturn390836view0

### Passos de uma trajetória são dependentes

Aqui eu considero **errado** usar os passos de uma trajetória como réplicas independentes.

A unidade experimental é a execução completa da trajetória sob uma condição experimental. Os passos são **unidades observacionais repetidas dentro dessa unidade**, não réplicas.

Isso dá duas análises legítimas diferentes:

- para ASR terminal, reduza cada trajetória a \(Y=1\) se o ataque teve sucesso e \(0\) caso contrário;
- para dinâmica interna, use análise de sobrevivência, modelos Markovianos, GEE, GLMM longitudinal ou outro modelo que respeite dependência temporal.

O artigo de Manakina et al. oferece um precedente muito limpo para essa segunda abordagem: define o primeiro CLAIM como evento, cria dados agent-step até evento ou censura e modela hazard discreto por regressão logística, condicionado a a trajetória ainda estar ativa. citeturn763496view2

Para SPC com autocorrelação, Montgomery trata explicitamente **SPC With Autocorrelated Process Data** no Cap. 10, §10.4, com §10.4.2 para abordagens model-based e §10.4.3 para uma abordagem model-free. citeturn192494search0turn192494search2 O tratamento canônico de Alwan e Roberts é modelar a série temporal e aplicar a carta aos **resíduos**, porque cartas clássicas sobre dados autocorrelacionados podem ser “seriously misleading”. citeturn192494search4

### Proporção perto de zero ou um

Uma carta p de três sigmas usa uma aproximação binomial/normal que pode ficar ruim quando \(n\bar p\) ou \(n(1-\bar p)\) é pequeno. Isso pode produzir limites truncados em zero/um e probabilidades de falso alarme muito diferentes da nominal. Montgomery revisa as aproximações binomial, Poisson e normal no Cap. 3 e cobre cartas de atributos e processos Bernoulli no Cap. 10, §10.11.7. citeturn192494search1turn390836view7

Para BAD-ACTS, eu não usaria automaticamente uma p-chart de 3σ se ASR estiver em 0.01, 0.99 ou se o número de trajetórias por ponto for pequeno. Preferiria:

- limites **binomiais exatos** ou calibrados por simulação;
- Bernoulli CUSUM/EWMA quando o dado chega uma trajetória por vez;
- g-chart/t-chart quando o evento de interesse é realmente raro e faz sentido monitorar número de oportunidades ou tempo entre eventos;
- modelo beta-binomial ou GLMM se houver sobredispersão por heterogeneidade de casos;
- calibração explícita do **ARL\(_0\)** ou da probabilidade de alarme por horizonte, em vez de assumir que “3 sigma” implica a propriedade desejada.

## Recomendações concretas para BAD-ACTS

Eu separaria com cuidado **experimento** de **monitoramento**.

A **unidade experimental** deve ser uma execução completa de um caso sob uma combinação específica de fatores. A **trajetória** é a realização da unidade experimental. O **caso** é um fator de bloqueio/efeito aleatório. A **paráfrase** deve ser tratada como fator de ruído ou efeito aleatório aninhado no caso. Os **passos** são medidas repetidas dentro da trajetória. A **versão da API** é bloco/fator de nuisance conhecido quando observável e fonte latente de drift quando não observável.

Para o 2², defina \(D\in\{-1,+1\}\) para defesa e \(C\in\{-1,+1\}\) para perturbação da coordenação. Para uma resposta binária por trajetória, o modelo básico deveria ser algo como

\[
\operatorname{logit} P(Y_{ijk}=1)
=
\beta_0+\beta_D D+\beta_C C+\beta_{DC}DC
+u_i+v_{ij}+b_k,
\]

em que \(u_i\) é efeito aleatório do caso, \(v_{ij}\) efeito de paráfrase dentro de caso e \(b_k\) efeito de bloco/API/dia. O parâmetro \(\beta_{DC}\) é a interação que uma ablação comum frequentemente perde. O efeito da defesa deve também ser reportado em escala de probabilidade, por exemplo diferença média de ASR ou risk ratio marginal, porque odds ratios de interação são difíceis de interpretar.

A execução deveria ser **pareada e randomizada dentro do caso**. Para cada caso/paráfrase, rode as quatro células do 2² em ordem aleatória dentro da menor janela temporal possível. Depois repita o bloco inteiro \(R\) vezes. Não faça todas as execuções “sem defesa” numa semana e todas “com defesa” na semana seguinte, pois qualquer atualização silenciosa de API ficará perfeitamente confundida com o tratamento.

Para a paráfrase, a lógica de Montgomery de robust design encaixa muito bem: fatores de controle são defesa e mecanismo de coordenação; fatores de ruído podem incluir paráfrase, formulação do ataque, idioma ou pequenas alterações ambientais. O Cap. 12 de *Design and Analysis of Experiments* cobre crossed arrays e combined arrays para robust parameter design. citeturn731879search9 Eu tenderia a um **combined array**, porque permite estimar diretamente interações controle × ruído em um único modelo.

Para SPC, use **Phase I** apenas para construir a distribuição in-control. Essa fase deveria conter execuções de uma configuração de referência claramente definida, com composição fixa ou explicitamente ajustada de casos. Remova pontos apenas quando houver causa especial documentada, não porque “ficaram fora”. Montgomery situa Phase I/II explicitamente em §5.3.7. citeturn818479search1

Na **Phase II**, o objeto monitorado deve ser escolhido de acordo com a pergunta. Se quiser detectar mudança na segurança agregada de uma API ao longo do tempo, use uma amostra sentinela fixa de casos e monitore a proporção ou um score ajustado ao risco. Se quiser detectar regressão por caso, monitore resíduos/log-likelihoods condicionais de um modelo de risco. Se quiser detectar pequenas mudanças persistentes, CUSUM/EWMA faz mais sentido do que Shewhart. Se quiser apenas comparar duas configurações numa experiência finita, eu **não usaria SPC como teste primário**. O GLMM fatorial deve ser a inferência primária; a carta deve ser uma ferramenta de estabilidade e diagnóstico.

Para validar os limites, não dependa de fórmulas assintóticas. Faça uma simulação paramétrica ou bootstrap hierárquico sob o modelo Phase I, preservando: prevalência/dificuldade por caso, número de réplicas, estrutura de paráfrase, variação entre lotes e, se relevante, autocorrelação. Depois escolha limites para obter, por exemplo, um ARL\(_0\) ou probabilidade de pelo menos um falso alarme em \(T\) pontos previamente especificado. Isso transforma a objeção “suas observações não são iid” numa pergunta operacional mensurável: **qual é o false-alarm rate real da carta sob um processo que representa a sua baseline?**

Eu também não aplicaria as regras Western Electric/Nelson automaticamente. Essas regras multiplicam oportunidades de sinal e dependem fortemente da estrutura de dependência. Montgomery trata as chamadas sensitizing rules em §5.3.6. citeturn818479search1 Se você quiser usá-las, calibre o conjunto inteiro de regras por simulação sob seu modelo Phase I.

Por fim, mantenha duas timelines. Uma é a **timeline experimental**, em que blocos e randomização impedem drift de API de contaminar efeitos causais. Outra é a **timeline operacional**, na qual versões e mudanças de API são exatamente aquilo que você quer que a carta detecte. Misturar essas duas finalidades é a principal fonte de confusão conceitual.

## O que pode dar errado com SPC em ML e LLMs

Não encontrei um artigo de alto nível cuja tese seja simplesmente “não use SPC para avaliar modelos de ML”. Encontrei, porém, três argumentos muito fortes contra o **uso ingênuo**.

O primeiro é autocorrelação. Alwan e Roberts mostram que o conceito clássico de statistical control está ligado a observações iid e que correlação serial pode tornar cartas padrão seriamente enganosas; a solução que propõem é modelar a estrutura temporal e monitorar os resíduos. citeturn192494search4 Esse argumento se aplica diretamente se você transformar os passos de uma trajetória em pontos consecutivos da carta.

O segundo é não estacionariedade/performatividade. Feng et al. mostram que quando um modelo implantado altera o ambiente que gera futuros dados, escolher “performance” como estatística monitorada parece simples, mas pode produzir inferência errada porque os dados observacionais já foram afetados pela ação do sistema. citeturn390836view0turn312366view2 Em agentes, algo análogo acontece quando uma defesa muda o comportamento dos parceiros, que por sua vez muda a distribuição de estados visitados.

O terceiro é adaptação do monitor. *Control Charts for Multi-Agent Systems* mostra um resultado especialmente relevante para segurança: um monitor fixo pode sinalizar aprendizagem legítima como anomalia, mas um monitor adaptativo pode absorver uma mudança adversarial lenta. citeturn390836view1 Isso é uma demonstração concreta de que “acomodar drift” e “detectar ataque” podem ser objetivos incompatíveis.

Há ainda um problema de prática de SPC: se o modelo Phase I estiver errado, uma sequência de alarmes pode simplesmente significar que os limites estão mal especificados. Uma revisão recente sobre prática de cartas de controle ressalta que falsos alarmes frequentes podem indicar que o modelo Phase I já não é válido e que limites precisam ser reestimados, além de advertir que “detectar antes” em um dataset retrospectivo pode apenas significar um falso alarme mais cedo. citeturn665078search0

Em resumo, a defesa metodológica mais forte para sua dissertação não seria afirmar que “LLMs são processos industriais e portanto as cartas tradicionais valem”. Seria afirmar algo mais restrito e defensável: **SPC fornece uma linguagem e uma família de procedimentos sequenciais para distinguir flutuação esperada de mudança estrutural, mas o modelo in-control precisa representar explicitamente heterogeneidade de casos, dependência temporal, drift de API e resposta binária discreta; os limites devem ser calibrados para esse modelo, e a inferência causal do fatorial deve permanecer separada do monitoramento sequencial.**

## Trabalhos e referências citados

| título | ano | identificador | local | revisado por pares? | relevância | o que ele faz e o que não faz em relação à pergunta |
|---|---:|---|---|---|---|---|
| *Control Charts for Multi-Agent Systems*, Hayden Helm, Carey Priebe, Brandon Duderstadt | 2026 | arXiv:2605.11135 | arXiv; aparece na página oficial de downloads NeurIPS 2026, mas não encontrei entrada de proceedings para conferir | **não conferido** | alta | Aplica cartas adaptativas a sistemas multiagentes generativos e estuda adversários lentos; não é uma carta p/I-MR sobre ASR de benchmark nem DOE de segurança. citeturn390836view1turn782222search0 |
| *Beyond Benchmarks: Toward Causally Faithful Evaluation of Large Language Models*, Zhengshuyuan Tian et al. | 2026 | PMLR v306 | 43rd ICML, PMLR 306 | sim, conferência principal | alta | DOE explicitamente fatorial, com efeitos principais e interações em avaliação de LLM; não é focado em segurança ou SPC. citeturn390836view2 |
| *CAFE: A Compound-AI Factorial Evaluation Framework*, Fabian Lukassen, Christoph Weisser, Thomas Kneib, Alexander Silbersdorff | 2026 | DOI 10.18653/2026.emnlp-demos.50; arXiv:2607.10380 | EMNLP 2026 System Demonstrations | sim, demo track | alta | Constrói desenhos fatoriais para sistemas compostos e estima efeitos/interações com mixed models; demonstra em RAG, não segurança. citeturn390836view3 |
| *Evaluation of Multi-Turn Consistency in LLM Agents: Survival Analysis and Failure-Rationale Taxonomy*, Olga Manakina, Igor Bogdanov, Chung-Horng Lung | 2026 | OpenReview, ICLR 2026 | ICLR 2026 | sim, conforme manuscrito publicado como conference paper | alta | Full factorial em agentes, 64 condições por modelo, e análise de hazard para dependência entre passos; não trata ataque/defesa nem SPC. citeturn763496view0turn763496view2 |
| *Voices Across Registers: Corpus-Conditioned Vernacular Jailbreaks against Aligned LLMs via Fanfiction Subgenres*, Zhongze Luo et al. | 2026 | DOI 10.18653/2026.emnlp-main.1148 | EMNLP 2026 main | sim, conferência principal | alta | Segurança/jailbreak com decomposição fatorial do efeito de registro, comprimento e estrutura; não é avaliação de agente multiagente nem carta de controle. citeturn584994view6 |
| *Does Safety Reasoning Travel? A Multilingual Measurement of Prompt-Injection Attacks and Runtime Monitors in Tool-Using LLM Agents*, Ruiyang Zhang | 2026 | DOI 10.18653/2026.oracle-main.13 | ORACLE Workshop, ACL Anthology | sim, workshop | alta | Segurança de agentes, desenho pareado e controle por paráfrase; mostra confounding por tradução/memorização. Não usa DOE fatorial formal nem SPC. citeturn584994view7 |
| *Quantifying Variance in Evaluation Benchmarks*, Lovish Madaan et al. | 2024 | arXiv:2406.10229 | NeurIPS 2024 Workshop RegML | sim, workshop | alta | Trata variância de benchmark, inclusive seed variance; não faz Gauge R&R literal, factorial DOE ou SPC. citeturn104848view0 |
| *Towards Reproducible LLM Evaluation: Quantifying Uncertainty in LLM Benchmark Scores*, Robert E. Blackwell, Jon Barry, Anthony G. Cohn | 2024 | arXiv:2410.03492 | preprint | não | alta | Formaliza repetição do mesmo benchmark e intervalos preditivos entre repetições; não usa cartas de controle ou DOE. citeturn584994view1turn104848view2 |
| *Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations*, Evan Miller | 2024 | arXiv:2411.00640 | preprint | não conferido, encontrei apenas arXiv | alta | Erros padrão, clusters, reamostragem, comparação pareada e power analysis; não usa SPC ou fatorial. citeturn584994view3 |
| *Lessons from the Trenches on Reproducible Evaluation of Language Models*, Stella Biderman et al. | 2024 | arXiv:2405.14782 | CoRR/preprint | não encontrei publicação formal | média | Discute reprodutibilidade e sensibilidade a detalhes de implementação; não decompõe variância como Gauge R&R e não usa SPC. citeturn584994view2turn104848view1 |
| *How Consistent Are LLM Agents? Measuring Behavioral Reproducibility in Multi-Step Tool-Calling Pipelines*, Abel Yagubyan | 2026 | arXiv:2605.28840 | preprint | não | alta | Repete tarefas idênticas com ferramentas determinísticas para medir variabilidade comportamental de agentes; não é Gauge R&R formal e não usa SPC. citeturn104848view4 |
| *ReasonBENCH: Benchmarking the (In)Stability of LLM Reasoning*, Nearchos Potamitis, Lars Klein, Akhil Arora | 2025 | arXiv:2512.07795 | CoRR/preprint | não encontrei venue revisado | média | Avaliação multi-run orientada a distribuições; não usa SPC nem DOE fatorial. citeturn104848view3turn755262search10 |
| *Designing Monitoring Strategies for Deployed Machine Learning Algorithms: Navigating Performativity through a Causal Lens*, Jean Feng et al. | 2024 | PMLR 236 | 3rd Conference on Causal Learning and Reasoning | sim | alta | Combina causal inference e SPC, mostra que monitoramento depende do mecanismo de dados e performatividade; não é LLM. citeturn390836view0turn312366view2 |
| *Risk-adjusted monitoring of binary surgical outcomes*, Stefan H. Steiner, Richard J. Cook, Vern T. Farewell | 2001 | DOI 10.1177/0272989X0102100301 | *Medical Decision Making* 21(3):163-169 | sim, periódico | alta | CUSUM ajustado ao risco para outcomes binários heterogêneos; referência direta para case-mix de ataques, não LLM. citeturn390836view5 |
| *Time-Series Modeling for Statistical Process Control*, Layth C. Alwan, Harry V. Roberts | 1988 | DOI 10.1080/07350015.1988.10509640 | *Journal of Business & Economic Statistics* 6(1):87-95 | sim, periódico | alta | Mostra que autocorrelação torna cartas padrão enganosas e propõe charting dos resíduos de modelos de séries temporais; não LLM. citeturn192494search4 |
| *Monitoring Univariate Processes Using Control Charts: Some Practical Issues and Advice* | 2023 | DOI 10.1080/08982112.2023.2238049 | *Quality Engineering* | sim, periódico | média | Discute Phase I/II, manutenção do modelo, falso alarme e perigos de conclusões retrospectivas; não específico de ML/LLM. citeturn665078search0 |
| *Introduction to Statistical Quality Control*, Douglas C. Montgomery, 7ª ed. | 2012/2013 | ISBN 978-1-118-14681-1 | Wiley, livro | livro-texto acadêmico, não artigo | alta | Cap. 5: causas comum/especial, subgrupos racionais, regras, Phase I/II; Cap. 10: autocorrelação, múltiplos fluxos, Bernoulli e saúde; Cap. 8: Gauge R&R. citeturn818479search0turn818479search1turn390836view7 |
| *Design and Analysis of Experiments*, Douglas C. Montgomery, 8ª ed. | 2012/2013 | ISBN 978-1-118-14692-7 | Wiley, livro | livro-texto acadêmico, não artigo | alta | Caps. 4-8: blocking e fatoriais; Cap. 11: response surfaces; Cap. 12: robust design/noise factors; Cap. 13: random factors e variance components; Cap. 14: nested/split-plot. citeturn731879search9turn731879search11 |
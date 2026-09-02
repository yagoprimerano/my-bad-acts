# Robustez e Estatística na Avaliação Adversarial de Agentes LLM: Investigação de Novidade e Posicionamento

**Documento de trabalho para reunião de orientação**
Programa de Mestrado em Sistemas de Informação — EACH-USP / C4AI
Data: agosto de 2026

---

## 1. Por que esta investigação foi feita

A apresentação que discutimos deixou duas apostas de contribuição no centro do trabalho: (i) tratar **robustez** como propriedade de primeira classe na avaliação de ataques adversariais a agentes LLM, ancorando-se na afirmação de Li et al. (2026, arXiv:2605.16282) de que a categoria de risco R10 (*Robustness & Reliability*) é a única com **zero benchmarks primários**; e (ii) unir a avaliação adversarial de agentes a um aparato **estatístico rigoroso** (intervalos de confiança, cartas de controle, delineamento de experimentos).

Antes de comprometer tempo e recursos em expandir os experimentos para um número maior de execuções — o requisito central do paper que a senhora sugeriu coautorar —, era preciso responder, com honestidade e com base em fontes primárias, a duas perguntas que determinam se essas apostas se sustentam diante de uma banca:

1. **A lacuna de robustez é real?** Nenhum benchmark cobre robustez como foco em contexto adversarial de agentes? E, se é verdade, *por que* a área teria deixado isso de lado, dado que robustez é um tema trivial na pesquisa de LLMs? Existe um desafio escondido, ou é apenas terreno inexplorado? Quão exclusivo eu seria ao ocupá-lo?
2. **Combinar ataques adversariais com estatística é novidade?** Isso já foi muito feito, pouco feito, ou é território aberto? Quão inovador, e em que sentido exato?

Este documento consolida os achados da investigação e traduz cada um deles em uma recomendação de posicionamento.

## 2. Como a investigação foi conduzida

O levantamento priorizou **fontes primárias**: preprints do arXiv, anais de ICLR/NeurIPS/ICML/ACL/EMNLP/USENIX Security (2023–2026) e o próprio artigo-âncora. Cada afirmação de novidade foi testada de forma **adversarial** — isto é, busquei ativamente o trabalho que *derrubaria* a alegação, não apenas os que a confirmam. Referências candidatas a "concorrentes" foram verificadas individualmente quanto à existência, autoria e conteúdo, para evitar apoiar o argumento em citações imprecisas. O resultado abaixo distingue deliberadamente dois graus de novidade: **"ninguém fez exatamente isto"** (novidade estreita) e **"esta é uma direção genuinamente inexplorada"** (novidade ampla) — a diferença é o que decide a defensabilidade.

## 3. Achado 1 — A lacuna de robustez é real, mas é preciso reivindicá-la com precisão cirúrgica

**A resposta curta: sim, a lacuna existe e é confirmada por múltiplas fontes independentes — porém ela é específica do subcampo de *benchmarks de segurança de agentes*, e está se fechando rapidamente.**

### 3.1 A lacuna se confirma

A afirmação de Li et al. não é isolada. O corpus de 40 benchmarks comportamentais que eles catalogam mostra R10 com **0 primários e 7 parciais** (Agent-SafetyBench, ST-WebAgentBench, SafeAgentBench, AGENTSAFE, IS-Bench, BAD-ACTS, AgentLAB), e a explicação estrutural é consistente: o corpus é dominado por avaliações de **disparo único, em sandbox, com pontuação baseada em regras**, com "pouquíssimo teste de perturbação repetida, análise em nível de disposição ou medição longitudinal". Nenhum benchmark testa, como objetivo primário, consistência comportamental sob perturbações semanticamente equivalentes, cascata de erros em planos multietapas, ou ações movidas por alucinação.

Fontes independentes corroboram a mesma fragilidade metodológica. Lunardi et al. (ECAI 2025, arXiv:2509.04013) parafrasearam sistematicamente as perguntas de seis benchmarks consagrados e mediram 34 LLMs: embora o *ranking* dos modelos permaneça estável, o **desempenho absoluto cai de forma significativa** sob reformulação — evidência direta de que benchmarks superestimam robustez e de que "notas altas podem não capturar a robustez a variações reais de entrada". No plano dos agentes, o survey de avaliação de agentes LLM (arXiv:2507.21504) reconhece que, sendo os LLMs não-determinísticos, os agentes exibem variabilidade de comportamento que exige consistência entre execuções repetidas — mas nota que o campo raramente a mede. A convergência de um survey de segurança, um estudo empírico de paráfrase e um survey de avaliação de agentes sobre o mesmo diagnóstico dá solidez à premissa.

### 3.2 Por que a área "fechou os olhos" — e o desafio escondido que você precisa conhecer

A questão mais importante da sua pergunta era *por quê*. A investigação aponta quatro causas concretas, e a última é o desafio técnico que estava oculto:

- **Fixação no ASR de disparo único.** Os benchmarks de segurança dominantes (AgentDojo, ASB, InjecAgent, TAMAS) reportam taxa de sucesso de ataque de uma única execução. A métrica é herdada da cultura de "novo ataque, nova taxa", que premia demonstrar vulnerabilidade, não caracterizar sua estabilidade.
- **Custo computacional da repetição.** Robustez exige rodar cada cenário muitas vezes. Quando cada trajetória agêntica leva minutos e envolve chamadas de API pagas, repetir 5–25 vezes multiplica custo — e múltiplos artigos de 2026 declaram explicitamente rodar cada instância uma única vez "devido ao alto custo computacional". É inércia econômica, não desinteresse.
- **Incentivos de publicação** favorecem ataques novos sobre estudos de confiabilidade.
- **O desafio escondido — e é o ponto crucial:** o não-determinismo do LLM torna a variância *difícil de interpretar*. Sob não-associatividade de hardware, roteamento de especialistas em modelos MoE e efeitos de batch, a variação entre rodadas é um **confundidor**, não um sinal limpo. O instinto da área foi **suprimir** essa variância (temperatura zero, fixação de *seed*) em vez de **medi-la e caracterizá-la**. Ou seja: não é que não haja o que explorar — é que caracterizar robustez exige tratar a variância como objeto de estudo e importar um ferramental (delineamento experimental, métricas cientes de variância) que os autores de benchmark majoritariamente não incorporaram. **É exatamente aí que o seu trabalho entra.** A dificuldade que afastou os outros é a oportunidade metodológica que você ocupa.

### 3.3 O ponto de honestidade: a janela está se fechando

A parte crítica — e a que mais protege você numa banca — é reconhecer que a "lacuna de robustez", *tomada de forma ampla*, já não é território vazio. Uma onda de trabalhos de 2026 ocupa o espaço geral de "confiabilidade / avaliação ciente de variância":

- **"Towards a Science of AI Agent Reliability" (Princeton, arXiv:2602.16666)** — o concorrente conceitual mais forte. Decompõe confiabilidade em consistência, robustez, previsibilidade e segurança, com 12 métricas "fundamentadas em engenharia crítica de segurança", avaliando 14 modelos. Já reivindica "confiabilidade como lente primária" — porém é **agente único e não-adversarial**.
- **"Consistency as a Testable Property" (arXiv:2605.10516)** — usa estatísticas-U para separar confiabilidade observável (nível de saída) de interna (nível de trajetória). Muito próximo do seu enquadramento estatístico.
- **ReasonBench (arXiv:2512.07795, Potamitis, Arora et al.)** — repete cada configuração modelo×estratégia×tarefa em múltiplos *trials* independentes e reporta intervalos de confiança; mostra que a estratégia melhor "vence apenas 77% dos confrontos diretos". É sobre estabilidade de **estratégias de raciocínio**, não sobre multiagente adversarial.
- **"How Consistent Are LLM Agents?" (arXiv:2605.28840)** — 1.140 traços, consistência estrutural vs. paramétrica, com ICs de 95%.

**Conclusão do Achado 1.** Fazer robustez a lente primária *para agentes em geral* deixou de ser amplamente novo no início de 2026. O que permanece **defensavelmente vazio** é a interseção tríplice: **adversarial × multiagente (R5) × robustez em nível de trajetória, quantificada estatisticamente**. Nenhum dos concorrentes acima combina os três — Princeton e ReasonBench não são adversariais nem multiagentes; os benchmarks multiagentes (BAD-ACTS, TAMAS) não tratam robustez como categoria autônoma. **A célula R10 × R5 é o quadrado que você deve reivindicar explicitamente — não "robustez", e sim esse cruzamento.**

## 4. Achado 2 — Estatística + adversarial: a novidade não está no rigor estatístico, está no paradigma industrial de controle

**A resposta curta: rigor estatístico aplicado à avaliação adversarial está *emergindo* e já não é exótico; mas o enquadramento específico de Controle Estatístico de Qualidade industrial (SPC/SQC) e Delineamento de Experimentos aplicado à segurança adversarial multiagente é genuinamente desocupado.** São duas conclusões que precisam andar juntas.

### 4.1 Rigor estatístico genérico já não é, por si só, a contribuição

Vários trabalhos recentes já acoplam estatística formal à avaliação:

- **Spark-LLM-Eval (arXiv:2603.28769, Mitra, jan. 2026)** — framework de avaliação em que **toda métrica** vem com intervalo de confiança por *bootstrap* e testes de significância (t pareado, McNemar, Wilcoxon). O próprio autor argumenta que "a maioria dos frameworks entrega estimativas pontuais e considera o trabalho concluído", tornando os ICs "não-opcionais".
- **ReasonBench** (acima) institucionaliza o *multi-run* com métricas cientes de variância.
- **Miller, "Adding Error Bars to Evals" (Anthropic, arXiv:2411.00640)** já tornou mainstream a tese de que "avaliações são experimentos" e que a literatura de avaliação ignorou a literatura de análise experimental.
- **O próprio Li et al.** usa intervalos de Wilson e W de Kendall; **TAMAS** e o estudo da Frontiers (abaixo) também empregam estatística formal.

Isto é decisivo: **"adicionar barras de erro / ICs à avaliação adversarial" é incremental**, não a sua tese. Apresentar isso como a inovação central seria vulnerável — a banca conhece esses trabalhos.

### 4.2 Onde a novidade é genuína — o paradigma SPC/DOE

A busca dedicada por trabalho anterior que aplique **cartas de controle de Shewhart (cartas p, I-MR), regras da Western Electric, distinção causa-comum vs. causa-especial (Montgomery) e delineamento fatorial (DOE)** à **segurança de agentes LLM / avaliação de injeção de prompt / red-teaming de IA** **não encontrou nenhum artigo**. O prior art mais próximo está todo em *outros* domínios:

- CUSUM + citação explícita de Montgomery para detecção de clientes adversariais em aprendizado federado (arXiv:2310.01537);
- CUSUM com limites de controle para detecção de ataque em sistemas ciberfísicos (arXiv:2105.10707);
- SPC para detecção de *drift* de conceito em ML e monitoramento de *out-of-distribution*.

Nenhum deles trata agentes LLM sob ataque adversarial. O estudo mais próximo no seu domínio — um trabalho da Frontiers (2026) sobre robustez adversarial de sistemas multiagentes LLM em problemas de engenharia — chega a usar intervalos exatos de Clopper–Pearson, teste exato de Fisher e V de Cramér, além de identificar um "efeito de primeiro movimento" (líder), mas **não** organiza isso como um DOE fatorial estilo Montgomery nem como monitoramento por cartas de controle.

**Conclusão do Achado 2.** A contribuição defensável **não é** a estatística em si, e sim **reconceituar a avaliação adversarial multiagente como um problema de Controle Estatístico de Processo**: tratar o time de agentes como uma "linha de produção", distinguir a **variação de causa-comum** (o não-determinismo inerente do LLM) da **variação de causa-especial** (a mudança induzida pelo ataque ou pela defesa), e usar cartas p / I-MR + regras de corrida + DOE 2×2 (defesa × perturbação, com efeitos principais e interação) para detectar quando o ataque empurra o processo "para fora de controle". **Novidade: ALTA para o paradigma SPC/DOE; BAIXA para estatística genérica.**

## 5. Síntese — onde exatamente está a sua contribuição

As duas frentes convergem para o mesmo enquadramento estratégico, o que é uma boa notícia: elas se reforçam.

> Reconceituamos a avaliação adversarial de sistemas multiagentes de LLM como um problema de **controle estatístico de processo**. Onde os benchmarks existentes reportam taxa de sucesso de ataque de disparo único — e onde Li et al. (2026) mostram que R10 é 0-primário e que os rankings de benchmark são não-concordantes (W = 0,10, p = 0,94) — tratamos o sistema multiagente como um processo cuja característica de qualidade é a conclusão segura da tarefa. Distinguimos variação de causa-comum (estocasticidade do LLM) de causa-especial (ataque/defesa) via cartas p e I-MR, quantificamos confiabilidade entre rodadas e consistência sob perturbação com intervalos de Wilson, e usamos DOE fatorial 2×2 para estimar efeitos principais e interações. É a primeira aplicação de SQC/DOE industrial à segurança adversarial multiagente e a primeira a tornar robustez (R10) uma lente primária, em nível de trajetória, no cenário multiagente (R5).

Note a distinção terminológica que deve ser respeitada: o Eixo 5 de Li et al. chama-se **"granularidade de avaliação"**, e o artigo **não** usa a palavra "trajetória". O vocabulário de "trajetória" alinha-se ao SafeAgents/DHARMA e ao ATBench — use "granularidade" ao citar Li et al. e "trajetória" ao se posicionar, sem atribuir esse termo ao artigo-âncora.

## 6. Objeções que a banca provavelmente levantará (e como responder)

Preparar as respostas agora é o que transforma "achei estranho" em "domino o terreno".

1. **"Princeton já fez da confiabilidade a lente primária (arXiv:2602.16666)."** → Aquele trabalho é agente único, não-adversarial e usa uma decomposição própria de 12 métricas, não um paradigma de controle SPC. Você acrescenta pressão adversarial, topologia multiagente (R5) e a decomposição causa-comum/causa-especial.
2. **"Estatística sobre ASR já é padrão (Wilson, bootstrap; Li et al., Spark-Eval, Miller)."** → A contribuição é o *paradigma de controle* (cartas, regras de corrida, estabilidade de processo, sinal de fora-de-controle), não os intervalos de confiança.
3. **"SPC é apenas detecção de *drift* rebatizada."** → O SPC de *drift* monitora distribuição de entrada em cenário benigno; aqui ele é um framework **experimental** para contrastar ataque/defesa e separar o sinal de causa-especial do ruído de causa-comum do LLM.
4. **"Cartas de controle pressupõem observações i.i.d. e um processo estável — o não-determinismo do LLM e a heterogeneidade dos prompts violam isso."** → **Esta é a objeção mais séria e substantiva.** Não pode ser respondida com acenos. Exige tratar autocorrelação entre passos da trajetória, racionalização de subgrupos e a validade dos limites de controle sob não-determinismo. Plano de mitigação: cartas I-MR para execuções individuais, cartas p para proporção-defeituosa entre tarefas subgrupadas, e — se as suposições não se sustentarem empiricamente — migrar de Shewhart para **EWMA/CUSUM** (tolerantes a autocorrelação), reenquadrando como "SQC de monitoramento sequencial". Uma análise de poder formal para o DOE 2×2 deve acompanhar.
5. **"DOE 2×2 é suficiente?"** → Antecipar com justificativa da resolução do design e discussão de extensão fatorial fracionada.

## 7. Recomendações de posicionamento para o paper

1. **Reformular a alegação de novidade.** Não afirmar "robustez é inexplorada". Afirmar a célula vazia específica: *robustez adversarial × multiagente × nível de trajetória, operacionalizada via SPC/DOE industrial*. Citar o R10 = 0-primário de Li et al. como **evidência motivadora**, não como prova de ausência total, e reconhecer explicitamente Princeton e arXiv:2605.10516 para demonstrar domínio da literatura recente.
2. **Liderar com o eixo SPC/SQC como contribuição primária.** É onde a novidade é genuinamente alta. Enquadrar a metodologia estatística industrial como *a contribuição*, com o cenário adversarial multiagente como *domínio de aplicação*.
3. **Dedicar um parágrafo a neutralizar o concorrente de Princeton**, articulando com precisão o que ele faz (agente único, não-adversarial) versus o que a dissertação acrescenta.
4. **Blindar a estatística contra a objeção i.i.d./estabilidade** desde o desenho experimental — não como remendo posterior.
5. **Respeitar a terminologia** ("granularidade" para Li et al.; "trajetória" para SafeAgents/DHARMA).

Essas cinco medidas convertem uma janela de novidade que está se estreitando em uma contribuição estreita, mas robusta e sustentável — que é exatamente o tipo de alegação que sobrevive a uma banca.

## 8. Referências-chave (verificadas)

- Li, Fung, Li, Ismail, Iqbal. *Taxonomy and Consistency Analysis of Safety Benchmarks for AI Agents.* arXiv:2605.16282 (2026). — artigo-âncora.
- *Towards a Science of AI Agent Reliability.* arXiv:2602.16666 (2026, Princeton). — concorrente conceitual mais próximo.
- *Consistency as a Testable Property: Statistical Methods to Evaluate AI Agent Reliability.* arXiv:2605.10516 (2026).
- Potamitis, Arora et al. *ReasonBENCH: Benchmarking the (In)Stability of LLM Reasoning.* arXiv:2512.07795 (2025–2026).
- *How Consistent Are LLM Agents?* arXiv:2605.28840 (2026).
- Lunardi, Della Mea, Mizzaro, Roitero. *On Robustness and Reliability of Benchmark-Based Evaluation of LLMs.* ECAI 2025 / arXiv:2509.04013.
- Mitra. *Spark-LLM-Eval: A Distributed Framework for Statistically Rigorous LLM Evaluation.* arXiv:2603.28769 (2026).
- Miller. *Adding Error Bars to Evals.* arXiv:2411.00640 (Anthropic, 2024).
- Debenedetti et al. *AgentDojo.* NeurIPS 2024 / arXiv:2406.13352.
- Zhang, Cui et al. *Agent-SafetyBench.* arXiv:2412.14470 (2024).
- Kavathekar et al. *TAMAS.* arXiv:2511.05269 (2025).
- SPC + adversarial (outros domínios): arXiv:2310.01537 (federado, CUSUM + Montgomery); arXiv:2105.10707 (sistemas ciberfísicos, CUSUM).
- Cascatas multiagente: CASPIAN, arXiv:2605.19240.
- Survey de avaliação de agentes: arXiv:2507.21504.

---

*Nota de status: quase todos os concorrentes são preprints de 2026, majoritariamente ainda não revisados por pares — "desocupado" deve ser afirmado como "nenhum trabalho anterior encontrado até agosto de 2026", não como um absoluto. AgentDojo (NeurIPS 2024) e Agent-SafetyBench (dez. 2024) são as âncoras revisadas por pares mais sólidas.*

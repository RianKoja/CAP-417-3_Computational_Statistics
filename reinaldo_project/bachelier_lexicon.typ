// bachelier_lexicon.typ
// Part A — Historical Lexicon and Generative AI

#import "@preview/touying:0.3.0": *
#import "refs.typ": refs

#let part-a-slides() = {
  // Section separator
  #slide[
    = Parte A — Léxico Histórico e IA

    - Cientista escolhido: Louis Jean-Baptiste Alphonse Bachelier (1870–1946).[refs.bachelier-wiki][refs.bachelier-bio]
    - Pioneiro da modelagem estocástica de preços e “pai” da matemática financeira moderna.[refs.bachelier-wiki][refs.bachelier-bio][refs.bachelier-centenary]
  ]

  // Biography slide
  #slide[
    = Louis Bachelier — Visão Geral

    - Matemático francês, tese de doutorado *Théorie de la spéculation* defendida em 1900 na Sorbonne.[refs.bachelier-wiki][refs.bachelier-bio]
    - Primeira modelagem matemática de um movimento Browniano, aplicada a preços de ativos na Bolsa de Paris.[refs.bachelier-wiki][refs.bachelier-centenary]
    - Trabalho antecipou conexões entre passeios aleatórios, equação do calor e processos de Wiener, influenciando Wiener, Kolmogorov, Itô e a formulação posterior de Black–Scholes–Merton.[refs.bachelier-bio][refs.bachelier-centenary][refs.davis-bachelier]
  ]

  // Conceptual lexicon — core ideas
  #slide[
    = Léxico Conceitual — Ideias Centrais

    - Passeio aleatório em preços: variações consideradas essencialmente aleatórias e independentes em horizontes curtos.[refs.bachelier-wiki][refs.century-kabanov]
    - Movimento Browniano em finanças: limite contínuo de passeios aleatórios, com incrementos normais e independentes no tempo.[refs.bachelier-centenary][refs.davis-bachelier]
    - Modelo normal aditivo: preço (não o log-preço) é modelado como processo normal, ao contrário do modelo lognormal de Black–Scholes.[refs.bachelier-wiki][refs.option-bachelier-vs-bs]
    - Dinâmica descrita por equações de difusão tipo equação do calor, ligando probabilidades de transição e densidades.[refs.bachelier-centenary][refs.davis-bachelier]
  ]

  // Typical mathematical language
  #slide[
    = Léxico Matemático Típico

    - Processo estocástico contínuo \(X_t\) representando o preço ou “desvio” em relação a um valor fundamental.
    - Incrementos normais: \(X_{t+\Delta t} - X_t \sim \mathcal{N}(0, \sigma^2 \Delta t)\) sob hipóteses ideais de mercado.[refs.bachelier-wiki][refs.bachelier-centenary]
    - Densidades de transição satisfazendo uma PDE de difusão, análoga à equação do calor de Fourier.[refs.bachelier-centenary][refs.bachelier-bio]
    - Uso precoce de relações do tipo Chapman–Kolmogorov contínuo para composição de probabilidades ao longo do tempo.[refs.bachelier-bio][refs.davis-bachelier]
  ]

  // Area of activity and style
  #slide[
    = Área de Atuação e Estilo

    - Área primária: matemática financeira, modelando preços de títulos, opções e outros derivativos na Bolsa de Paris.[refs.bachelier-wiki][refs.bachelier-bio]
    - Contribuições centrais em probabilidade contínua: movimento Browniano, ligação passeio aleatório–difusão e reflexão para máximos.[refs.bachelier-bio][refs.bachelier-centenary]
    - Estilo: empiricamente motivado, com argumentos probabilísticos e PDEs, anterior ao formalismo de Kolmogorov; focado em modelos tratáveis com fórmulas explícitas.[refs.bachelier-bio][refs.bachelier-centenary]
  ]

  // Problems investigated
  #slide[
    = Problemas Estudados por Bachelier

    - Representar matematicamente a aleatoriedade das flutuações de preços em mercados especulativos.[refs.bachelier-wiki][refs.history-datascience]
    - Derivar a distribuição de preços futuros a partir de hipóteses sobre infinitesimais de preço e difusão.[refs.bachelier-centenary][refs.davis-bachelier]
    - Valorizar opções (incluindo barreira) via expectativa de payoffs sob a lei estocástica dos preços.[refs.bachelier-bio][refs.davis-bachelier]
  ]

  // Modern applications
  #slide[
    = Aplicações Modernas do Modelo de Bachelier

    - Modelos aditivos para taxas de juro, commodities ou ativos que podem assumir valores negativos (modelo normal em vez de lognormal).[refs.option-bachelier-vs-bs]
    - Referência pedagógica em cursos de cálculo estocástico e engenharia financeira, por permitir fórmulas explícitas simples.[refs.bachelier-bio][refs.davis-bachelier]
    - Ponto de partida para comparar precificação tipo Bachelier vs. Black–Scholes em dados reais e analisar volatilidade implícita.[refs.option-bachelier-vs-bs]
  ]

  // Contemporary question slide
  #slide[
    = Pergunta Contemporânea para Bachelier

    *Prompt resumido a ser passado a um agente de IA:*

    > “Em um ambiente de negociação de alta frequência e grandes volumes de dados financeiros, como estender o passeio aleatório clássico para capturar caudas pesadas, clustering de volatilidade e efeitos de microestrutura? E como integrar tais modelos estocásticos com métodos modernos de aprendizado de máquina focados em previsão de risco, e não de níveis de preço?”

    - Esta pergunta liga diretamente o modelo original de passeio aleatório Gaussiano às preocupações atuais com caudas e volatilidade condicionais.
    - Mais adiante na apresentação, você irá preencher os resultados de agentes de IA que gerarem variações desta pergunta ou refinamentos de vocabulário.
  ]
}
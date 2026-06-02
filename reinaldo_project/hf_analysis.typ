// hf_analysis.typ
// Part C — Applied Computational Statistical Analysis (with placeholders)

#import "@preview/touying:0.3.0": *
#import "refs.typ": refs

#let part-c-slides() = {
  #slide[
    = Parte C — Análise Aplicada

    - Contexto: dados de alta frequência (por ex., 1-min) de um índice líquido (futuros de S&P 500, ETF amplo, ou outro ativo representativo).[refs.history-datascience]
    - Objetivo: confrontar o passeio aleatório Gaussiano de Bachelier com evidências modernas de caudas pesadas, clustering de volatilidade e microestrutura.
  ]

  // Dataset choice
  #slide[
    = Escolha do Conjunto de Dados

    - Dataset alvo: preços intradiários (timestamp, preço, volume) em frequência fixa (ex.: 1-min) ao longo de vários meses.[refs.history-datascience]
    - Link conceitual: modelo normal de Bachelier como “modelo nulo”; desvios empíricos motivam extensões GARCH, saltos, ML para risco.
    - [PLACEHOLDER] Especificar ativo e período exatos após coleta via API (Ex.: `SPY`, `ES`, índice local, etc.).
  ]

  // Methodology overview
  #slide[
    = Metodologia — Visão Geral

    1. Pré-processamento e cálculo de retornos (logs, limpeza de outliers, alinhamento temporal).
    2. EDA: séries de preços/retornos, histograma, ECDF, QQ-plot vs. normal.[refs.history-datascience]
    3. Testes de passeio aleatório: ACF/PACF de retornos e retornos ao quadrado, testes Ljung–Box.
    4. Modelos de heterocedasticidade condicional: GARCH(1,1) e variantes.
    5. Análise de caudas: estimadores de índice de cauda, POT (peaks-over-threshold).
    6. Integração com ML: previsão de volatilidade/risco, não de nível de preço.
  ]

  // Preprocessing & EDA slide with code placeholder
  #slide[
    = Pré-processamento e EDA

    - Construir retornos \(r_t = \log(P_t) - \log(P_{t-1})\) e remover timestamps com dados faltantes ou volumes anômalos.
    - [PLACEHOLDER-GRÁFICO-1] Gráfico de série temporal dos retornos intradiários.
    - [PLACEHOLDER-GRÁFICO-2] Histograma e QQ-plot dos retornos vs. normal para avaliar Gaussianidade.
    - [PLACEHOLDER-CÓDIGO] Inserir trecho de código Python/Julia usado para EDA (pandas, matplotlib, etc.).
  ]

  // Random walk tests
  #slide[
    = Teste da Hipótese de Passeio Aleatório

    - Avaliar ACF/PACF de retornos e retornos ao quadrado; expectativa Bachelier: pouca autocorrelação em retornos e variância constante.[refs.history-datascience]
    - Aplicar testes Ljung–Box para autocorrelação em diferentes defasagens.
    - [PLACEHOLDER-GRÁFICO-3] ACF de retornos.
    - [PLACEHOLDER-GRÁFICO-4] ACF de retornos ao quadrado.
    - [PLACEHOLDER-TABELA-1] Tabela com estatísticas Ljung–Box (lags, estatística, p-valor).
  ]

  // GARCH modeling
  #slide[
    = Modelagem de Volatilidade Condicional

    - Ajustar um modelo GARCH(1,1) sobre retornos (por exemplo, usando `arch` em Python) para capturar clustering de volatilidade.[refs.history-datascience]
    - Comparar ajuste com modelo de variância constante (passeio aleatório Gaussiano de Bachelier).
    - [PLACEHOLDER-GRÁFICO-5] Série temporal da volatilidade condicional estimada.
    - [PLACEHOLDER-TABELA-2] Tabela com parâmetros do GARCH, erros-padrão e medidas de ajuste (AIC/BIC).
  ]

  // Heavy tails and extremes
  #slide[
    = Caudas Pesadas e Extremos

    - Estimar índices de cauda (p. ex., estimador de Hill) para retornos positivos e negativos.
    - Implementar abordagem POT (peaks-over-threshold) para excedências acima de um quantil alto (ex.: 99%).
    - [PLACEHOLDER-GRÁFICO-6] Plot de Hill ou gráfico de quantil-excedência.
    - [PLACEHOLDER-TABELA-3] Estimativas de parâmetros de cauda e comparação com normal.
  ]

  // ML for risk
  #slide[
    = IA e Previsão de Risco

    - Construir features simples: volatilidade recente, magnitude de retornos recentes, hora do dia, volume, possivelmente proxies de fluxo de ordens.
    - Treinar modelos (Random Forest, Gradient Boosting, Redes Neurais leves) para prever volatilidade ou medida de risco (ex.: VaR intradiário) em vez de preço.
    - [PLACEHOLDER-GRÁFICO-7] Curvas de previsão vs. volatilidade observada ou VaR empírico.
    - [PLACEHOLDER-TABELA-4] Métricas de desempenho (MSE, cobertura de VaR, etc.) comparando modelos.
    - [PLACEHOLDER-CÓDIGO-ML] Inserir trecho de código com pipeline de ML (train/test split, baseline vs. modelo).
  ]

  // Interpretative slide
  #slide[
    = Interpretação Estatística e Financeira

    - Retornos com baixa autocorrelação mas forte autocorrelação em retornos ao quadrado sugerem martingale em nível de preço, mas volatilidade condicionada — indo além de Bachelier mas preservando imprevisibilidade direcional.
    - Caudas pesadas e clusters de extremos indicam que o modelo normal clássico subestima risco de forma sistemática, justificando GARCH, saltos ou processos de Lévy.[refs.history-datascience]
    - ML que melhora previsão de volatilidade, mas não de retornos médios, reforça a ideia de Bachelier de que “o jogo é fundamentalmente aleatório”, mas a lei da aleatoriedade pode ser parcialmente aprendida.
  ]

  // Final methodological reflection
  #slide[
    = Reflexão Metodológica

    - Modelo de Bachelier funciona como baseline teórico claro: passeio aleatório normal com variância constante.[refs.bachelier-wiki][refs.bachelier-centenary]
    - Estendê-lo com volatilidade estocástica, saltos e ML para risco mostra a continuidade entre probabilidades clássicas e estatística computacional moderna.
    - [PLACEHOLDER-DISCUSSÃO] Inserir comentários finais baseados nos resultados efetivamente obtidos na sua implementação.
  ]
}
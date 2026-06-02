// main.typ
// CAP 417 Final Work — Louis Bachelier, Generative AI, and Computational Statistics
// Presentation using Touying

#import "@preview/touying:0.3.0": *
#import "theme.typ": *
#import "bachelier_lexicon.typ": *
#import "bachelier_ai_response.typ": *
#import "hf_analysis.typ": *
#import "refs.typ": refs

// Use 16:9 slides and our custom theme
#show: presentation.with(
  theme: cap417-theme,
  aspect-ratio: 16/9,
  // You can tweak font sizes here if needed
)

// Title slide
#title-slide()

// Outline or agenda slide
#slide[
  = Estrutura da Apresentação

  - Parte A — Léxico histórico de Louis Bachelier e agente de IA.
  - Parte B — Resposta hipotética de Bachelier e análise crítica.
  - Parte C — Análise estatística aplicada em dados de alta frequência.
  - Discussão final — Ideias históricas, limitações de IA e benchmarking entre agentes.
]

// Part A slides
#part-a-slides()

// Part B slides
#part-b-slides()

// Part C slides
#part-c-slides()

// Final discussion / takeaway
#slide[
  = Conclusões e Próximos Passos

  - Ideias de Bachelier permanecem centrais em estatística financeira moderna.[refs.bachelier-wiki][refs.bachelier-bio]
  - IA generativa pode emular estilo histórico, mas com anacronismos inevitáveis.
  - Análise empírica com dados HFT: testar o passeio aleatório Gaussiano vs. modelos mais ricos (GARCH, saltos, ML para risco).
  - Próximo passo: preencher placeholders com resultados reais (gráficos, testes, métricas) obtidos via agentes e código.
]

// Optional closing slide
#slide[
  = Fim

  Obrigado pela atenção.
  Perguntas?
]
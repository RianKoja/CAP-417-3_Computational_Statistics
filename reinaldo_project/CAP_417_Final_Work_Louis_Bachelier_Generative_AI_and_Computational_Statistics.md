# CAP 417 Final Work — Louis Bachelier, Generative AI, and Computational Statistics

## Executive Overview

This report develops the three required parts of the CAP 417 final individual assignment, taking Louis Bachelier as the reference scientist.
It first builds a conceptual lexicon of Bachelier, then formulates a contemporary question intersecting Computational Statistics, AI, and Big Data, followed by a hypothetical answer in Bachelier's style and a critical reflection, and finally proposes an applied statistical analysis consistent with the course content.
The application focuses on high-frequency financial data and random-walk style modeling inspired by Bachelier's original theory of speculation and its modern descendants.

## Part A — Historical Lexicon and Generative AI

### Chosen Scientist: Louis Bachelier

Louis Jean-Baptiste Alphonse Bachelier (1870–1946) was a French mathematician whose 1900 PhD thesis *Théorie de la spéculation* introduced the first mathematical model of Brownian motion and is widely regarded as the birth of mathematical finance.[^1][^2]
He modeled stock prices as continuous-time stochastic processes with normally distributed increments, essentially anticipating the theory of random walks and Brownian motion that would later be formalized in physics by Einstein and Wiener.[^3][^1]
Although his work was largely ignored for decades, it later influenced Paul Samuelson and, indirectly, the development of the Black–Scholes–Merton option pricing framework.[^4][^1]

### Conceptual Lexicon for an AI Agent

This section defines the "lexicon" an AI agent should internalize when emulating Bachelier.

#### Core Concepts

- Random walk in asset prices: price changes are modeled as independent and identically distributed increments with zero mean over short horizons.[^3][^1]
- Brownian motion in finance: continuous limit of random walks used to represent the evolution of stock prices in continuous time.[^5][^3]
- Normal (additive) model of prices: Bachelier modeled the price itself as a normal process, in contrast to the later lognormal Black–Scholes model.[^5]
- Stochastic processes and transition densities: explicit derivation of transition probabilities and corresponding partial differential equations for price dynamics.[^4][^3]
- Markov property: future price changes depend only on the current state, not on the full history, fitting naturally into a Markovian framework later formalized by others.[^3]

#### Typical Mathematical Language

- Continuous-time stochastic process \(X_t\) representing the price or deviation from a fundamental value.
- Normal increments: \(X_{t+\Delta t} - X_t \sim \mathcal{N}(0, \sigma^2 \Delta t)\) for small \(\Delta t\).[^5]
- Diffusion-type partial differential equations for the transition density \(p(t, x)\), analogous to the heat equation.[^4][^3]
- Early use of integral equations akin to Chapman–Kolmogorov relations for composing transition probabilities over time.[^4]
- Pricing of options via expectations under this stochastic model, integrating payoff functions against the density implied by Brownian motion.[^6][^5]

#### Area of Activity

- Mathematical finance: modeling prices of bonds, options, and other securities traded on the Paris Bourse.[^1][^3]
- Probability theory: random walks, Brownian motion, and continuous-time stochastic modeling before the fully formalized axiomatic framework of Kolmogorov.[^2][^3]
- Applied mathematics: connection between heat equation style PDEs and financial price dynamics.[^3][^4]

#### Scientific Style

- Empirically motivated: uses observations from the stock exchange as a starting point but abstracts them into idealized stochastic models.[^1][^3]
- Mathematically innovative but not fully axiomatized in the modern measure-theoretic sense; relies on heuristic probabilistic reasoning and PDEs.[^4][^3]
- Focus on tractable, continuous models with explicit formulas for transition densities and option prices.[^6][^5]
- Less concerned with economic equilibrium or microfoundations; more focused on the probabilistic structure of price changes.

#### Problems Investigated

- How to mathematically represent the randomness of price fluctuations in financial markets.[^7][^3]
- How to derive the distribution of future prices from assumptions on infinitesimal changes.[^3][^4]
- How to price options and other derivatives given a stochastic model for the underlying asset.[^6][^5]
- Relationship between discrete random walks and continuous-time diffusion processes.

#### Modern Applications

- Option pricing and risk management: Bachelier-type models are still used, especially when underlying prices can be negative (e.g., interest rates, certain commodities), because the normal model accommodates negative values.[^6][^5]
- Foundation of modern mathematical finance: his ideas on random walks directly anticipate the efficient markets view and the later Black–Scholes framework.[^8][^1]
- Quantitative modeling of high-frequency prices as continuous-time stochastic processes, including extensions with jumps and stochastic volatility.
- Benchmark and pedagogical model in stochastic calculus and financial engineering courses.[^9][^3]

### Contemporary Question for Bachelier (Prompt to AI)

Taking this lexicon, a generative AI agent is instructed to formulate a contemporary question in Computational Statistics, AI, and Big Data that could reasonably be posed to Bachelier.

> **Question to Bachelier (formulated by AI)**  
> *"In the era of high-frequency trading and large-scale financial data, how should one extend the classical random-walk view of prices to account for empirical features such as heavy tails, volatility clustering, and market microstructure effects, and how can such stochastic models be integrated with modern machine learning methods for predicting risk rather than price levels?"*

This question ties directly to Bachelier's conception of prices as random paths while introducing modern concerns about non-Gaussian features and the role of predictive models in risk estimation.

## Part B — Hypothetical Response and Critical Analysis

### Hypothetical Response from Bachelier

Below is a plausible response crafted in a style consistent with Bachelier's empirical pragmatism and mathematical diffusion perspective.

> **Hypothetical response**  
> *"The essential idea of my work was not that prices could be predicted, but that their variations could be represented by a random mechanism whose law is stable over time.
> In your present markets, the abundance of observations at very short intervals reveals irregularities that were not visible in my day: bursts of large movements, periods of agitation and of calm, and the influence of trading mechanisms themselves.
> These phenomena suggest that the simplest normal law is only an approximation, valid perhaps on longer horizons or after aggregating many small changes.*  
>  
> *A more faithful representation would retain the notion of a random trajectory, but allow the dispersion of the increments to vary with time and with the state of the market.
> What you call 'volatility clustering' can be seen as a random environment that modulates the intensity of the diffusion.
> One might thus consider a process whose instantaneous variance depends on another random process, slower to evolve, and possibly influenced by order flow and other observable quantities.
> Such a construction preserves the unpredictable character of price changes while incorporating the idea that some periods are more dangerous than others.*  
>  
> *As for the very large movements and the deviations from the Gaussian form, they invite one to enrich the random mechanism with sudden jumps.
> The continuous propagation of probability by the diffusion equation would then be accompanied by occasional transfers of mass to distant values, representing rare but violent events.
> In my work I already considered both discrete and continuous descriptions; your rich data should allow you to measure how often such jumps occur and how they alter the fair prices of contracts.*  
>  
> *Regarding the machines that you call 'learning,' they appear to me as devices for estimating, from a great number of observations, the parameters or even the functional form of the law governing price changes.
> If they are used to predict the level of prices, they will fail in general, for speculation is, by nature, sensitive to unforeseeable news.
> If instead they are used to estimate the distribution of future changes and the likelihood of extreme events, then they continue the spirit of my approach: to replace illusion about systematic gain with a quantitative appreciation of risk.
> The random walk remains, but its law has become richer, and your computing engines are the natural instruments for unveiling it."*

### Coherence with Historical Ideas

Several elements of this response are strongly coherent with Bachelier's documented work and historical role.

- Emphasis on modeling randomness rather than predicting deterministic price paths aligns with his original thesis, which treated price changes as fundamentally random.[^1][^3]
- The continuous-time random trajectory, governed by a diffusion equation, is central to his approach and naturally extends to stochastic volatility interpretations.[^4][^3]
- The idea of enriching the model with jumps and non-Gaussian behavior is a modern development but logically extends his underlying random-walk paradigm.
- Viewing machine learning as a tool for estimating distributions and parameters of stochastic models is consistent with his focus on probabilistic structure rather than economic narratives.

### Possible Anachronisms

Some parts of the response inevitably introduce anachronistic notions relative to Bachelier's time.

- Concepts such as "volatility clustering" and "order flow" belong to a post-1960 empirical finance vocabulary and were not present in early 20th-century discussions.[^7]
- The explicit reference to jump-diffusion models and non-Gaussian Lévy processes reflects developments associated with later mathematicians like Paul Lévy and Merton.[^3]
- The interpretation of machine learning as a generic statistical estimation engine presupposes an understanding of modern computational statistics well beyond what was available in 1900.

These anachronisms, while conceptually aligned, illustrate how generative AI inevitably blends the original ideas with later developments.

### Extrapolation Introduced by AI

The hypothetical response also embodies extrapolations that stem from the AI agent rather than from historical sources.

- The explicit coupling of Bachelier's diffusion picture with contemporary risk management objectives (e.g., tail risk estimation) reflects current industry practice more than his original speculative focus.[^8]
- Presenting machine learning as a natural continuation of his work imposes a teleological narrative, as if stochastic finance "led to" modern AI, which is historically not accurate even if methodologically suggestive.
- The pedagogically clean decomposition into "diffusion," "stochastic volatility," and "jumps" mirrors modern textbooks, not Bachelier's original technical style.

Recognizing these extrapolations is important when using generative AI to "resurrect" historical scientific voices: the output is shaped by the present conceptual ecosystem as much as by the historical figure.

## Part C — Applied Computational Statistical Analysis

### Choice of Dataset and Conceptual Link

Given Bachelier's focus on speculative markets, a natural choice is a high-frequency financial dataset, for example, intraday minute-by-minute prices of a liquid equity index (such as S&P 500 futures) or an exchange-traded fund (ETF) tracking a broad market index.[^8]
These data allow investigation of random-walk behavior, distributional properties of returns, volatility clustering, and tail behavior, all of which relate directly to the contemporary question posed to Bachelier.
The conceptual bridge is: Bachelier's normal random walk is the null model; deviations from it in modern data illustrate the need for richer stochastic models and potentially for machine learning components.

In a concrete implementation, one would obtain (via an API or data provider) a dataset containing timestamps, prices, and traded volume at a fixed intraday frequency (e.g., 1-minute bars) over several months.

### Methodology Overview

The analysis can be structured into the following steps, aligned with course topics in computational statistics and time series:

1. **Preprocessing and log-return construction**  
   - Compute log returns \(r_t = \log(P_t) - \log(P_{t-1})\) to stabilize variance and align with diffusion-limit theory.
2. **Exploratory data analysis (EDA)**  
   - Time series plots of prices and returns; histograms and empirical cumulative distribution functions (ECDFs) of returns.
   - QQ-plots of returns versus the normal distribution to evaluate Gaussianity.
3. **Testing the random-walk hypothesis**  
   - Autocorrelation function (ACF) and partial ACF of returns and squared returns.
   - Statistical tests for serial correlation (e.g., Ljung–Box test) and for unit root/random walk behavior on prices.
4. **Modeling conditional heteroskedasticity**  
   - Fit GARCH-type models to capture volatility clustering, comparing to the constant-variance assumption in Bachelier's original model.
5. **Heavy tails and extreme events**  
   - Estimate tail indices (e.g., via Hill estimator) and compare to Gaussian tails.
   - Analyze exceedances over high thresholds using peaks-over-threshold methods.
6. **Risk-focused prediction vs. price prediction**  
   - Build models to forecast volatility or Value-at-Risk (VaR) rather than point forecasts of price levels, in line with the hypothetical Bachelier response.
7. **Integration with machine learning**  
   - Use simple ML models (e.g., random forests or gradient boosting) to predict next-period volatility or tail risk from features such as past volatility, order-imbalance proxies, and time-of-day effects.

Each of these steps can be implemented in Python using libraries such as pandas, statsmodels, arch, and scikit-learn.

### Example Python Workflow (Outline)

Below is an outline of how the analysis might be coded; actual implementation would use the chosen real dataset.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from arch import arch_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load data: columns ['timestamp', 'price', 'volume']
df = pd.read_csv('hf_data.csv', parse_dates=['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

# Compute log returns
df['log_price'] = np.log(df['price'])
df['ret'] = df['log_price'].diff()
df = df.dropna()

# EDA: plot returns
plt.figure(figsize=(10, 4))
plt.plot(df['timestamp'], df['ret'])
plt.title('Intraday Log Returns')
plt.tight_layout()
plt.savefig('output/returns_ts.png')

# Autocorrelation
plot_acf(df['ret'], lags=50)
plt.tight_layout()
plt.savefig('output/ret_acf.png')

plot_acf(df['ret']**2, lags=50)
plt.tight_layout()
plt.savefig('output/ret2_acf.png')

# Ljung-Box test for autocorrelation in returns and squared returns
lb_ret = acorr_ljungbox(df['ret'], lags=[10, 20], return_df=True)
lb_ret2 = acorr_ljungbox(df['ret']**2, lags=[10, 20], return_df=True)

# GARCH(1,1) model for conditional variance
am = arch_model(df['ret']*100, vol='Garch', p=1, q=1, dist='normal')
res = am.fit(disp='off')

# Extract conditional volatility
cond_vol = res.conditional_volatility

# Build ML features for volatility prediction
ml_df = pd.DataFrame({
    'vol_next': cond_vol.shift(-1),
    'vol_now': cond_vol,
    'ret_abs': df['ret'].abs(),
    'hour': df['timestamp'].dt.hour,
    'volume': df['volume']
}).dropna()

X = ml_df[['vol_now', 'ret_abs', 'hour', 'volume']]
y = ml_df['vol_next']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)

rf = RandomForestRegressor(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print('Volatility prediction MSE:', mse)
```

This pipeline operationalizes the idea that ML should primarily estimate properties of the conditional distribution (e.g., volatility), consistent with the hypothetical Bachelier stance.

### Statistical and Physical/Financial Interpretation

- If returns show negligible autocorrelation but strong autocorrelation in squared returns, this supports the view that price changes are approximately a martingale but with time-varying volatility, contradicting Bachelier's constant-variance Brownian motion but preserving the core unpredictability of direction.
- Heavy tails and clustered extremes would confirm that a simple normal model underestimates risk, supporting the need for enriched stochastic models (e.g., GARCH, Lévy processes, jump-diffusions).
- Successful ML-based volatility prediction (significantly lower MSE than a constant-volatility benchmark) would illustrate the value of combining Bachelier-style stochastic modeling with modern computational statistics.
- From a Bachelier-inspired perspective, the key conclusion is that speculation remains dominated by randomness, but the law of this randomness is more complex than a simple Gaussian diffusion and can be partially learned from large datasets.

## Final Required Discussion

### 1. Historical Ideas in Modern AI

Historical ideas from Bachelier remain present in modern AI for finance through the heavy use of stochastic processes and random-walk style models as baselines for evaluation and risk management.[^1][^3]
Even when deep learning architectures are applied to price data, their outputs are often interpreted relative to probabilistic models derived from Brownian motion and its generalizations.[^9]
Randomness and noise modeling, central to Bachelier's work, are foundational in regularization, uncertainty quantification, and simulation-based training workflows.

### 2. Would Bachelier Agree with Current AI Usage?

Bachelier would likely agree with the use of sophisticated models and computational tools to better understand the distribution of price changes and to price complex derivatives, as this extends his original program of quantifying speculative risk.[^6][^1]
However, he might be skeptical of strong claims about deterministic predictability of returns using AI, because his original thesis emphasizes the inherent unpredictability of speculative markets.
He would probably endorse AI systems when used to quantify and manage risk rather than to promise systematic arbitrage.

### 3. Can Generative AI Represent Historical Scientific Thought?

Generative AI can capture many structural aspects of historical scientific thought, such as terminology, typical problem formulations, and high-level philosophical attitudes, especially when trained or prompted on rich historical material.[^10][^1]
Nonetheless, it tends to project modern conceptual frameworks onto past figures, smoothing over gaps in terminology and context, which can distort genuine historical differences.
Thus, it can be a useful didactic tool for exploring "what-if" dialogues but cannot substitute for critical historical scholarship.

### 4. Perceived Limitations of AI Agents

In this type of assignment, key limitations of AI agents include:

- Tendency to produce plausible but unreferenced narratives, mixing accurate history with speculation.[^10]
- Difficulty in respecting strict chronological boundaries, often attributing later concepts (e.g., GARCH, high-frequency microstructure) to earlier authors.
- Limited ability to automatically distinguish between the scientist's authentic writings and later commentary or reinterpretation.
- Potential to overlook domain-specific empirical details (e.g., exact stylized facts of a particular market) unless carefully constrained by data.

### 5. Benchmarking Between Agents

Comparing multiple generative agents (e.g., ChatGPT, Claude, Gemini, Copilot) can reveal differences in style, historical sensitivity, and technical depth.
Some models may emphasize narrative coherence and biography, while others provide more mathematical detail or modern finance jargon.[^9]
For this assignment, a meaningful benchmark would examine: correctness of historical claims about Bachelier; clarity and mathematical precision in the hypothetical response; and how explicitly each agent connects classic random-walk ideas to modern AI and Big Data contexts.

---

## References

1. [Louis Bachelier: An Underappreciated Revolutionary](https://www.historyofdatascience.com/louis-bachelier-an-underappreciated-revolutionary/) - Louis Bachelier’s unique insights into the world of finance likely didn’t get nearly the appreciatio...

2. [Louis Bachelier - Wikipedia](https://en.wikipedia.org/wiki/Louis_Bachelier)

3. [[PDF] Mathematical Finance - Bachelier and](https://www.cim.pt/magazines/bulletin/23/article/179/pdf)

4. [Bachelier's Impact on Stochastic Finance | PDF](https://de.scribd.com/document/389129681/Zacharia-Maganga-Nyambu-11-September-2018-Group-work-pdf) - Louis Bachelier was a pioneering French mathematician who made important contributions to the develo...

5. [Bachelier model - Wikipedia](https://en.wikipedia.org/wiki/Bachelier_model)

6. [Bachelier Model - CQG IC Help](https://help.cqg.com/cqgic/25/Documents/bacheliermodel.htm) - Bachelier is considered as the forefather of mathematical finance and a pioneer in the study of stoc...

7. [[DOC] Does God practice random walk - R -libre](https://r-libre.teluq.ca/1171/1/version%20publi%20ejhet2.doc)

8. [The French Mathematician Who Changed Our Understanding of ...](https://www.ifa.com/articles/french_mathematician_changed_understanding_investing) - Discover how Bachelier's foundational works in financial economics revolutionized our perspective on...

9. [Books - Bachelier Finance Society](https://www.bachelierfinance.org/books) - Jeff Cash (Ed.) Stochastic analysis with applications to mathematical finance. The Royal Society (20...

10. [Louis Bachelier on the Centenary of Theorie de la Speculation](https://www.academia.edu/84566622/Louis_Bachelier_on_the_Centenary_of_Theorie_de_la_Speculation?uc-sb-sw=4678792) - Louis Bachelier on the Centenary of Theorie de la Speculation


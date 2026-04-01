# The Model Confidence Set

**Peter R. Hansen**$^{a\dagger}$, **Asger Lunde**$^b$, and **James M. Nason**$^c$

$^a$ Stanford University, Department of Economics, 579 Serra Mall, Stanford, CA 94305-6072, USA & CREATES  
$^b$ Aarhus University, School of Economics and Management, Bartholins Allé 10, Aarhus, Denmark & CREATES  
$^c$ Federal Reserve Bank of Philadelphia, Ten Independence Mall, Philadelphia, PA 19106-1574, USA  

*March 2010*

---

## Abstract

The paper introduces the model confidence set (MCS) and applies it to the selection of models. A MCS is a set of models that is constructed such that it will contain the best model with a given level of confidence. The MCS is in this sense analogous to a confidence interval for a parameter. The MCS acknowledges the limitations of the data, such that uninformative data yields a MCS with many models, whereas informative data yields a MCS with only a few models. The MCS procedure does not assume that a particular model is the true model; in fact the MCS procedure can be used to compare more general objects, beyond the comparison of models. We apply the MCS procedure to two empirical problems. First, we revisit the inflation forecasting problem posed by Stock and Watson (1999), and compute the MCS for their set of inflation forecasts. Second, we compare a number of Taylor rule regressions and determine the MCS of the best in terms of in-sample likelihood criteria.

**JEL Classification:** C12, C19, C44, C52, and C53.  
**Keywords:** Model Confidence Set, Model Selection, Forecasting, Multiple Comparisons.

---

## 1 Introduction

Econometricians often face a situation where several models or methods are available for a particular empirical problem. A relevant question is: Which is the best? This question is onerous for most data to answer, especially when the set of competing alternatives is large. Many applications will not yield a single model that significantly dominates all competitors because the data is not sufficiently informative to give an unequivocal answer to this question. Nonetheless, it is possible to reduce the set of models to a smaller set of models — a model confidence set — that contains the best model with a given level of confidence.

The objective of the model confidence set (MCS) procedure is to determine the set of models, $\mathcal{M}^*$, that consists of the best model(s) from a collection of models, $\mathcal{M}_0$, where "best" is defined in terms of a criterion that is user-specified. The MCS procedure yields a model confidence set, $\hat{\mathcal{M}}^*$, that is a collection of models built to contain the best models with a given level of confidence. The process of winnowing models out of $\mathcal{M}_0$ relies on sample information about the relative performances of the models in $\mathcal{M}_0$. This sample information drives the MCS to create a random data-dependent set of models, $\hat{\mathcal{M}}^*$. The set $\hat{\mathcal{M}}^*$ includes the best model(s) with a certain probability in the same sense that a confidence interval covers a population parameter.

An attractive feature of the MCS approach is that it acknowledges the limitations of the data. Informative data will result in a MCS that contains only the best model. Less informative data makes it difficult to distinguish between models and may result in a MCS that contains several (or possibly all) models. Thus, the MCS differs from extant model selection criteria that choose a single model without regard to the information content of the data. Another advantage is that the MCS procedure makes it possible to make statements about significance that are valid in the traditional sense — a property that is not satisfied by the commonly used approach of reporting p-values from multiple pairwise comparisons. Another attractive feature of the MCS procedure is that it allows for the possibility that more than one model can be the best, in which case $\mathcal{M}^*$ contains more than a single model.

The contributions of this paper can be summarized as follows:

1. We introduce a model confidence set procedure and establish its theoretical properties.
2. We propose a practical bootstrap implementation of the MCS procedure for a set of problems that includes comparisons of forecasting models evaluated out-of-sample and regression models evaluated in-sample.
3. The finite sample properties of the bootstrap MCS procedure are analyzed in simulation studies.
4. We apply the MCS procedure to two empirical applications: we revisit the out-of-sample prediction problem of Stock and Watson (1999) and construct MCSs for their inflation forecasts; we also build a MCS for Taylor rule regressions using three likelihood criteria that include the AIC and BIC.

### 1.1 Theory of Model Confidence Sets

We do not treat models as sacred objects, nor do we assume that a particular model represents the true data generating process. Models are evaluated in terms of a user-specified criterion function. Consequently, the "best" model is unlikely to be replicated for all criteria. Also, we use the term "models" loosely. It can refer to econometric models, competing forecasts, or alternatives that need not involve any modelling of data, such as trading rules. So the MCS procedure is not specific to comparisons of models. For example, one could construct a MCS for a set of different "treatments" by comparing sample estimates of the corresponding treatment effects, or a MCS for trading rules with the best Sharpe ratio.

A MCS is constructed from a collection of competing objects, $\mathcal{M}_0$, and a criterion for evaluating these objects empirically. The MCS procedure is based on an equivalence test, $\delta_\mathcal{M}$, and an elimination rule, $e_\mathcal{M}$. The equivalence test is applied to the set $\mathcal{M} = \mathcal{M}_0$. If $\delta_\mathcal{M}$ is rejected, there is evidence that the objects in $\mathcal{M}$ are not equally "good" and $e_\mathcal{M}$ is used to eliminate an object with poor sample performance from $\mathcal{M}$. This procedure is repeated until $\delta_\mathcal{M}$ is "accepted", and the MCS is now defined by the set of "surviving" objects. By using the same significance level, $\alpha$, in all tests, the procedure guarantees that

$$\liminf_{n \to \infty} P\!\left(\mathcal{M}^* \subset \hat{\mathcal{M}}^*_{1-\alpha}\right) \geq 1 - \alpha,$$

and in the case where $\mathcal{M}^*$ consists of one object we have the stronger result that

$$\lim_{n \to \infty} P\!\left(\mathcal{M}^* = \hat{\mathcal{M}}^*_{1-\alpha}\right) = 1.$$

The MCS procedure also yields p-values for each of the objects. For a given object, $i \in \mathcal{M}_0$, the MCS p-value, $\hat{p}_i$, is the threshold at which $i \in \hat{\mathcal{M}}^*_{1-\alpha}$ if and only if $\hat{p}_i \geq \alpha$. Thus, an object with a small MCS p-value makes it unlikely that it is one of the "best" alternatives in $\mathcal{M}_0$.

### 1.2 Bootstrap Implementation and Simulation Results

We propose a bootstrap implementation of the MCS procedure that is convenient when the number of models is large. The bootstrap implementation is simple to use in practice and avoids the need to estimate a high-dimensional covariance matrix. White (2000b) is the source of many of the ideas that underlie our bootstrap implementation.

We study the properties of our bootstrap implementation of the MCS procedure through simulation experiments. The results are very encouraging as the best model does end up in the MCS at the appropriate frequency, and the MCS procedure does have power to weed out all the poor models when the data contains sufficient information.

### 1.3 Empirical Analysis of Inflation Forecasts and Taylor Rules

We apply the MCS to two empirical problems. First, the MCS is used to study the inflation forecasting problem. The choice of an inflation forecasting model is an especially important issue for central banks, treasuries, and private sector agents. The fifty-plus-year tradition of the Phillips curve suggests it remains an effective vehicle for the task of inflation forecasting. Stock and Watson (1999) make the case that "a reasonably specified Phillips curve is the best tool for forecasting inflation"; also see Gordon (1997), Staiger, Stock, and Watson (1997b), and Stock and Watson (2003). Atkeson and Ohanian (2001) conclude that this is not the case because they find it is difficult for any of the Phillips curves they study to beat a simple no-change forecast in out-of-sample point prediction.

Our first empirical application is based on the Stock and Watson (1999) data set. We partition the evaluation period into the same two subsamples as Stock and Watson (1999). The earlier subsample covers a period with persistent and volatile inflation — this sample is expected to be relatively informative about which models might be the best forecasting models. Indeed, the MCS consists of relatively few models. The later subsample is a period in which inflation is relatively smooth and exhibits little volatility. This yields a sample that contains relatively little information about which of the models deliver the best forecasts. Nonetheless, the no-change (month) forecast of Stock and Watson (1999) never ends up in the MCS. The no-change (year) forecast of Atkeson and Ohanian (2001) has the smallest mean square prediction error (MSPE) in the second subsample. This enables us to reconcile Stock and Watson (1999) with Atkeson and Ohanian (2001) by showing their different definitions of the benchmark forecast explain the different conclusions they reach.

Our second empirical example applies the MCS to choosing from a set of competing nominal interest rate rule regressions on a quarterly U.S. sample running from 1979 through 2006. These regressions fall into the class of interest rate rules promoted by Taylor (1993). The MCS procedure begins with 25 regression models, including a pure AR(1) of the federal funds rate. The remaining 24 models are Taylor rule regressions containing different combinations of lagged inflation and lags of various definitions of real economic activity (output gap, unemployment rate gap, or real marginal cost), and in some cases the lagged federal funds rate.

### 1.4 Outline of Paper

The paper is organized as follows. We present the theoretical framework of the MCS in Section 2. Section 3 outlines practical bootstrap methods to implement the MCS. Multiple model comparison methods related to the MCS are discussed in Section 4. Section 5 reports the results of simulation experiments. The MCS is applied to two empirical examples in Section 6. Section 7 concludes.

---

## 2 General Theory for Model Confidence Set

In this section, we discuss the theory of model confidence sets for a general set of alternatives. Our leading example concerns the comparison of empirical models, such as forecasting models. Nevertheless, we do not make specific references to "models" in the first part of this section, in which we lay out the general theory.

We consider a set, $\mathcal{M}_0$, that contains a finite number of objects indexed by $i = 1, \ldots, m_0$. The objects are evaluated in terms of a loss function and we denote the loss associated with object $i$ in period $t$ as $L_{i,t}$, $t = 1, \ldots, n$. For example, in the situation where a point forecast, $\hat{Y}_{i,t}$, of $Y_t$ is evaluated in terms of a loss function, $L$, we define

$$L_{i,t} = L\!\left(Y_t,\, \hat{Y}_{i,t}\right).$$

Define the **relative performance variables**

$$d_{ij,t} \equiv L_{i,t} - L_{j,t}, \qquad \text{for all } i, j \in \mathcal{M}_0.$$

This paper assumes that $\mu_{ij} \equiv \mathbb{E}(d_{ij,t})$ is finite and does not depend on $t$, for all $i, j \in \mathcal{M}_0$. We rank alternatives in terms of expected loss, so that alternative $i$ is preferred to alternative $j$ if $\mu_{ij} < 0$.

> **Definition 1.** The set of superior objects is defined by
> $$\mathcal{M}^* \equiv \left\{i \in \mathcal{M}_0 : \mu_{ij} \leq 0 \text{ for all } j \in \mathcal{M}_0\right\}.$$

The objective of the MCS procedure is to determine $\mathcal{M}^*$. This is done through a sequence of significance tests, where objects that are found to be significantly inferior to other elements of $\mathcal{M}_0$ are eliminated. The hypotheses that are being tested take the form:

$$H_{0,\mathcal{M}} : \mu_{ij} = 0 \quad \text{for all } i, j \in \mathcal{M}, \tag{1}$$

where $\mathcal{M} \subset \mathcal{M}_0$. We denote the alternative hypothesis, $\mu_{ij} \neq 0$ for some $i, j \in \mathcal{M}$, by $H_{A,\mathcal{M}}$. Note that $H_{0,\mathcal{M}^*}$ is true given our definition of $\mathcal{M}^*$, whereas $H_{0,\mathcal{M}}$ is false if $\mathcal{M}$ contains elements from $\mathcal{M}^*$ and its complement, $\mathcal{M}_0 \setminus \mathcal{M}^*$.

We define a model confidence set to be any subset of $\mathcal{M}_0$ that contains all of $\mathcal{M}^*$ with a given probability (its coverage probability). The challenge is to design a procedure that produces a set with the proper coverage probability.

### 2.1 The MCS Algorithm and Its Properties

As stated in the introduction, the MCS procedure is based on an equivalence test, $\delta_\mathcal{M}$, and an elimination rule, $e_\mathcal{M}$. The equivalence test, $\delta_\mathcal{M}$, is used to test the hypothesis $H_{0,\mathcal{M}}$ for any $\mathcal{M} \subset \mathcal{M}_0$, and $e_\mathcal{M}$ identifies the object of $\mathcal{M}$ that is to be removed from $\mathcal{M}$ in the event that $H_{0,\mathcal{M}}$ is rejected. As a convention, we let $\delta_\mathcal{M} = 0$ and $\delta_\mathcal{M} = 1$ correspond to the cases where $H_{0,\mathcal{M}}$ is "accepted" and "rejected" respectively.

> **Definition 2 (MCS Algorithm).**  
> - **Step 0:** Initially set $\mathcal{M} = \mathcal{M}_0$.  
> - **Step 1:** Test $H_{0,\mathcal{M}}$ using $\delta_\mathcal{M}$ at level $\alpha$.  
> - **Step 2:** If $H_{0,\mathcal{M}}$ is "accepted", define $\hat{\mathcal{M}}^*_{1-\alpha} = \mathcal{M}$; otherwise use $e_\mathcal{M}$ to eliminate an object from $\mathcal{M}$ and repeat from Step 1.

The set $\hat{\mathcal{M}}^*_{1-\alpha}$, which consists of the "surviving" objects, is referred to as the **model confidence set**. Theorem 1 shows that the term "confidence set" is appropriate in this context, provided that the equivalence test and the elimination rule satisfy the following assumption.

> **Assumption 1.** For any $\mathcal{M} \subset \mathcal{M}_0$ we assume the following about $(\delta_\mathcal{M}, e_\mathcal{M})$:  
> (a) $\limsup_{n \to \infty} P(\delta_\mathcal{M} = 1 \mid H_{0,\mathcal{M}}) \leq \alpha$;  
> (b) $\lim_{n \to \infty} P(\delta_\mathcal{M} = 1 \mid H_{A,\mathcal{M}}) = 1$;  
> (c) $\lim_{n \to \infty} P(e_\mathcal{M} \in \mathcal{M}^* \mid H_{A,\mathcal{M}}) = 0$.

Condition (a) requires the asymptotic level not to exceed $\alpha$; (b) requires the asymptotic power to be one; and (c) requires that a superior object $i^* \in \mathcal{M}^*$ is not eliminated (as $n \to \infty$) as long as there are inferior models in $\mathcal{M}$.

> **Theorem 1 (Properties of MCS).** Given Assumption 1, it holds that:  
> (i) $\liminf_{n \to \infty} P\!\left(\mathcal{M}^* \subset \hat{\mathcal{M}}^*_{1-\alpha}\right) \geq 1 - \alpha$;  
> (ii) $\lim_{n \to \infty} P\!\left(i \in \hat{\mathcal{M}}^*_{1-\alpha}\right) = 0$ for all $i \notin \mathcal{M}^*$.

*Proof.* Let $i^* \in \mathcal{M}^*$. To prove (i), we consider the event that $i^*$ is eliminated from $\mathcal{M}$. From Assumption 1(c) it follows that $P(\delta_\mathcal{M} = 1,\, e_\mathcal{M} = i^* \mid H_{A,\mathcal{M}}) \leq P(e_\mathcal{M} = i^* \mid H_{A,\mathcal{M}}) \to 0$ as $n \to \infty$. So the probability that a good model is eliminated when $\mathcal{M}$ contains poor models vanishes as $n \to \infty$. Next, Assumption 1(a) shows that

$$\limsup_{n \to \infty} P(\delta_\mathcal{M} = 1,\, e_\mathcal{M} = i^* \mid H_{0,\mathcal{M}}) = \limsup_{n \to \infty} P(\delta_\mathcal{M} = 1 \mid H_{0,\mathcal{M}}) \leq \alpha,$$

such that the probability that $i^*$ is eliminated when all models in $\mathcal{M}$ are good models is asymptotically bounded by $\alpha$. To prove (ii), we first note that $\lim_{n \to \infty} P(e_\mathcal{M} = i^* \mid H_{A,\mathcal{M}}) = 0$ such that only poor models will be eliminated (asymptotically) as long as $\mathcal{M} \not\subseteq \mathcal{M}^*$. On the other hand, Assumption 1(b) ensures that models will be eliminated as long as the null hypothesis is false. $\square$

The asymptotic familywise error rate (FWE) — the probability of making one or more false rejections — is bounded by the level used in all tests. Sequential testing is key for building a MCS, and the MCS procedure does not accumulate Type I errors because the sequential testing is halted when the first hypothesis is "accepted" (cf. Leeb and Pötscher, 2003).

When there is only a single model in $\mathcal{M}^*$, we obtain a stronger result.

> **Corollary 1.** Suppose that Assumption 1 holds and that $\mathcal{M}^*$ is a singleton. Then
> $$\lim_{n \to \infty} P\!\left(\mathcal{M}^* = \hat{\mathcal{M}}^*_{1-\alpha}\right) = 1.$$

*Proof.* When $\mathcal{M}^* = \{i^*\}$, it follows from Theorem 1 that $i^*$ will be the last surviving element with probability approaching one as $n \to \infty$. The result follows because the last surviving element is never eliminated. $\square$

### 2.2 Coherency between Test and Elimination Rule

The previous asymptotic results do not rely on any direct connection between the hypothesis test, $\delta_\mathcal{M}$, and the elimination rule, $e_\mathcal{M}$. Nonetheless, when the MCS is implemented in finite samples, there is an advantage to having them be **coherent**. The next theorem establishes a finite-sample version of Theorem 1(i).

> **Theorem 2.** Suppose that $P(\delta_\mathcal{M} = 1,\, e_\mathcal{M} \in \mathcal{M}^*) \leq \alpha$. Then
> $$P\!\left(\mathcal{M}^* \subset \hat{\mathcal{M}}^*_{1-\alpha}\right) \geq 1 - \alpha.$$

*Proof.* We only need to consider the first instance that $e_\mathcal{M} \in \mathcal{M}^*$, because all preceding tests will not eliminate elements in $\mathcal{M}^*$. Regardless of whether the null is true or false, $P(\delta_\mathcal{M} = 1,\, e_\mathcal{M} \in \mathcal{M}^*) \leq \alpha$, so $\alpha$ bounds the probability that an element from $\mathcal{M}^*$ is eliminated. Additional elements from $\mathcal{M}^*$ may be eliminated in subsequent tests, but these tests will only be undertaken if all preceding tests are rejected. Thus $P(\mathcal{M}^* \subset \hat{\mathcal{M}}^*_{1-\alpha}) \geq 1 - \alpha$. $\square$

In practice, hypothesis tests often rely on asymptotic results that cannot guarantee $P(\delta_\mathcal{M} = 1, e_\mathcal{M} \in \mathcal{M}^*) \leq \alpha$ in finite samples. We provide a definition of coherency for this setting. In what follows, we use $P_0$ to denote the probability measure that arises by imposing the null hypothesis via the transformation $d_{ij,t} \mapsto d_{ij,t} - \mu_{ij}$.

> **Definition 3.** There is said to be **coherency** between test and elimination rule when
> $$P(\delta_\mathcal{M} = 1,\, e_\mathcal{M} \in \mathcal{M}^*) \leq P_0(\delta_\mathcal{M} = 1).$$

Coherency in conjunction with asymptotic control of the Type I error, $\limsup_{n \to \infty} P_0(\delta_\mathcal{M} = 1) \leq \alpha$, translates into an asymptotic version of the condition in Theorem 2. Coherency prevents adopting the most powerful test of $H_{0,\mathcal{M}}$ in some situations, because tests do not necessarily identify a single element as the cause for rejection.[^1]

[^1]: A good analogy is found in the standard regression model, where an $F$-test may reject the joint hypothesis that all regression coefficients are zero, even though all $t$-statistics are insignificant. Another analogy is that it is easier to conclude that a murder has taken place than to determine who committed it.

### 2.3 MCS p-Values

The elimination rule, $e_\mathcal{M}$, defines a sequence of (random) sets,

$$\mathcal{M}_0 = \mathcal{M}_1 \supset \mathcal{M}_2 \supset \cdots \supset \mathcal{M}_{m_0},$$

where $\mathcal{M}_i = \{e_{\mathcal{M}_i}, \ldots, e_{\mathcal{M}_{m_0}}\}$ and $m_0$ is the number of elements in $\mathcal{M}_0$. So $e_{\mathcal{M}_0} = e_{\mathcal{M}_1}$ is the first element to be eliminated, $e_{\mathcal{M}_2}$ is the second, etc.

> **Definition 4 (MCS p-values).** Let $P_{H_{0,\mathcal{M}_i}}$ denote the p-value associated with the null hypothesis $H_{0,\mathcal{M}_i}$, with the convention that $P_{H_{0,\mathcal{M}_{m_0}}} \equiv 1$. The **MCS p-value** for model $e_{\mathcal{M}_j} \in \mathcal{M}_0$ is defined by
> $$\hat{p}_{e_{\mathcal{M}_j}} \equiv \max_{i \leq j}\, P_{H_{0,\mathcal{M}_i}}.$$

Since $\mathcal{M}_{m_0}$ consists of a single model, the null hypothesis $H_{0,\mathcal{M}_{m_0}}$ simply states that the last surviving model is as good as itself, making the convention $P_{H_{0,\mathcal{M}_{m_0}}} \equiv 1$ logical.

**Table 1: Computation of MCS p-values**

| Elimination Rule | p-value for $H_{0,\mathcal{M}_k}$ | MCS p-value |
|:---|:---|:---|
| $e_{\mathcal{M}_1}$ | $P_{H_{0,\mathcal{M}_1}} = 0.01$ | $\hat{p}_{e_{\mathcal{M}_1}} = 0.01$ |
| $e_{\mathcal{M}_2}$ | $P_{H_{0,\mathcal{M}_2}} = 0.04$ | $\hat{p}_{e_{\mathcal{M}_2}} = 0.04$ |
| $e_{\mathcal{M}_3}$ | $P_{H_{0,\mathcal{M}_3}} = 0.02$ | $\hat{p}_{e_{\mathcal{M}_3}} = 0.04$ |
| $e_{\mathcal{M}_4}$ | $P_{H_{0,\mathcal{M}_4}} = 0.03$ | $\hat{p}_{e_{\mathcal{M}_4}} = 0.04$ |
| $e_{\mathcal{M}_5}$ | $P_{H_{0,\mathcal{M}_5}} = 0.07$ | $\hat{p}_{e_{\mathcal{M}_5}} = 0.07$ |
| $e_{\mathcal{M}_6}$ | $P_{H_{0,\mathcal{M}_6}} = 0.04$ | $\hat{p}_{e_{\mathcal{M}_6}} = 0.07$ |
| $e_{\mathcal{M}_7}$ | $P_{H_{0,\mathcal{M}_7}} = 0.11$ | $\hat{p}_{e_{\mathcal{M}_7}} = 0.11$ |
| $e_{\mathcal{M}_8}$ | $P_{H_{0,\mathcal{M}_8}} = 0.25$ | $\hat{p}_{e_{\mathcal{M}_8}} = 0.25$ |
| $\vdots$ | $\vdots$ | $\vdots$ |
| $e_{\mathcal{M}_{m_0}}$ | $P_{H_{0,\mathcal{M}_{m_0}}} \equiv 1.00$ | $\hat{p}_{e_{\mathcal{M}_{m_0}}} = 1.00$ |

*The table illustrates the computation of MCS p-values. Note that MCS p-values for some models do not coincide with the p-values for the corresponding null hypotheses. For example, the MCS p-value for $e_{\mathcal{M}_3}$ (the third model to be eliminated) exceeds the p-value for $H_{0,\mathcal{M}_3}$ because the p-value associated with $H_{0,\mathcal{M}_2}$ — a null hypothesis tested prior to $H_{0,\mathcal{M}_3}$ — is larger.*

> **Theorem 3.** Let the elements of $\mathcal{M}_0$ be indexed by $i = 1, \ldots, m_0$. The MCS p-value $\hat{p}_i$ is such that
> $$i \in \hat{\mathcal{M}}^*_{1-\alpha} \iff \hat{p}_i \geq \alpha, \qquad \text{for any } i \in \mathcal{M}_0.$$

*Proof.* Suppose $\hat{p}_i < \alpha$ and determine the $k$ for which $i = e_{\mathcal{M}_k}$. Since $\hat{p}_i = \hat{p}_{e_{\mathcal{M}_k}} = \max_{j \leq k} P_{H_{0,\mathcal{M}_j}}$, it follows that $H_{0,\mathcal{M}_1}, \ldots, H_{0,\mathcal{M}_k}$ are all rejected at significance level $\alpha$. Hence, the first accepted hypothesis (if any) occurs after $i = e_{\mathcal{M}_k}$ has been eliminated. So $\hat{p}_i < \alpha$ implies $i \notin \hat{\mathcal{M}}^*_{1-\alpha}$. Conversely, if $\hat{p}_i \geq \alpha$, then for some $j \leq k$ we have $P_{H_{0,\mathcal{M}_j}} \geq \alpha$, in which case $H_{0,\mathcal{M}_j}$ is accepted at significance level $\alpha$, terminating the MCS procedure before the elimination rule reaches $e_{\mathcal{M}_k} = i$. $\square$

The interpretation of a MCS p-value is analogous to that of a classical p-value. The MCS p-value cannot be interpreted as the probability that a particular model is the best model, exactly as a classical p-value is not the probability that the null hypothesis is true. Rather, the probability interpretation is tied to the random nature of the MCS, which is a random subset of models that contains $\mathcal{M}^*$ with a certain probability.

---

## 3 Bootstrap Implementation

### 3.1 Equivalence Tests and Elimination Rules

Now we consider specific equivalence tests and elimination rules that satisfy Assumption 1. The following assumption is sufficiently strong to enable bootstrap implementation of the MCS procedure.

> **Assumption 2.** For some $r > 2$ and $\gamma > 0$ it holds that $\mathbb{E}|d_{ij,t}|^{r+\gamma} < \infty$ for all $i, j \in \mathcal{M}_0$, and that $\{d_{ij,t}\}_{i,j \in \mathcal{M}_0}$ is strictly stationary with $\mathrm{var}(d_{ij,t}) > 0$ and $\alpha$-mixing of order $-r/(r-2)$.

Assumption 2 places restrictions on the relative performance variables $\{d_{ij,t}\}$, not directly on the loss variables $\{L_{i,t}\}$. For example, a loss function need not be stationary as long as the loss differentials $\{d_{ij,t}\}$ satisfy Assumption 2. The assumption allows for some types of structural breaks and other features that can create non-stationary $\{L_{i,t}\}$, as long as all objects in $\mathcal{M}_0$ are affected in a "similar" way that preserves the stationarity of $\{d_{ij,t}\}$.

#### 3.1.1 Quadratic-Form Test

Let $\mathcal{M}$ be some subset of $\mathcal{M}_0$ and let $m$ be the number of models in $\mathcal{M} = \{i_1, \ldots, i_m\}$. We define the vector of loss-variables

$$L_t \equiv (L_{i_1,t}, \ldots, L_{i_m,t})', \quad t = 1, \ldots, n,$$

and its sample average $\bar{L} \equiv n^{-1}\sum_{t=1}^n L_t$. Let $\iota \equiv (1, \ldots, 1)'$ be the $m$-vector of ones. The orthogonal complement to $\iota$ is an $m \times (m-1)$ matrix, $\iota_\perp$, that has full column rank and satisfies $\iota_\perp' \iota = \mathbf{0}$. The $(m-1)$-dimensional vector

$$X_t \equiv \iota_\perp' L_t$$

can be viewed as $m-1$ contrasts, because each element of $X_t$ is a linear combination of $d_{ij,t}$, $i, j \in \mathcal{M}$, which has mean zero under the null hypothesis.

> **Lemma 1.** Given Assumption 2, let $X_t \equiv \iota_\perp' L_t$ and define $\theta \equiv \mathbb{E}(X_t)$. The null hypothesis $H_{0,\mathcal{M}}$ is equivalent to $\theta = 0$, and it holds that
> $$n^{1/2}(\bar{X} - \theta) \xrightarrow{d} \mathcal{N}(0,\, \Sigma),$$
> where $\bar{X} \equiv n^{-1}\sum_{t=1}^n X_t$ and $\Sigma \equiv \lim_{n \to \infty} \mathrm{var}(n^{1/2}\bar{X})$.

*Proof.* Note that $X_t = \iota_\perp' L_t$ can be written as a linear combination of $d_{ij,t}$, $i, j \in \mathcal{M}_0$, because $\iota_\perp' \iota = \mathbf{0}$. Thus $H_{0,\mathcal{M}}$ is given by $\theta = 0$, and asymptotic normality follows by the CLT for $\alpha$-mixing processes (see White, 2000a). $\square$

Lemma 1 shows that $H_{0,\mathcal{M}}$ can be tested using traditional quadratic-form statistics. An example is

$$T_Q \equiv n\bar{X}' \hat{\Sigma}^{\#} \bar{X},$$

where $\hat{\Sigma}$ is some consistent estimator of $\Sigma$ and $\hat{\Sigma}^{\#}$ denotes the Moore–Penrose inverse of $\hat{\Sigma}$.[^2] The rank $q \equiv \mathrm{rank}(\hat{\Sigma})$ represents the effective number of contrasts. Since $\hat{\Sigma} \xrightarrow{p} \Sigma$ it follows that

$$T_Q \xrightarrow{d} \chi^2_{(q)},$$

where $\chi^2_{(q)}$ denotes the chi-squared distribution with $q$ degrees of freedom. Under the alternative hypothesis, $T_Q$ diverges to infinity with probability one. So the test $\delta_\mathcal{M}$ will meet the requirements of Assumption 1 when constructed from $T_Q$. Note that $T_Q$ is invariant to the choice of $\iota_\perp$.

[^2]: Under the additional assumption that $\{d_{ij,t}\}_{i,j \in \mathcal{M}}$ is uncorrelated across $t$, one can use $\hat{\Sigma} = n^{-1}\sum_{t=1}^n (X_t - \bar{X})(X_t - \bar{X})'$. Otherwise a robust estimator along the lines of Newey and West (1987) is needed. In the context of comparing forecasts, West and Cho (1995) were first to use the test statistic $T_Q$, basing their test on asymptotic critical values from $\chi^2_{(m-1)}$.

A rejection of the null hypothesis based on the quadratic-form test need not identify an inferior alternative, because a large value of $T_Q$ can stem from several $\bar{d}_{ij}$ being slightly different from zero. In order to achieve coherence between test and elimination rule, additional testing of all sub-hypotheses of any rejected hypothesis is needed (unless nested in an accepted hypothesis). The underlying principle is known as the **closed testing procedure** (Lehmann and Romano, 2005, pp. 366–367).

#### 3.1.2 Tests Constructed from t-Statistics

This section develops two tests based on multiple $t$-statistics, bypassing the need for an explicit estimate of $\Sigma$ and simplifying construction of a coherent elimination rule.

Define the relative sample loss statistics

$$\bar{d}_{ij} \equiv n^{-1}\sum_{t=1}^n d_{ij,t} \qquad \text{and} \qquad \bar{d}_{i\cdot} \equiv m^{-1}\sum_{j \in \mathcal{M}} \bar{d}_{ij}.$$

Here $\bar{d}_{ij}$ measures the relative sample loss between the $i$-th and $j$-th models, while $\bar{d}_{i\cdot}$ is the sample loss of the $i$-th model relative to the average across models in $\mathcal{M}$. The latter follows from the identity $\bar{d}_{i\cdot} = \bar{L}_i - \bar{L}_\cdot$, where $\bar{L}_i \equiv n^{-1}\sum_{t=1}^n L_{i,t}$ and $\bar{L}_\cdot \equiv m^{-1}\sum_{i \in \mathcal{M}} \bar{L}_i$. From these statistics we construct the $t$-statistics

$$t_{ij} = \frac{\bar{d}_{ij}}{\sqrt{\widehat{\mathrm{var}}(\bar{d}_{ij})}} \qquad \text{and} \qquad t_{i\cdot} = \frac{\bar{d}_{i\cdot}}{\sqrt{\widehat{\mathrm{var}}(\bar{d}_{i\cdot})}}, \qquad \text{for } i, j \in \mathcal{M},$$

where $\widehat{\mathrm{var}}(\bar{d}_{ij})$ and $\widehat{\mathrm{var}}(\bar{d}_{i\cdot})$ denote estimates of $\mathrm{var}(\bar{d}_{ij})$ and $\mathrm{var}(\bar{d}_{i\cdot})$ respectively. The statistic $t_{ij}$ is used in the well-known test for comparing two forecasts (Diebold and Mariano, 1995; West, 1996). The $t$-statistics $t_{ij}$ and $t_{i\cdot}$ are associated with $H_{ij}: \mu_{ij} = 0$ and $H_{i\cdot}: \mu_{i\cdot} = 0$, where $\mu_{i\cdot} = \mathbb{E}(\bar{d}_{i\cdot})$.

These statistics form the basis of tests of $H_{0,\mathcal{M}}$. With $\mathcal{M} = \{i_1, \ldots, i_m\}$, the equivalence

$$\mu_{i_1} = \cdots = \mu_{i_m} \iff \mu_{ij} = 0 \; \forall\, i,j \in \mathcal{M} \iff \mu_{i\cdot} = 0 \; \forall\, i \in \mathcal{M}$$

motivates the test statistics[^3]

$$T_{\max,\mathcal{M}} = \max_{i \in \mathcal{M}}\, t_{i\cdot} \qquad \text{and} \qquad T_{R,\mathcal{M}} \equiv \max_{i,j \in \mathcal{M}}\, |t_{ij}|,$$

which are available to test $H_{0,\mathcal{M}}$. The asymptotic distributions of these test statistics are non-standard because they depend on nuisance parameters, but this poses few obstacles as the relevant distributions can be estimated with bootstrap methods.

[^3]: An earlier version of this paper has results for the test statistic $T_D = \sum_{j=1}^n t_{i\cdot}^2$ and $T_Q$.

The natural elimination rules are:

$$e_{\max,\mathcal{M}} \equiv \arg\max_{i \in \mathcal{M}}\, t_{i\cdot} \qquad \text{(for } T_{\max,\mathcal{M}}\text{)},$$

$$e_{R,\mathcal{M}} \equiv \arg\max_{i \in \mathcal{M}}\, \sup_{j \in \mathcal{M}}\, t_{ij} \qquad \text{(for } T_{R,\mathcal{M}}\text{)}.$$

> **Proposition 1.** Let $\delta_{\max,\mathcal{M}}$ and $\delta_{R,\mathcal{M}}$ denote the tests based on $T_{\max,\mathcal{M}}$ and $T_{R,\mathcal{M}}$ respectively. Then $(\delta_{\max,\mathcal{M}},\, e_{\max,\mathcal{M}})$ and $(\delta_{R,\mathcal{M}},\, e_{R,\mathcal{M}})$ satisfy the coherency of Definition 3.

*Proof.* Let $T_i$ denote either $t_{i\cdot}$ or $\max_{j \in \mathcal{M}} t_{ij}$, so that $T_{\max,\mathcal{M}}$ and $T_{R,\mathcal{M}}$ are both of the form $T = \max_{i \in \mathcal{M}} T_i$. For $i \in \mathcal{M}^*$, the definitions of $t_{i\cdot}$ and $t_{ij}$ yield the first-order stochastic dominance result:

$$P_0\!\left(\max_{i \in \mathcal{M}'} T_i > x\right) \geq P\!\left(\max_{i \in \mathcal{M}'} T_i > x\right) \quad \text{for any } \mathcal{M}' \subset \mathcal{M}^*, \text{ all } x \in \mathbb{R}.$$

The coherency now follows from:

$$\begin{aligned}
P(T > c,\; e_\mathcal{M} = i \text{ for some } i \in \mathcal{M}^*) &= P\!\left(T > c,\; T = T_i \text{ for some } i \in \mathcal{M}^*\right) \\
&= P\!\left(\max_{i \in \mathcal{M} \cap \mathcal{M}^*} T_i > c,\; T_i \geq T_j \;\forall\, j \in \mathcal{M}\right) \\
&\leq P\!\left(\max_{i \in \mathcal{M} \cap \mathcal{M}^*} T_i > c\right) \\
&\leq P_0\!\left(\max_{i \in \mathcal{M} \cap \mathcal{M}^*} T_i > c\right) \\
&\leq P_0\!\left(\max_{i \in \mathcal{M}} T_i > c\right) = P_0(T > c). \quad \square
\end{aligned}$$

Next, we establish two intermediate results that underpin the bootstrap implementation.

> **Lemma 2.** Suppose that Assumption 2 holds and define $\bar{Z} = (\bar{d}_{1\cdot}, \ldots, \bar{d}_{m\cdot})'$. Then
> $$n^{1/2}(\bar{Z} - \psi) \xrightarrow{d} \mathcal{N}_m(0,\, \Sigma), \qquad \text{as } n \to \infty, \tag{2}$$
> where $\psi \equiv \mathbb{E}(\bar{Z})$ and $\Sigma \equiv \lim_{n \to \infty} \mathrm{var}(n^{1/2}\bar{Z})$, and the null hypothesis $H_{0,\mathcal{M}}$ is equivalent to $\psi = 0$.

*Proof.* From the identity $\bar{d}_{i\cdot} = \bar{L}_i - \bar{L}_\cdot = m^{-1}\sum_{j \in \mathcal{M}} \bar{d}_{ij}$, we see that the elements of $\bar{Z}$ are linear transformations of $\bar{X}$ from Lemma 1. Thus for some $(m-1) \times m$ matrix $G$ we have $\bar{Z} = G' \bar{X}$, and the result follows with $\psi = G'\theta$ and $\Sigma = G'\Sigma G$. (The $m \times m$ covariance matrix $\Sigma$ has reduced rank, $\mathrm{rank}(\Sigma) \leq m-1$.) $\square$

In what follows, let $\varrho$ denote the $m \times m$ correlation matrix implied by $\Sigma$ from Lemma 2, and given $\xi \sim \mathcal{N}_m(0, \varrho)$, let $F_\varrho$ denote the distribution of $\max_i \xi_i$.

> **Theorem 4.** Let Assumption 2 hold and suppose that $\hat{\omega}_i^2 \equiv \widehat{\mathrm{var}}(n^{1/2}\bar{d}_{i\cdot}) = n\,\widehat{\mathrm{var}}(\bar{d}_{i\cdot}) \xrightarrow{p} \omega_i^2$, where $\omega_i^2$, $i = 1, \ldots, m$, are the diagonal elements of $\Sigma$. Under $H_{0,\mathcal{M}}$:
> $$T_{\max,\mathcal{M}} \xrightarrow{d} F_\varrho.$$
> Under $H_{A,\mathcal{M}}$, $T_{\max,\mathcal{M}} \to \infty$ in probability. Moreover, under $H_{A,\mathcal{M}}$, $T_{\max,\mathcal{M}} = t_{j\cdot}$ where $j = e_{\max,\mathcal{M}} \notin \mathcal{M}^*$, for $n$ sufficiently large.

*Proof.* Let $D \equiv \mathrm{diag}(\omega_1^2, \ldots, \omega_m^2)$ and $\hat{D} \equiv \mathrm{diag}(\hat{\omega}_1^2, \ldots, \hat{\omega}_m^2)$. From Lemma 2 it follows that

$$\xi_n = (\xi_{1,n}, \ldots, \xi_{m,n})' \equiv D^{-1/2} n^{1/2} \bar{Z} \xrightarrow{d} \mathcal{N}_m(0, \varrho),$$

since $\varrho = D^{-1/2}\Sigma D^{-1/2}$. From $t_{i\cdot} = \bar{d}_{i\cdot}/\sqrt{\widehat{\mathrm{var}}(\bar{d}_{i\cdot})} = n^{1/2}\bar{d}_{i\cdot}/\hat{\omega}_i = \xi_{i,n}\,(\omega_i/\hat{\omega}_i)$, it follows that

$$T_{\max,\mathcal{M}} = \max_i t_{i\cdot} = \max_i \bigl(\hat{D}^{-1/2} n^{1/2} \bar{Z}\bigr)_i \xrightarrow{d} F_\varrho.$$

Under $H_{A,\mathcal{M}}$, $\bar{d}_{j\cdot} \xrightarrow{p} \mu_{j\cdot} > 0$ for any $j \notin \mathcal{M}^*$, so both $t_{j\cdot}$ and $T_{\max,\mathcal{M}}$ diverge to infinity at rate $n^{1/2}$ in probability. Moreover, $e_{\max,\mathcal{M}} \notin \mathcal{M}^*$ for $n$ sufficiently large. $\square$

Theorem 4 shows that the asymptotic distribution of $T_{\max,\mathcal{M}}$ depends on the correlation matrix $\varrho$. Bootstrap methods are employed to deal with this nuisance parameter problem, leading to an asymptotically valid test. A detailed description of the bootstrap implementation is available in a separate appendix (Hansen, Lunde, and Nason, 2010). Similar results hold for the MCS constructed from $T_{R,\mathcal{M}}$ and $e_{R,\mathcal{M}}$.

---

> **Note:** Sections 3.2 onward (Variance Estimation, Regression Models), Section 4 (Related Methods), Section 5 (Simulation Study), Section 6 (Empirical Applications), Section 7 (Conclusion), and the References were not fully captured in the text extraction due to document length limits. The content above covers the complete theoretical core of the paper (Sections 1–3.1.2).

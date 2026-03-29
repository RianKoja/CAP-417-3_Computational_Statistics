The probability density function (PDF) of the **sample mean** depends on whether the underlying distribution is discrete or continuous, and on the sample size \(n\). In both cases the object of interest is the **sampling distribution of the sample mean**.

***

### Discrete case: known discrete distribution

Suppose you have a discrete random variable \(X\) with known probability mass function (PMF) \(p(x_i)\), and you draw an independent random sample \(X_1, X_2, \dots, X_n\) of size \(n\). The sample mean is  
\[
\bar X = \frac{1}{n}\sum_{i=1}^{n} X_i.
\]

- \(\bar X\) is still a **discrete** random variable, taking values on a finite or countable set (e.g., multiples of \(1/n\) if the support of \(X\) is integer‑valued). 
- Its distribution is obtained by convolving the PMF of \(X\) with itself \(n\) times and then scaling by \(1/n\).  
  - More explicitly, the PMF of \(\bar X\) at a point \(z\) is  
  \[
    P(\bar X = z) = \sum_{(x_1,\dots,x_n)\in S_n(z)} \prod_{i=1}^{n} p(x_i),
  \]
  where \(S_n(z)\) is the set of all \(n\text{‑tuples}\) such that \(\frac{1}{n}\sum x_i = z\). 
- The **density** of \(\bar X\) with respect to **counting measure** is this PMF; if you insist on viewing it as a PDF, you can write it as a sum of Dirac deltas:  
  \[
    f_{\bar X}(t) = \sum_{z \in \text{support of } \bar X} P(\bar X = z)\,\delta(t - z).
  \]

Key properties (under finite variance \(\sigma^2\)):  
- Mean: \(\mathbb{E}[\bar X] = \mu\).  
- Variance: \(\mathrm{Var}(\bar X) = \sigma^2/n\).  
- As \(n \to \infty\), the scaled distribution of \(\sqrt{n}(\bar X - \mu)\) converges weakly to a normal distribution (Central Limit Theorem). 

***

### Continuous case: known continuous distribution

Now suppose \(X\) is continuous with PDF \(f_X(x)\), mean \(\mu\), and variance \(\sigma^2\). Draw an i.i.d. sample of size \(n\) and form the sample mean \(\bar X = \frac{1}{n}\sum_{i=1}^{n} X_i\).

- The **sampling distribution of \(\bar X\)** has PDF \(f_{\bar X}(t)\) obtained by convolving \(f_X\) with itself \(n\) times and then scaling:  
  \[
    f_{\bar X}(t) = n \cdot \left( f_X^{*n} \right)(n t),
  \]
  where \(f_X^{*n}\) is the \(n\text{‑fold}\) convolution of \(f_X\). 
- For many common distributions (e.g., normal, exponential), this can be worked out in closed form; for others it is usually only implicit or approximated numerically. 

Again the summary properties are:  
- Mean: \(\mathbb{E}[\bar X] = \mu\).  
- Variance: \(\mathrm{Var}(\bar X) = \sigma^2/n\).  
- Central Limit Theorem: if \(\sigma^2 < \infty\), then for large \(n\),  
  \[
    f_{\bar X}(t) \approx \frac{1}{\sqrt{2\pi\sigma^2/n}} \exp\left(-\frac{(t - \mu)^2}{2\sigma^2/n}\right),
  \]
  i.e., the sampling distribution of \(\bar X\) is approximately normal \(\mathcal{N}(\mu,\sigma^2/n)\). 

***

### Concrete illustration

If \(X \sim \text{Bernoulli}(p)\), then \(\bar X = \frac{1}{n}\sum X_i\) takes values in \(\{0, 1/n, 2/n, \dots, 1\}\), and its PMF is  
\[
P(\bar X = k/n) = \binom{n}{k} p^k (1-p)^{n-k}, \quad k = 0,1,\dots,n.
\]  
For large \(n\), \(\bar X\) is approximately normal with mean \(p\) and variance \(p(1-p)/n\). 

If instead \(X \sim \mathcal{N}(\mu,\sigma^2)\), then \(\bar X \sim \mathcal{N}(\mu,\sigma^2/n)\) *exactly* for every \(n\ge 1\).

***

If you like, you can specify the discrete or continuous distribution you have in mind (e.g., Poisson, uniform, beta), and I can write the exact or approximate PDF of \(\bar X\) for that case.
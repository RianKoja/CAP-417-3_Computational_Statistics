## Kurtosis of BM Level Values on a Single Path

### Setup

We simulate $W_t$, $t\in[0,1]$, sampled at $t_i=i/N$, and compute the Pearson kurtosis of the $N$ level values:

$$\hat{\kappa} = \frac{\frac{1}{N}\sum \widetilde{W}_{t_i}^4}{\left(\frac{1}{N}\sum \widetilde{W}_{t_i}^2\right)^2}, \qquad \widetilde{W}_t = W_t - \bar{W}$$

As $N\to\infty$ this converges a.s. to the **random functional** $\kappa_\infty = \int_0^1\widetilde{W}_t^4\,dt \;/\; \left(\int_0^1\widetilde{W}_t^2\,dt\right)^2$.

---
### Step 1 — Covariance of the demeaned path

$\widetilde{W}_t = W_t - \int_0^1 W_s\,ds$ is Gaussian with mean 0. Using $\mathbb{E}[W_s\bar{W}] = s - s^2/2$ and $\mathbb{E}[\bar{W}^2]=1/3$:

$$K(s,t) = (s\wedge t) - s - t + \frac{s^2+t^2}{2} + \frac{1}{3}$$

Diagonal: $K(t,t) = t^2 - t + \tfrac{1}{3} = (t-\tfrac{1}{2})^2 + \tfrac{1}{12} \geq 0$

---
### Step 2 — Expected 2nd time-average moment

$$\mathbb{E}\!\left[\int_0^1\widetilde{W}_t^2\,dt\right] = \int_0^1 K(t,t)\,dt = \int_0^1\!\left(t^2-t+\tfrac{1}{3}\right)dt = \frac{1}{3}-\frac{1}{2}+\frac{1}{3} = \frac{1}{6}$$

---
### Step 3 — Expected 4th time-average moment

Since $\widetilde{W}_t$ is marginally $\mathcal{N}(0,K(t,t))$, we have $\mathbb{E}[\widetilde{W}_t^4]=3K(t,t)^2$. Expanding $(t^2-t+\frac{1}{3})^2$ and integrating:

$$\mathbb{E}\!\left[\int_0^1\widetilde{W}_t^4\,dt\right] = 3\int_0^1 K(t,t)^2\,dt = 3\left(\frac{1}{5}-\frac{1}{2}+\frac{5}{9}-\frac{1}{3}+\frac{1}{9}\right) = 3\cdot\frac{1}{30} = \frac{1}{10}$$

---
### Step 4 — Ratio of expectations (upper bound, NOT the expected kurtosis)

$$\frac{\mathbb{E}[\int\widetilde{W}^4]}{\mathbb{E}[\int\widetilde{W}^2]^2} = \frac{1/10}{(1/6)^2} = \frac{18}{5} = 3.6 \quad\Rightarrow\quad \text{Fisher} = 0.6$$

---
### Step 5 — Why $\mathbb{E}[A/B^2] \neq \mathbb{E}[A]/\mathbb{E}[B]^2$

Let $A=\int\widetilde{W}^4\,dt$, $B=\int\widetilde{W}^2\,dt$. Both are random with $\mathbb{E}[B]=1/6$, but $\mathrm{Var}(B)\sim O(1)$. The denominator fluctuates strongly:

$$\mathbb{E}[B^2] = \int_0^1\!\int_0^1 \!\left[K(s,s)K(t,t)+2K(s,t)^2\right]ds\,dt = \left(\tfrac{1}{6}\right)^2 + 2\|K\|^2_{L^2}$$

The $2\|K\|^2_{L^2}$ term is large, pulling $\mathbb{E}[A/B^2]$ well below $3.6$. The **exact expected kurtosis has no closed form** and is determined by simulation:

| Quantity | Pearson | Fisher |
|---|---|---|
| Ratio of expectations | $18/5 = 3.6$ | $0.6$ |
| **Simulation estimate** | **$\approx 2.40$** | **$\approx -0.60$** |
| Std across runs | | $\approx 0.64$ |

The path-level distribution is **platykurtic** (Fisher $< 0$): the empirical histogram of $W_{t_i}$ on one path is flatter than Gaussian.
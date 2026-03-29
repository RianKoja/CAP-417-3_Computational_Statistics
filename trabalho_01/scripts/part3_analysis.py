import numpy as np
import matplotlib.pyplot as plt
from math import gcd

def are_coprime(a, b):
    return gcd(a, b) == 1

def run_part3(max_n=10**6, seed=42):
    np.random.seed(seed)
    
    # Generate random positive integers
    # Standard choice is to use a large range to approximate samples from all integers
    a = np.random.randint(1, 2**31 - 1, size=max_n)
    b = np.random.randint(1, 2**31 - 1, size=max_n)
    
    # Check coprimality (vectorized-ish using np.frompyfunc)
    v_gcd = np.frompyfunc(gcd, 2, 1)
    coprime_mask = (v_gcd(a, b) == 1).astype(int)
    
    # Cumulative fraction of coprime pairs
    cumulative_coprime = np.cumsum(coprime_mask)
    n_range = np.arange(1, max_n + 1)
    p_est = cumulative_coprime / n_range
    
    # Pi estimation: pi = sqrt(6/p)
    # Avoid division by zero
    p_est_safe = np.where(p_est > 0, p_est, 1e-10)
    pi_est = np.sqrt(6 / p_est_safe)
    
    # Error vs N
    error = np.abs(pi_est - np.pi)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.loglog(n_range, error, label="Coprime Method Error")
    # 1.59/N as requested by the user
    plt.loglog(n_range, np.sqrt(1.59 / n_range), '--', label=r"$\sqrt{1.59/N}$ std dev")
    
    plt.xlabel("Number of Samples (N)")
    plt.ylabel("Absolute Error")
    plt.title("Pi Convergence (Coprime Trick)")
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    
    plt.savefig("outputs/plots/pi_convergence.png", dpi=300)
    plt.close()
    
    return {
        "pi_estimate": f"{pi_est[-1]:.6f}",
        "pi_samples": int(max_n)
    }

if __name__ == "__main__":
    import os
    results = run_part3()
    print(results)

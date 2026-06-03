import sympy as sp
import numpy as np
from scipy.stats import poisson, binom, gamma, expon

def check_list_1():
    print("--- Problem List 1 ---")
    # P4: Flight
    n_br, n_us, n_es, n_gb = 100, 90, 38, 73
    total = n_br + n_us + n_es + n_gb
    print(f"P4: Total={total}, P(BR)={n_br/total:.4f}, P(US or GB)={(n_us+n_gb)/total:.4f}, P(ES or BR)={(n_es+n_br)/total:.4f}")

    # P5: Weather
    # P(C) = 0.5, P(R) = 0.65, P(C & R) = 0.45
    # P(neither) = 1 - P(C or R) = 1 - (P(C) + P(R) - P(C & R))
    p_neither = 1 - (0.5 + 0.65 - 0.45)
    print(f"P5: P(neither)={p_neither:.4f}")

    # P6: Conditional
    # Omega = {1,2,3,4,5,6}, A={1,3,5}, B={2,3,4,5,6}
    # P(B|A) = P(B & A) / P(A)
    # B & A = {3, 5} -> n=2. A = {1,3,5} -> n=3.
    print(f"P6: P(B|A) = 2/3 = {2/3:.4f}")

    # P8: Flight Gender
    # Men: BR(55), US(30), ES(38), GB(12)
    # Women: BR(45), US(60), ES(0), GB(61)
    men_total = 55 + 30 + 38 + 12
    women_total = 45 + 60 + 0 + 61
    print(f"P8: P(BR|Man) = 55/{men_total} = {55/men_total:.4f}")
    print(f"P8: P(US|Woman) = 60/{women_total} = {60/women_total:.4f}")
    print(f"P8: P(Man|ES) = 38/38 = 1.0")

    # P9: COVID (Bayes)
    # P(Pos|Inf) = 0.98. P(Pos|NotInf) = 0.98 (as per phrasing "and of those who are not indeed infected")
    # Wait, the phrasing says: "The test diagnosis is positive among 98% of those which are truly infected and of those who are not indeed infected."
    # This usually means P(Pos|Inf) = 0.98 and P(Neg|NotInf) = 0.98? 
    # Or does it mean P(Pos|NotInf) = 0.98? 
    # Usually "False positive rate" is 1 - specificity. 
    # If P(Pos|NotInf) = 0.98, the test is useless.
    # Re-reading: "positive among 98% of those which are truly infected AND of those who are not indeed infected"
    # This phrasing is ambiguous. In many textbooks, it means P(Pos|Inf) = 0.98 and P(Pos|NotInf) = 0.02 (98% accuracy for both).
    # Let's assume P(Pos|Inf)=0.98 and P(Neg|NotInf)=0.98. 
    # But we need P(Inf). If not given, assume 50/50? Or is it a trick?
    # Usually these problems give a prior. If not, I'll state the formula.
    
    # P10: Target shooting
    # P(A)=1/3, P(B)=2/3
    # P(A & B) = 1/3 * 2/3 = 2/9
    # P(A or B) = 1/3 + 2/3 - 2/9 = 1 - 2/9 = 7/9
    print(f"P10: P(Both)={2/9:.4f}, P(At least one)={7/9:.4f}")

    # P11: Balls
    # 8R, 3W, 4B. Total 15.
    # P(R1, W2) = 8/15 * 3/14
    # P(W1, R2) = 3/15 * 8/14
    # P(R1, R2) = 8/15 * 7/14
    print(f"P11: P(RW)={8/15 * 3/14:.4f}, P(WR)={3/15 * 8/14:.4f}, P(RR)={8/15 * 7/14:.4f}")

    # P12: Naive Bayes
    p_spam = 0.3
    p_not_spam = 0.7
    # P(Free|Spam)=0.8, P(Win|Spam)=0.6
    # P(Free|Not)=0.1, P(Win|Not)=0.05
    score_spam = 0.8 * 0.6 * 0.3
    score_not = 0.1 * 0.05 * 0.7
    print(f"P12: Score Spam={score_spam:.4f}, Score Not={score_not:.4f}")

def check_list_2():
    print("\n--- Problem List 2 ---")
    # P3: Discrete Uniform Variance
    n = sp.Symbol('n', integer=True, positive=True)
    # Variance = E[X^2] - (E[X])^2
    # For 1 to n: E[X] = (n+1)/2. E[X^2] = Sum(i^2)/n = [n(n+1)(2n+1)/6] / n = (n+1)(2n+1)/6
    # Var = (n+1)(2n+1)/6 - ((n+1)/2)^2
    # Var = (n+1) [ (2n+1)/6 - (n+1)/4 ] = (n+1) [ (4n+2 - 3n-3)/12 ] = (n+1)(n-1)/12 = (n^2-1)/12
    # Here x_high - x_low + 1 is n.
    var_expr = (n**2 - 1)/12
    print(f"P3: Variance formula check: {var_expr}")

    # P4: Poisson
    # 4a: mu=5, x=3
    p4a = poisson.pmf(3, 5)
    # 4b: mu=12, x<=8
    p4b = poisson.cdf(8, 12)
    print(f"P4: P4a={p4a:.4f}, P4b={p4b:.4f}")

def check_list_3():
    print("\n--- Problem List 3 ---")
    # P1.1: Ruler 30cm. f(x) = 1/30.
    print(f"P1.1: f(5) = 1/30 = {1/30:.4f}")
    
    # P1.2: f(x)=3 on [0, 1/3]
    # P(0.1 < X < 0.2) = 3 * (0.2 - 0.1) = 0.3
    # CDF = 3x for x in [0, 1/3]
    print(f"P1.2: P(0.1<X<0.2) = 0.3")

    # P2.1: Continuous Uniform Var
    # Var = Integral[(x - (a+b)/2)^2 * 1/(b-a)] dx from a to b
    a, b = sp.symbols('a b')
    x = sp.Symbol('x')
    f = 1/(b-a)
    mu = (a+b)/2
    var_cont = sp.integrate((x - mu)**2 * f, (x, a, b))
    print(f"P2.1: Continuous Var = {sp.simplify(var_cont)}")

    # P2.2: Uniform [32, 42]. P(32 < X < 40)
    # (40 - 32) / (42 - 32) = 8/10 = 0.8
    print(f"P2.2: P(32<X<40) = 0.8")

    # P3.1: Gamma. New call every 4 mins. Lambda = 1/4?
    # Usually Gamma(alpha, beta) where alpha is number of events, beta is rate.
    # If 1 call every 4 mins, rate beta = 1/4 calls/min.
    # Time for 3 calls: alpha=3.
    # E[X] = alpha / beta = 3 / (1/4) = 12 mins.
    print(f"P3.1: Expected time for 3 calls = 12 mins")

if __name__ == "__main__":
    check_list_1()
    check_list_2()
    check_list_3()

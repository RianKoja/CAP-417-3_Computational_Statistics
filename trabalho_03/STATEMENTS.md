# Problem 1:
Explain the theory of sampling distribution, the distribution of the sample mean, for a discrete and a continuous distribution. 

Show a working example: Create set of 1_000_000 values. Plot the true distribution, compute the mean and std, then use bootstrap with few samples to estimate the mean and std. Then use a large sample size to estimate the mean and std. Do this repeatedly to estimate the std of estimating the mean with a large sample versus estimating it with bootstrap. Compare the results.

# Problem 2:

Given the motivation problem:
A sample of 25 adult males from a city showed that the cholesterol level has a mean of 186 and a standard deviation of 12. Considering that in this city the cholesterol level among the adult male population follows a normal distribution, obtain the 95% confidence interval for the mean.

Explain central limit theorem to show what the distribution of the sample mean and sample standard deviation is. Then create the confidence interval analytically for both.

# Problem 3
This is an optional exercise that involves using a problem with my own data.
We'll take isnpiration from trabalho_03/references/or_mcs/helpers/demo_figs.py

We'll create a similar script, but remember that we'll be using typst for the final document and we want to demosntrate the MCS procedure. 

First, we'll add an explanation of the MCS procedure. Explain the main theorems from the Hanse, Lunde, Nason paper, then explain how to itnerpret results.

Second let's show an example where it shines: Is actually points out the best model among a set of candidate models. We'll use different functions with added noise, create a training and test set, and then use MCS to select the best model. We'll plot the results to show that MCS is able to select the best model.

Third, let's show an example where it fails: We'll show again the plot that is currently on references/or_mcs/helpers/demo_results_linear.svg and whose MCS p-values and other metrics are already computed. We'll explain why MCS and other methods fail to identify the best model in this case.
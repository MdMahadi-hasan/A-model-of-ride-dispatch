import numpy as np
import pandas as pd
from scipy.stats import poisson
import ace_tools as tools

# Create grid
ns = np.arange(1, 6)  # n=1..5
mus = np.linspace(0.1, 5, 50)  # mu grid

records = []

for n in ns:
    k = 6 - n
    for mu in mus:
        # Original inequality
        delta_g = 1 - poisson.cdf(k-1, mu)
        # g_k = E[min(M, k)]
        pmf_vals = poisson.pmf(np.arange(0, k+20), mu)
        # compute g_k exactly
        g_k = sum(j * pmf_vals[j] for j in range(k+1)) + k * (1 - sum(pmf_vals[:k+1]))
        lhs_orig = n * delta_g + g_k
        rhs_orig = (2*mu**2 + n*mu) * poisson.pmf(k-1, mu) + mu * poisson.cdf(k-1, mu)
        orig = lhs_orig > rhs_orig
        
        # Finite-sum condition
        term_sum = 0.0
        for j in range(0, k-1):
            term_sum += (6 - j + mu) * mu**j / np.math.factorial(j)
        term_sum += ((n+1) + (n+1)*mu + 2*mu**2) * mu**(k-1) / np.math.factorial(k-1)
        finite_sum = 6 * np.exp(mu) > term_sum
        
        # Exponential bound
        exp_bound = np.exp(mu) > (1 + mu + 2*mu**2 / (n+1))
        
        records.append({'n': n, 'mu': round(mu, 3),
                        'original': orig,
                        'finite_sum': finite_sum,
                        'exp_bound': exp_bound})

df = pd.DataFrame(records)

# Check mismatches
df['orig_vs_fs'] = df['original'] == df['finite_sum']
df['fs_vs_exp'] = df['finite_sum'] == df['exp_bound']

# Display summary
summary = pd.DataFrame([{
    'Total points': len(df),
    'Original vs Finite-sum matches': df['orig_vs_fs'].sum(),
    'Finite-sum vs Exp-bound matches': df['fs_vs_exp'].sum(),
    'Original vs Exp-bound matches': ((df['original'] == df['exp_bound']).sum())
}])

tools.display_dataframe_to_user("Numerical Equivalence Summary", summary)

# Also display a few sample rows
tools.display_dataframe_to_user("Sample Checks", df.head(10))

import numpy as np
import matplotlib.pyplot as plt
import math

# Parameters
pI = 1.0
lambda_rate = 1.0
T = 0.33
wbar = 0.5  # hours

# Compute values
n_vals = np.arange(1, 7)
g_vals = []
for n in n_vals:
    k = 6 - n
    mu = lambda_rate * T
    pmf = [math.exp(-mu) * mu**m / math.factorial(m) for m in range(0, k+1)]
    cdf_k = sum(pmf)
    expected_trunc = sum(m * pmf[m] for m in range(len(pmf))) + k * (1 - cdf_k)
    g_vals.append(expected_trunc)
g_vals = np.array(g_vals)

# Profit per unit time π(n)
A = pI * (n_vals + 0.5 * g_vals)
B = n_vals / lambda_rate + 2 * T
profit = A / B

# Expected wait E[W(n)] = (n-1)/(2λ)
ewait = (n_vals - 1) / (2 * lambda_rate)

# Demand ceiling
ceiling_n = int(math.floor(2 * lambda_rate * wbar + 1))

# Equilibrium point coordinates
idx = ceiling_n - 1  # zero-based index
x_eq = n_vals[idx]
y_eq = profit[idx]

# Plot
fig, ax1 = plt.subplots(figsize=(8, 5))

# Profit line
ax1.plot(n_vals, profit, '-o', color='black', label=r'Profit $\pi(n)$')
ax1.set_xlabel('Departure threshold $n$')
ax1.set_ylabel('Profit per unit time $\pi(n)$', color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Shade infeasible region
ax1.axvspan(ceiling_n + 1, 6.5, color='gray', alpha=0.2, label='Infeasible: $E[W(n)] > \\bar w$')

# Vertical equilibrium line
ax1.axvline(ceiling_n, color='blue', linestyle='--')

# Annotate equilibrium exactly at (n*, π(n*))
ax1.annotate(r'$n^*$', 
             xy=(x_eq, y_eq), 
             xytext=(x_eq + 0.8, y_eq),
             color='blue', fontsize='small', ha='left',
             arrowprops=dict(arrowstyle='->', color='blue'))

# Secondary axis for expected wait
ax2 = ax1.twinx()
ax2.plot(n_vals, ewait, '--s', color='gray', label=r'Expected wait $E[W(n)]$')
ax2.axhline(wbar, color='red', linestyle=':', label=r'$\bar w$ (max tolerated wait)')
ax2.set_ylabel('Expected wait $E[W(n)]$ (hr)', color='gray')
ax2.tick_params(axis='y', labelcolor='gray')

# Combine legend inside plot
lines_labels = [ax.get_legend_handles_labels() for ax in [ax1, ax2]]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
ax1.legend(lines, labels, loc='center right', frameon=False, fontsize='small', bbox_to_anchor=(0.95, 0.5))

# Axes formatting
ax1.set_xticks(n_vals)
ax1.set_xlim(0.5, 6.5)
ax1.grid(False)
ax2.grid(False)
for spine in ax1.spines.values():
    spine.set_linewidth(1)

plt.title('Profit vs. Waiting-Time Constraint', fontsize='medium')
plt.tight_layout()
plt.show()

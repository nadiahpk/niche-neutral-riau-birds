# check that the number of species on each island in the samples matches well the Chisholm curve

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import sys
sys.path.insert(0,'../../functions')

from my_functions import S_fnc # S_fnc(theta, K, J_k, m)


# parameters
# ---

# which fit should we use for the parameter values? 
rho = 1700
subset_name = 'survey_only'
#subset_name = 'peninsula_only'

# where are the parameter values from when the Chisholm model was fitted to Keita's data
fname_chisholm_fit = '../../results/area_richness_curve/best_fits.csv'

# where is processed information about islands?
dir_processed = '../../data/processed/'

# where to put results
dir_results = '../../results/neutral_data/'


# get the island richnesses and percentiles
# ---

fname = dir_results + 'percentiles_richness_' + subset_name + '.csv'
df = pd.read_csv(fname)

island_names = df['island_name'].values # fixed ordering for islands
area = df['area_sq_km'].values
S = df['S'].values # fixed ordering for islands


# plot true data points
# ---

plt.scatter(area, S, color='red', alpha=0.7, label='survey data')


# plot niche-neutral model fit
# ---

# get fitted parameter values
df_fit = pd.read_csv(fname_chisholm_fit)
row = df_fit[(df_fit['subset_name'] == subset_name) & (df_fit['rho'] == rho) ]
K = row.iloc[0]['K']
theta = row.iloc[0]['theta_est']
m = row.iloc[0]['m_est']

# plot it over a suitable range
A_max = max(area); A_min = min(area)
A_pwr_min = np.log10(A_min); A_pwr_max = np.log10(A_max)
A_pwrV = np.linspace( A_pwr_min, A_pwr_max, 100 )
AV = 10**A_pwrV
JV = AV*rho
SV = [S_fnc(theta, K, J/K, m) for J in JV]
plt.plot(AV, SV, ls='dotted', color='black', label='niche-neutral model')

# vertical line for the Acrit
A_crit = row.iloc[0]['A_crit_est']
plt.axvline(A_crit, ls='dashed', color='black', label=r'$A_{crit}$')

# plot percentiles of sequential sampling algorithm
# ---

mean_S = df['model_mean_S'].values
lo_S = df['model_lo_S'].values
hi_S = df['model_hi_S'].values

# order by area
a_m_lo_hi = sorted(list(zip(area, mean_S, lo_S, hi_S)), key=lambda v: v[0])
areas, means, los, his = zip(*a_m_lo_hi)

# plot the means
plt.scatter(areas, means, color='blue', marker='_', label='sampling (95 pctl)')

# plot a vert line for each percentile?
for area, _, lo, hi in a_m_lo_hi:

    plt.plot([area, area], [lo, hi], alpha=0.7, color='blue')


# save plot
# ---

plt.xlabel(r'island area (km$^2$)', fontsize='xx-large')
plt.ylabel(r'species richness', fontsize='xx-large')
plt.legend(loc='best', fontsize='medium')
plt.xscale('log')
plt.tight_layout()
plt.savefig(dir_results + 'area_v_richness_' + subset_name + '.pdf')
plt.close()

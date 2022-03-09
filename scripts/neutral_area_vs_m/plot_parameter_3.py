# plot each of the parameter sets in an array

#from scipy.special import digamma
import matplotlib.pyplot as plt
import pandas as pd

import sys
sys.path.append("../../functions")

from my_functions import S_fnc


# parameters
# ---

# where results go
dir_results = '../../results/neutral_area_vs_m/'
suffix = '_3'

# the two axes for the plot
J_names = ['J3', 'J2', 'J1']
m_names = ['m1', 'm2', 'm3', 'm4', 'm5']


# get the parameter values for the parameters that didn't vary
# ---

fname_csv = dir_results + 'baseline.csv'
df = pd.read_csv(fname_csv)
df = df[df['suffix'] == suffix] # subset the suffix we want

# record each of the baseline parameter values
# columns = ['suffix', 'K', 'H', 'm', 'theta', 'J', 'S']
K = df['K'].values[0]
H = df['H'].values[0]
theta = df['theta'].values[0]


# get the parameter values that did vary
# ---


fname_csv = dir_results + 'parameter' + suffix + '_Jm.csv'
df = pd.read_csv(fname_csv)
df = df[df['suffix'] == suffix] # subset the suffix we want


# get species richness curves for each combination
# ---


SVD = dict()
for J_idx, J_name in enumerate(J_names):

    SVD[J_name] = dict()

    for m_idx, m_name in enumerate(m_names):

        JV = df[J_name].values
        mV = df[m_name].values

        SV = [ S_fnc(theta, K, J/K, m) for m, J in zip(mV, JV) ]

        SVD[J_name][m_name] = SV


# make a big subplots of the species richness curves
# ---

fig, axs = plt.subplots(3, 5, sharex=True, sharey=True, figsize=(20,9))

island_IDs = list(range(H))

fig.add_subplot(111, frameon=False) # for shared x and y labels
for J_idx, J_name in enumerate(J_names):

    for m_idx, m_name in enumerate(m_names):

        SV = SVD[J_name][m_name]

        axs[J_idx, m_idx].plot( island_IDs, SV, '-o', color='black' )
        axs[J_idx, m_idx].set_xticks(island_IDs)

plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False) # for labels
plt.xlabel('island', fontsize='x-large')
plt.ylabel('species richness', fontsize='x-large')
plt.tight_layout()
plt.savefig(dir_results + 'parameter' + suffix + '_Jm.pdf')
plt.close()

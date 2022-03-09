# take the best-fitting model and further fit the migration parameter (m) to the data


import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from scipy.optimize import bisect

import sys
sys.path.insert(0,'../../functions')

from my_functions import S_fnc # S_fnc(theta, K, J, m)


# parameters
# ---

# which subset to do
subset = 'survey_only'
rho = 1700

# which island subsets info kept
dirname_subsets = '../../data/processed/island_subsets/'

# where to find the island area and richness data
fname_area = '../../data/processed/island_area.csv'     # island_name,area_sq_m,area_sq_km
fname_rich = '../../data/processed/island_richness.csv' # island_name,richness

# where are fits of island subsets
fname_fits = '../../results/area_richness_curve/best_fits.csv'

# where to put results
dir_results = '../../results/neutral_data_fitm/'


# create a dataframe: island_name, area, richness
# ---

df_area = pd.read_csv(fname_area)
df_rich = pd.read_csv(fname_rich)
assert len(df_area) == len(df_rich), f'Number of islands in {fname_area} =/= {fname_rich}'
df_data = pd.merge(df_area, df_rich, on="island_name")

# subset the data to the subset of interest

# which islands are in this subset
islands = list( pd.read_csv( dirname_subsets + subset + '.csv', header=0 )['island_name'] )

# subset the data to those islands
df_data_sub = df_data[df_data['island_name'].isin(islands)]


# read in the best fit
# ---

df_fits = pd.read_csv(fname_fits, header=0)
best_fit = df_fits[ (df_fits['subset_name'] == subset) & (df_fits['rho'] == rho) ]
K = best_fit['K'].values[0]
theta = best_fit['theta_est'].values[0]
m = best_fit['m_est'].values[0]
A_crit = best_fit['A_crit_est'].values[0]


# for each island, tune m to fit the richness exactly
# ---

mV = list()
JV = list()
for island in islands:

    # get basic island info
    # ---

    A = df_data_sub[df_data_sub['island_name'] == island]['area_sq_km'].values[0]
    J = A*rho
    JV.append(J)
    Jk = J/K # the total area is divided into K niches and multiplied by the density
    S_tru = df_data_sub[df_data_sub['island_name'] == island]['richness'].values[0]

    if S_tru <= K:

        # in this case, the best-fitting m is m=0
        # so, in the absence of better choices, just append
        # the original fitted m
        mV.append(m)

    else:

        # find m_i satisfies S_fnc == S_tru
        # ---

        # get upper and lower search area for m

        S_fit = S_fnc(theta, K, Jk, m)
        S_lo = S_fit; S_hi = S_fit
        m_lo = m; m_hi = m

        if S_fit < S_tru:

            while S_hi < S_tru:

                m_lo = m_hi
                m_hi = 2*m_hi
                S_hi = S_fnc(theta, K, Jk, m_hi)

        else:

            while S_lo > S_tru:

                m_hi = m_lo
                m_lo = m_lo/2
                S_lo = S_fnc(theta, K, Jk, m_lo)

        # find the m_i that satisfies and store

        m_i = bisect(lambda m_i: S_fnc(theta, K, Jk, m_i)-S_tru, m_lo, m_hi)
        mV.append(m_i)


# write the new parameter set to file
# ---

# create dataframe to save
columns = ['subset_name', 'rho', 'H', 'theta', 'K', 'T'] + ['m_' + island for island in islands] + ['J_' + island for island in islands]
H = len(islands)
data_row = [subset, rho, H, theta, K, np.inf] + mV + JV
data_rows = [data_row]
df_out = pd.DataFrame.from_records(data_rows, columns=columns)

# save datafrmae
fname_csv = dir_results + 'archipelago_params.csv'
df_out.to_csv(fname_csv, mode='w', header=True, index=False)

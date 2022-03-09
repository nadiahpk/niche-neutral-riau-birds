# take the best-fitting model and further fit the number of niches (K) to the data


import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#from scipy.optimize import bisect

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
dir_results = '../../results/neutral_data_fitK/'


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

thetak = theta / K


# for each island, tune m to fit the richness exactly
# ---

KV = list()
JV = list()
SV = list()
for island in islands:

    # get basic island info
    # ---

    A = df_data_sub[df_data_sub['island_name'] == island]['area_sq_km'].values[0]
    J = A*rho
    JV.append(J)
    S_tru = df_data_sub[df_data_sub['island_name'] == island]['richness'].values[0]


    # find the K_lo and K_hi nearest the true value
    # ---

    K_lo = 1
    S_lo = S_fnc(thetak*K_lo, K_lo, J/K_lo, m)

    if S_tru < S_lo:

        # this is as low as it could go, so just append this value
        KV.append(K_lo)
        SV.append(S_lo)

    else:

        K_hi = K_lo + 1
        S_hi = S_fnc(thetak*K_hi, K_hi, J/K_hi, m)

        while S_hi < S_tru:

            S_lo = S_hi
            K_lo = K_hi

            K_hi += 1
            S_hi = S_fnc(thetak*K_hi, K_hi, J/K_hi, m)

        # append whichever was closest
        if abs(S_tru - S_lo) < abs(S_tru - S_hi):

            KV.append(K_lo)
            SV.append(S_lo)

        else:

            KV.append(K_hi)
            SV.append(S_hi)




# write the new parameter set to file
# ---

# create dataframe to save
columns = ['subset_name', 'rho', 'H', 'theta_k', 'm', 'T'] + ['K_' + island for island in islands] + ['J_' + island for island in islands]
H = len(islands)
data_row = [subset, rho, H, thetak, m, np.inf] + KV + JV
data_rows = [data_row]
df_out = pd.DataFrame.from_records(data_rows, columns=columns)

# save datafrmae
fname_csv = dir_results + 'archipelago_params.csv'
df_out.to_csv(fname_csv, mode='w', header=True, index=False)

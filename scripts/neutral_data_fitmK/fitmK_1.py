# Fit according to these rules:
# if S <= K, set K_new = S
# if S > K
#   if m_fit in [m/10, 10*m] can make S_fit = S
#       m_new = m_fit; K_new = K
#   else
#       m_tmp = m/10 or 10*m
#       K_new = K_fit
#       then tune m_new = m_fit


import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from scipy.optimize import bisect

import sys
sys.path.insert(0,'../../functions')

from my_functions import S_fnc # S_fnc(theta, K, J, m)


# parameters
# ---

# default m otherwise fitted
m_dft = 0.0036105103995363757 # NOTE hardcoding for now

no_samples = 40 # number of samples to draw using the spp generator

# where are the fitted m values
fname_fit = '../../results/neutral_data_fitm/archipelago_params.csv'

# which fit should we use for the parameter values? 
rho = 1700
subset_name = 'survey_only'

# where is processed information about islands?
dir_processed = '../../data/processed/'

# where to put results
dir_results = '../../results/neutral_data_fitmK/'


# get information about the islands used for this subset
# ---

# get names of islands
fname_islands = dir_processed + 'island_subsets/' + subset_name + '.csv'
island_names = list( pd.read_csv( fname_islands, header=0 )['island_name'] )

# get their richness
fname_rich = dir_processed + 'island_richness.csv'
df_rich = pd.read_csv(fname_rich)
df_rich.set_index('island_name', inplace=True)
#S_truV = [ df_rich.loc[island_name]['richness'] for island_name in island_names ]

#fname_area = dir_processed + 'island_area.csv'
#df_area = pd.read_csv(fname_area)
#df_area.set_index('island_name', inplace=True)
#areas = [ df_area.loc[island_name]['area_sq_km'] for island_name in island_names ]


# get fitted m values
# ---

df_fit = pd.read_csv(fname_fit)
fitm = df_fit[(df_fit['subset_name'] == subset_name) & (df_fit['rho'] == rho) ].iloc[0]
theta = fitm['theta']
K = fitm['K']

# set theta_k, the biodiversity per niche, to a default value
theta_k = theta / K


# fit new parameters according to the rules
# ---

K_new = list()
m_new = list()
S_new = list()
#island_name = island_names[9]
#if True:
for island_name in island_names:

    # m fit and parameters for this island
    m = fitm['m_' + island_name]
    J = fitm['J_' + island_name]
    S_tru = df_rich.loc[island_name]['richness']

    if S_tru <= K:

        K_new.append(S_tru)
        m_new.append(m_dft)
        S_new.append( S_fnc(theta_k*S_tru, S_tru, J/S_tru, m_dft) )

    else:

        m_lo = m_dft / 10
        m_hi = 10*m_dft

        S_fitm_lo = S_fnc(theta_k*K, K, J/K, m_lo)
        S_fitm_hi = S_fnc(theta_k*K, K, J/K, m_hi)

        if S_fitm_lo < S_tru and S_tru < S_fitm_hi:

            # only fitting m
            K_new.append(K)
            m_new.append(m)
            S_new.append( S_fnc(theta_k*K, K, J/K, m) )

        else:

            # fitting both m and K

            # is m not low enough or not high enough
            if S_tru < S_fitm_lo:
                m_i = m_lo
            else:
                m_i = m_hi
            
            # fit K given m_i

            K_lo = 1
            S_lo = S_fnc(theta_k*K_lo, K_lo, J/K_lo, m_i)
            K_hi = K_lo + 1
            S_hi = S_fnc(theta_k*K_hi, K_hi, J/K_hi, m_i)

            while S_hi < S_tru:

                S_lo = S_hi
                K_lo = K_hi
                K_hi += 1
                S_hi = S_fnc(theta_k*K_hi, K_hi, J/K_hi, m_i)

            # choose whichever was closest
            K_i = K_lo if abs(S_tru - S_lo) < abs(S_tru - S_hi) else K_hi

            # but don't allow K_i = S_tru here NOTE a bit of arbitrary rule to deal with panggal sedang
            K_i = K_i-1 if K_i == S_tru else K_i

            # calculate fit
            S_fit = S_fnc(theta_k*K_i, K_i, J/K_i, m_i)

            # final tune of m

            # find upper and lower bounds for m

            m_lo = m_i; m_hi = m_i
            S_lo = S_fit; S_hi = S_fit

            if S_fit < S_tru:

                while S_hi < S_tru:

                    m_lo = m_hi
                    m_hi = 2*m_hi
                    S_hi = S_fnc(theta_k*K_i, K_i, J/K_i, m_hi)

            else:

                while S_lo > S_tru:

                    m_hi = m_lo
                    m_lo = m_lo/2
                    S_lo = S_fnc(theta_k*K_i, K_i, J/K_i, m_lo)

            # fit
            m_i = bisect(lambda m_i: S_fnc(theta_k*K_i, K_i, J/K_i, m_i)-S_tru, m_lo, m_hi)
            S_fit = S_fnc(theta_k*K_i, K_i, J/K_i, m_i)

            # store
            K_new.append(K_i)
            m_new.append(m_i)
            S_new.append( S_fit )


# create J[k][h], the number of individuals in each niche on each island
# ---

max_K = max(K_new)
JkL = list()
headL = list()
for K, island_name in zip(K_new, island_names):

    J = fitm['J_' + island_name]

    # assume J is evenly split between niches
    Jk = J / K

    # assume niches are filled in order
    JV = [Jk]*K + [0]*(max_K-K)

    # append to the column header and list of J values
    JkL += JV
    headL += [ 'J_' + str(kk) + '_' + island_name for kk in range(max_K) ]


# write the new parameter set to file
# ---

# create dataframe to save
columns = ['subset_name', 'rho', 'H', 'theta_k', 'max_K', 'T'] 
columns += ['m_' + island for island in island_names] 
columns += ['K_' + island for island in island_names] 
columns += headL

data_row = [subset_name, rho, len(island_names), theta_k, max_K, np.inf] + m_new + K_new + JkL
data_rows = [data_row]
df_out = pd.DataFrame.from_records(data_rows, columns=columns)

# save datafrmae
fname_csv = dir_results + 'archipelago_params_1.csv'
df_out.to_csv(fname_csv, mode='w', header=True, index=False)

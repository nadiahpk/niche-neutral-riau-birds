# Contrive a fit that might make it look like the real data

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from scipy.optimize import bisect

import sys
sys.path.insert(0,'../../functions')

from my_functions import S_fnc # S_fnc(theta, K, J, m)


# parameters
# ---

# NOTE my contrivance for the niches on each island
island2niches = {
        'lingga'        : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        'sebangka'      : [0, 1, 2, 3, 4, 10],
        'temiang'       : [0, 1, 2, 3, 4, 5, 6, 7],
        'durian'        : [0, 1, 2, 3, 4, 5, 6, 11],
        'ngenang'       : [0, 1, 2, 3, 4, 5, 6, 7],
        'momoi'         : [0, 1, 2, 3, 4, 5, 6, 7],
        'tinjul'        : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        'akar'          : [0, 1, 2, 3, 4, 5, 6, 7],
        'remang_besar'  : [0, 1, 2, 3, 4, 5, 6, 7],
        'sambu_kecil'   : [0, 1, 2, 3, 4, 5, 6, 7],
        'remang_kecil'  : [0, 1, 2, 3, 4, 5, 6, 7],
        'matang_cilik'  : [1, 2, 3, 6, 7],
        'panggal_besar' : [0, 1, 2, 3, 4, 5, 6, 7],
        'malang'        : [0, 1, 2, 3, 4, 5, 6, 7],
        'paloi_besar'   : [0, 1, 2, 3, 4, 5, 6, 7],
        'sepatu'        : [0, 1, 2, 3, 4, 5, 6, 7],
        'panggal_sedang': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        'nipong'        : [0, 1, 2, 3, 5, 6, 7],
        'sayap'         : [0, 1, 3, 4, 5, 6],
        'telor_besar'   : [0, 2, 7],
        'paloi_kecil'   : [3],
        'telor_kecil'   : [5, 6],
        'panggal_kecil' : [0, 1, 3, 4, 5, 6, 7],
}
max_K = 12 # how many niches total

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
    niches = island2niches[island_name]
    K_i = len(niches)
    S_fit = S_fnc(theta_k*K_i, K_i, J/K_i, m)

    if S_tru <= K:

        K_new.append(K_i)
        m_new.append(m)
        S_new.append(S_fit)

    else:

        # tune m

        m_lo = m; m_hi = m
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

#check = list()
JkL = list()
headL = list()
for K, island_name in zip(K_new, island_names):

    J = fitm['J_' + island_name]

    # assume J is evenly split between niches
    Jk = J / K

    # assume niches are filled according to my contrivance
    niches = island2niches[island_name]
    JV = [ Jk if k in niches else 0 for k in range(max_K) ]
    #check.append([ 1 if k in niches else 0 for k in range(max_K) ])

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
fname_csv = dir_results + 'archipelago_params_2.csv' # NOTE suffix change here
df_out.to_csv(fname_csv, mode='w', header=True, index=False)

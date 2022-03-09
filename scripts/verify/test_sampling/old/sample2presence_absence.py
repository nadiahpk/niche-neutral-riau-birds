# turn a data row into a presence-absence matrix

import pandas as pd
import numpy as np


# parameters
# ---

sample_ID = 2
suffix = '_1'

# where to save results
dir_results = '../../../results/verify/test_sampling/'


# read in desired record
# ---

fname = dir_results + 'samples' + suffix + '.csv'
df_in = pd.read_csv(fname, skiprows=[0], header=None)
df_sub = df_in[df_in.iloc[:,0] == sample_ID]


# turn the data row into a presence-absence matrix
# ---

S = df_sub.iloc[0,1]    # number of species
H = df_sub.iloc[0,2]    # number of islands
K = df_sub.iloc[0,3]    # number of niches

# no_spp_niche starts at:
idx = 5 + 3*H 
spp_in_niches = df_sub.iloc[0, idx : idx+K].values.astype('int')

# presence-absence matrix starts after that
data_row = df_sub.iloc[0, idx+K:].values
data_row = data_row[ ~ np.isnan(data_row) ].astype('int')

# create island names, species names
isle_names = [ 'simulated_' + str(h) for h in range(H) ]
spp_IDs = [ (k, i) for k, spp_in_niche in zip(range(K), spp_in_niches) for i in range(spp_in_niche) ]
spp_names = [ 'species_' + str(k) + '_' + str(i) for k, i in spp_IDs ]

# create the data frame
data = {isle_name: data_row[i:i+S] for i, isle_name in zip(range(0, S*H, S), isle_names) }
df = pd.DataFrame(data, index=spp_names)

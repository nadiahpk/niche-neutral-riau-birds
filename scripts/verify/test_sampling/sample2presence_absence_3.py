# turn a data row into a presence-absence matrix

# import numpy as np
import pandas as pd
# import csv as csv

from helpers import sample2matrix


# parameters
# ---

sample_ID = 2
suffix = '_3'

# where to save results
dir_results = '../../../results/verify/test_sampling/'


# get the presence-absence matrix
# ---

fname = dir_results + 'samples' + suffix + '.csv'
df = sample2matrix(fname, sample_ID)


'''
# read in desired record
# ---

fname = dir_results + 'samples' + suffix + '.csv'

df_in = pd.read_csv(fname)
row = df_in[df_in['sample_ID'] == sample_ID ]

S = row.iloc[0]['no_spp_S']
H = row.iloc[0]['no_isles_H']
K = row.iloc[0]['K']

spp_in_niches = [ row.iloc[0]['no_spp_niche_' + str(idx)] for idx in range(K) ]

data_row_as_str = row.iloc[0]['presence_absence_matrix_cols_(isles)_concatenated']
data_row = [ 1 if s == 'p' else 0 for s in data_row_as_str ]


# turn the data row into a presence-absence matrix
# ---

# create island names, species names
isle_names = [ 'simulated_' + str(h) for h in range(H) ]
spp_IDs = [ (k, i) for k, spp_in_niche in zip(range(K), spp_in_niches) for i in range(spp_in_niche) ]
spp_names = [ 'species_' + str(k) + '_' + str(i) for k, i in spp_IDs ]

# create the data frame
data = {isle_name: data_row[i:i+S] for i, isle_name in zip(range(0, S*H, S), isle_names) }
df = pd.DataFrame(data, index=spp_names)
'''

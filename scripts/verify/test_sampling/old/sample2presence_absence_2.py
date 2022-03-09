# turn a data row into a presence-absence matrix

import numpy as np
import pandas as pd
import csv as csv # NOTE pandas can't handle uneven number of columns

from helpers import get_maximum_sample_ID, strings2numbers


# parameters
# ---

sample_ID = 2
suffix = '_2'

# where to save results
dir_results = '../../../results/verify/test_sampling/'


# read in desired record
# ---

fname = dir_results + 'samples' + suffix + '.csv'

if True: # get max sample_ID
    max_sample_ID = get_maximum_sample_ID(fname)


# NOTE: pandas can't deal with uneven columns
# df_in = pd.read_csv(fname, skiprows=[0], header=None)
# df_sub = df_in[df_in.iloc[:,0] == sample_ID]

with open(fname, newline='') as csvfile:

    reader = csv.reader(csvfile, delimiter=',')
    for row_strings in reader:
        if row_strings[0] == str(sample_ID):
            break

# check we did find it
assert row_strings[0] == str(sample_ID)

row = strings2numbers(row_strings)


# turn the data row into a presence-absence matrix
# ---

S = row[1]    # number of species
H = row[2]    # number of islands
K = row[3]    # number of niches

# no_spp_niche starts at:
idx = 5 + 3*H                       # [sam_ID, S, H, K, theta] is 5; T, J, and m for each island is 3*H
spp_in_niches = row[idx : idx+K]    # one entry for each of K niches

# presence-absence matrix starts after that
data_row = row[idx+K:]              # remainder of the row is the presence absence matrix

# create island names, species names
isle_names = [ 'simulated_' + str(h) for h in range(H) ]
spp_IDs = [ (k, i) for k, spp_in_niche in zip(range(K), spp_in_niches) for i in range(spp_in_niche) ]
spp_names = [ 'species_' + str(k) + '_' + str(i) for k, i in spp_IDs ]

# create the data frame
data = {isle_name: data_row[i:i+S] for i, isle_name in zip(range(0, S*H, S), isle_names) }
df = pd.DataFrame(data, index=spp_names)

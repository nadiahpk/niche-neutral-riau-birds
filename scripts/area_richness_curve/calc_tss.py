# calculate the total sum of squares (for calculating R^2)

import pandas as pd
import numpy as np

# parameters
# ---

# where to find the island area and richness data
fname_rich = '../../data/processed/island_richness.csv' # island_name,richness

# which island subsets to fit - correspond to file names
subsets = ['all',  'peninsula_only',  'riau_only',  'survey_only']
dirname_subsets = '../../data/processed/island_subsets/'


# loop over each island subset finding TSS
# ---

# get all richnesses
df = pd.read_csv(fname_rich)

TSSV = list()
for subset in subsets:

    # get the list of islands we want
    islands = list( pd.read_csv( dirname_subsets + subset + '.csv', header=0 )['island_name'] )

    # subset the relevant array of richness S
    S_true = np.array(df[df['island_name'].isin(islands)]['richness'])

    # calculate TSS and store
    S_mean = np.mean(S_true)
    TSS = sum( (S_true_i - S_mean)**2 for S_true_i in S_true )
    TSSV.append(TSS)

# write them to csv
# ---

df_out = pd.DataFrame( list(zip(subsets, TSSV)), columns=['subset_name', 'TSS_S'])
df_out.to_csv('../../results/area_richness_curve/TSS_richness.csv', index=False)

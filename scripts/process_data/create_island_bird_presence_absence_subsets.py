# create different subsets of islands that might be interesting to analyse

import pandas as pd


# parameters
# ---

# where the full matrix is
fname_matrix = '../../data/processed/island_bird_presence_absence.csv'

# which subsets to do
subsets = ['all',  'peninsula_only',  'riau_only',  'survey_only']
dirname_subsets = '../../data/processed/island_subsets/'

# where island area information is stored
fname_area = '../../data/processed/island_area.csv'

# where to send results
dir_out = '../../data/processed/island_subsets/'


# create island areas dictionary
# ---

df_area = pd.read_csv(fname_area)
island2area = dict(zip( df_area['island_name'].values, df_area['area_sq_km'] ))


# read in the full matrix
# ---

df_matrix = pd.read_csv(fname_matrix)

for subset in subsets:

    # get the list of islands we want
    islands = list( pd.read_csv( dirname_subsets + subset + '.csv', header=0 )['island_name'] )

    # order islands by area (largest to smallest)
    islands = sorted(islands, key = lambda v: -island2area[v])

    # subset df with only the islands of interest
    df_sub = df_matrix[ ['species_name'] + islands ]
    df_sub = df_sub[ df_sub.sum(axis=1) > 0 ]

    # write to file
    df_sub.to_csv(dir_out + 'island_bird_presence_absence_' + subset + '.csv', index=False)

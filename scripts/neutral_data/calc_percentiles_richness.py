# compare the observed species richnesses to the 95 percentiles of the neutral model

import pandas as pd
import numpy as np



# parameters
# ---

# which fit should we use for the parameter values? 
rho = 1700
subset_name = 'survey_only'

# where to put results
dir_results = '../../results/neutral_data/'

# where is processed information about islands?
dir_processed = '../../data/processed/'

# where to put results
dir_results = '../../results/neutral_data/'


# get area and real richness of each island
# ---

# get island name to richness
fname_islands = dir_processed + 'island_subsets/island_bird_presence_absence_' + subset_name + '.csv'
df_pamatrix = pd.read_csv(fname_islands)
island_names = list(df_pamatrix.columns[1:]) # fixed ordering of island names

richness = [ sum(df_pamatrix[island_name]) for island_name in island_names ]

# get island name to area
fname_area = dir_processed + 'island_area.csv'
df_area = pd.read_csv(fname_area)
df_area.set_index('island_name', inplace=True)
areas = [ df_area.loc[island_name]['area_sq_km'] for island_name in island_names ]


# get the species richness of each model sample
# ---

fname = dir_results + 'samples_' + subset_name + '_rho' + str(rho)  + '.csv'
df = pd.read_csv(fname)


# calculate the mean and percentiles of richness for each island
# ---

# create means, hi, and lo
mean_sampled_richness = [ np.mean(df['no_spp_isle_' + island_name]) for island_name in island_names ]
hi_sampled_richness = [ np.percentile(df['no_spp_isle_' + island_name], 97.5) for island_name in island_names ]
lo_sampled_richness = [ np.percentile(df['no_spp_isle_' + island_name], 2.5) for island_name in island_names ]


# check if true is within percentiles
# ---

check_within = [ 'yes' if S >= lo and S <= hi else 'no' for S, lo, hi in zip(richness, lo_sampled_richness, hi_sampled_richness) ]


# save information to file
# ---

# put it into a dataframe
df_out = pd.DataFrame(zip( island_names, areas, richness, check_within, mean_sampled_richness, lo_sampled_richness, hi_sampled_richness ),
        columns=['island_name', 'area_sq_km', 'S', 'true_S_in_bounds?', 'model_mean_S', 'model_lo_S', 'model_hi_S'])
df_out.to_csv( dir_results + 'percentiles_richness' + subset_name + '.csv', index=False)

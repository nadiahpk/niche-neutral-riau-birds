# write the island areas in standard form

import sys
sys.path.insert(0,'../../functions') # so I can import the common functions

from helpers import standardise_name

import pandas as pd


# parameters
# ---

# data source information from Keita
fname_in = '../../data/raw/island_data_source.csv'

# dataset also specifies the list of the islands of interest
fname_our = '../../data/processed/island_bird_presence_absence.csv'

# where to put output files
dir_out = '../../data/processed/'


# get the list of island names of interest
# ---

df_our = pd.read_csv(fname_our)
our_island_names = list(df_our.columns[1:])


# create standardised list of islands and data sources
# ---

df_in = pd.read_csv(fname_in)

data_src = df_in['Data Source'].values
std_data_src = [ standardise_name(s) for s in data_src ]

new_island_names = df_in['Island Name'].values
std_island_names = [ standardise_name(s) for s in new_island_names ]

# dictionary for looking up
island2src = dict(zip( std_island_names, std_data_src ))


# get data source for each of our islands of interest
# ---

our_data_src = [ island2src[island_name] if island_name in island2src else 'historical' for island_name in our_island_names ]


# write data sources
# ---

ll = list(zip( our_island_names, our_data_src ))
df_out = pd.DataFrame(ll, columns =['island_name', 'data_source'])
df_out.to_csv(dir_out + 'island_data_source.csv', index=False)

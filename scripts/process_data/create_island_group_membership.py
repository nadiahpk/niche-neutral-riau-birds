# write a csv file with each standardised island name and its corresponding standardised group name

import pandas as pd

import sys
sys.path.insert(0,'../../functions') # so I can import the common functions

from helpers import standardise_name


# parameters
# ---

# island group names from Keita
fname_in = '../../data/raw/island_properties.csv'

# dataset has headers as island names
fname_our = '../../data/processed/island_bird_presence_absence.csv'

# where to put output files
dir_out = '../../data/processed/'


# get the list of island names of interest
# ---

df_our = pd.read_csv(fname_our)
our_island_names = list(df_our.columns[1:])


# get Keita's island info
# ---

df_new = pd.read_csv(fname_in)
new_island_names = df_new['Island.Name'].values
std_island_names = [ standardise_name(s) for s in new_island_names ]

new_group_names = df_new['Island Group'].values
std_group_names = [ standardise_name(s) for s in new_group_names ]

# create a dictionary from it
island2group = dict(zip(std_island_names, std_group_names))


# get list of group names of interest to match island names
# ---

our_group_names = [ island2group[island_name] for island_name in our_island_names ]


# write island group membership file
# ---

ll = list(zip( our_island_names, our_group_names ))
df_out = pd.DataFrame(ll, columns = ['island_name', 'group_name'])
df_out.to_csv(dir_out + 'island_group_membership.csv', index=False)

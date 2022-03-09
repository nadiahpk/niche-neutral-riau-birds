# write the island areas in standard form
# check that all the islands in our data are in raw_data/island_area.csv

import pandas as pd
import sys
sys.path.insert(0,'../../functions') # so I can import the common functions

from helpers import standardise_name

# parameters
# ---

# island areas from Keita
fname_in = '../../data/raw/island_properties.csv'

# dataset also specifies the list of the islands of interest
fname_our = '../../data/processed/island_bird_presence_absence.csv'

# where to put output files
dir_out = '../../data/processed/'


# get the list of island names of interest
# ---

df_our = pd.read_csv(fname_our)
our_island_names = list(df_our.columns[1:])


# create standardised list of islands and their areas
# ---

df_in = pd.read_csv(fname_in)

areas = df_in['Present Day Area (m2)'].values

new_island_names = df_in['Island.Name'].values
std_island_names = [ standardise_name(s) for s in new_island_names ]

# dictionary for looking up
island2area = dict(zip( std_island_names, areas ))


# get area for each of our islands of interest
# ---

our_areas = [ island2area[island_name] for island_name in our_island_names ]


# write island areas
# ---

area_sq_km = [ area / 1e6 for area in our_areas ]
ll = list(zip( our_island_names, our_areas, area_sq_km ))
df_out = pd.DataFrame(ll, columns =['island_name', 'area_sq_m', 'area_sq_km'])
df_out.to_csv(dir_out + 'island_area.csv', index=False)

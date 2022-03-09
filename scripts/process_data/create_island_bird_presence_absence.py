# Convert the raw presence-absence data into a standardised form
# NOTE using the old database for the moment so I can check results, then I'll swap to the new one

import pandas as pd

import sys
sys.path.insert(0,'../../functions') # so I can import the common functions

from helpers import standardise_name



# parameters
# ---

# where the presence-absence data is stored
fname_in = '../../data/raw/island_bird_presence_absence_2021.csv'

# where to put the new data 
dir_out = '../../data/processed/'
fname_out = '../../data/processed/island_bird_presence_absence.csv'

# read in the data
# ---

df = pd.read_csv(fname_in, header=[0])

'''
Looks like this

                     Species Name            Scientific Name Endemic  Singapore  Bangka  Langkawi  Lingga  Bintan  Nias  ...  Sayap  Balik Kekup  Lalang
0          Brown-throated Sunbird      Anthreptes malacensis     NaN          1       1         1       1       1     1  ...      1            1       0
1             Collared Kingfisher        Todiramphus chloris     NaN          1       1         1       1       1     1  ...      1            1       0
2        Pink-necked Green Pigeon             Treron vernans     NaN          1       1         1       1       1     1  ...      0            0       0
3                  Ornate Sunbird           Cinnyris ornatus     NaN          1       1         1       1       1     1  ...      0            1       0
...
320                 Green Peafowl               Pavo muticus     NaN          0       0         0       0       0     0  ...      0            0       0
321       Orange-footed Scrubfowl       Megapodius reinwardt     NaN          0       0         0       0       0     0  ...      0            0       0
322       total number of species                        NaN     NaN        150     121       113     107     104   103  ...      6            5       5
'''


# tidy up
# ---

# drop totals in last row
df.drop(df.tail(1).index, inplace=True)

# drop scientific name and endemic status
df.drop(columns=['Scientific Name', 'Endemic'], inplace=True)

# remake the header standardised island names
old_header = list(df.columns)
pretty_island_names = old_header[1:]
standard_island_names = [ standardise_name(s) for s in pretty_island_names ]
new_header = ['species_name'] + standard_island_names
df.columns = new_header

# standardise the species names
pretty_species_names = list(df['species_name'])
standard_species_names = [ standardise_name(s) for s in pretty_species_names ]
df['species_name'] = standard_species_names


# write new presence-absence matrix
# ---

df.to_csv(fname_out, index=False)


# write mappings from standardised names to pretty names
# ---

df_out = pd.DataFrame(list(zip(standard_island_names, pretty_island_names)), columns = ['standard_name', 'pretty_name'])
df_out.to_csv(dir_out + 'standard2pretty_island_names.csv', index=False)

df_out = pd.DataFrame(list(zip(standard_species_names, pretty_species_names)), columns = ['standard_name', 'pretty_name'])
df_out.to_csv(dir_out + 'standard2pretty_species_names.csv', index=False)


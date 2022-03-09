# create island richness from sundas_presence_absence.csv

import pandas as pd
import numpy as np


# parameters
# ---

# where the Sundas presence absence data is stored
fname_in = '../../data/processed/island_bird_presence_absence.csv'

# where to put output files
dir_out = '../../data/processed/'


# read in the data
# ---

df = pd.read_csv(fname_in)

'''
Looks like this:
                     species_name  panggal_kecil  telor_kecil  paloi_kecil  telor_besar  sayap  ...  saya  penyenget  galang  bulan  batam  bintan
0             collared_kingfisher              1            1            0            1      1  ...     1          1       1      1      1       1
1          brown_throated_sunbird              1            0            0            0      1  ...     0          0       0      1      1       1
2            van_hasselts_sunbird              1            0            0            0      0  ...     0          0       0      1      1       1
...
321         streaked_wren_babbler              0            0            0            0      0  ...     0          0       0      0      0       0
322           white_bellied_munia              0            0            0            0      0  ...     0          0       0      0      0       0
323        moustached_hawk_cuckoo              0            0            0            0      0  ...     0          0       0      0      0       1
324           grey_headed_babbler              0            0            0            0      0  ...     0          0       0      0      0       0
'''

# get the island sums and write to a file
# ---

df_out = df.sum()[1:].reset_index(level=0, inplace=False) # sum makes the island names the index
df_out.columns = ['island_name', 'richness']
df_out.to_csv(dir_out + 'island_richness.csv', index=False)

# plot example sample to check

import pandas as pd
import matplotlib.pyplot as plt

# parameters
# ---

# which subset
subset = 'survey_only'
rho = 1700

# where are the samples and where to put results
dir_results = '../../results/neutral_data_fitm/'

# where to find the island area and richness data
fname_area = '../../data/processed/island_area.csv'     # island_name,area_sq_m,area_sq_km
fname_rich = '../../data/processed/island_richness.csv' # island_name,richness

# which island subsets info kept
dirname_subsets = '../../data/processed/island_subsets/'


# which islands are we doing
# ---

islands = list( pd.read_csv( dirname_subsets + subset + '.csv', header=0 )['island_name'] )


# get real data's area vs richness
# ---

# create a dataframe: island_name, area, richness
df_area = pd.read_csv(fname_area)
df_rich = pd.read_csv(fname_rich)
assert len(df_area) == len(df_rich), f'Number of islands in {fname_area} =/= {fname_rich}'
df_data = pd.merge(df_area, df_rich, on="island_name")

# subset to islands of interest 
df_data_sub = df_data[df_data['island_name'].isin(islands)]

A_tru = df_data_sub['area_sq_km'].values
S_tru = df_data_sub['richness'].values


# get the first sample's area vs richness
# ---

fname = dir_results + 'samples_' + subset + '_rho_' + str(rho)  + '.csv'
df = pd.read_csv(fname)
df_1 = df.iloc[0]

# get order of island names and areas
islands = [ s[2:] for s in df.columns if s[0:2] == 'J_' ]
isle2area = dict(zip(df_data_sub['island_name'], df_data_sub['area_sq_km'])) # dictionary to turn island names into island areas
A_sam = [ isle2area[island] for island in islands ]

# get the richness of each island
data_row_as_str = df_1['presence_absence_matrix_cols_isles_concatenated']
data_row = [ 1 if c == 'p' else 0 for c in data_row_as_str ]
S = df_1['S']
H = df_1['H']

S_sam = [ sum(data_row[i:i+S]) for i, island in zip( range(0, S*H, S), islands ) ]


# plot both for comparison
# ---

plt.scatter(A_tru, S_tru, alpha=0.7, label='data')
plt.scatter(A_sam, S_sam, alpha=0.7, label='sample')
plt.xlabel(r'area (km$^2$)')
plt.ylabel(r'number of species')
plt.xscale('log')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig(dir_results + 'sample_' + subset + '_rho_' + str(rho) + '.pdf')
plt.close()

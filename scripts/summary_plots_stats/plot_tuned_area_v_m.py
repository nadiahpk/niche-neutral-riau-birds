# plot how the fitted m for the tuned model varies with island size

import matplotlib.pyplot as plt
import pandas as pd


# parameters
# ---

# which parameter set and archipelagos to sample
subset_name = 'survey_only'
suffix = '_3'
rho = 1700

# where results are stored
dir_plot = '../../results/summary_stats/'
dir_m = '../../results/neutral_data_fitmK/'
fname_area = '../../data/processed/island_area.csv'


# get migration parameter on all islands
# ---

fname_params = dir_m + 'archipelago_params' + suffix + '.csv'
df = pd.read_csv(fname_params)
df_sub = df[(df['subset_name'] == subset_name) & (df['rho'] == rho)]
params = df_sub.iloc[0]
island_names = [ v[2:] for v in df_sub.columns if v[:2] == 'm_' ]

# migration probability
mV = [ params['m_' + island_name] for island_name in island_names ]


# get area of each island
# ---

df_area = pd.read_csv(fname_area)
areaV = [ df_area[df_area['island_name'] == island_name]['area_sq_km'].iloc[0] for island_name in island_names ]


# plot area vs. m
# ---

plt.scatter(areaV, mV, color='blue')

plt.xlabel(r'island area (km$^2$)', fontsize='xx-large')
plt.ylabel(r'migration rate $m$', fontsize='xx-large')
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
plt.savefig(dir_plot + 'tuned_area_v_m' + suffix + '.pdf')
plt.close()


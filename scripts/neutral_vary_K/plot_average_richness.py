# not possible to use the Chisholm model to get richness on each island because niches change size
# so use the samples instead

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# parameters
# ---

# where to save results
dir_results = '../../results/neutral_vary_K/'

# which one to plot
suffix = '_3'
# archipelago_ID = 1
archipelago_ID = 9

# number of islands NOTE being lazy
H = 16

# range of island carrying capacities (10**pwr km^2)
pwr_min = 2
pwr_max = 5

# range of carrying capacities
pwrV = np.linspace(pwr_min, pwr_max, H)
JV = [ 10**pwr for pwr in pwrV ]


# read in samples and find mean richnesses
# ---

fname = dir_results + 'samples' + suffix + '_archipelago_' + str(archipelago_ID) + '.csv'
df = pd.read_csv(fname)

# get the mean number of species on each island
SV = [ np.mean(df['no_spp_island_' + str(h)].values) for h in range(H) ]


# plot
# ---

plt.xscale('log')
plt.plot(JV, SV, color='black', alpha=0.3) # background curve
plt.scatter(JV, SV, color='black') # actual islands
plt.xlabel(r'carrying capacity (no. individuals)')
plt.ylabel(r'number of species')
plt.tight_layout()
plt.savefig(dir_results + 'average_richness' + suffix + '_archipelago_' + str(archipelago_ID) + '.pdf')
plt.close()


# save to csv
# ---

df_out = pd.DataFrame(zip(JV, SV), columns=['J', 'mean_S'])
df_out.to_csv( dir_results + 'average_richness' + suffix +'_archipelago' + str(archipelago_ID) + '.csv', index=False)

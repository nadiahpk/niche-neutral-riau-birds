# check the total number of species in the archipelago against the neutral samples

import pandas as pd
import matplotlib.pyplot as plt

#import sys
#sys.path.insert(0,'../../functions')



# parameters
# ---

# which fit should we use for the parameter values? 
rho = 1700
subset_name = 'survey_only'
#suffix = '_1'
suffix = '_3'
suffix = '_4'

# where to put results
dir_results = '../../results/neutral_data_fitmK/'

# where is processed information about islands?
dir_processed = '../../data/processed/'


# get richness of real archipelago
# ---

# get island name to richness
fname_real = dir_processed + 'island_subsets/island_bird_presence_absence_' + subset_name + '.csv'
df_real = pd.read_csv(fname_real)
richness_real = len(df_real.index) # count rows, which are species


# get richness of each sample
# ---

fname = dir_results + 'samples_archipelago' + suffix + '.csv'
df = pd.read_csv(fname)
richness_samples = df['S'].values


# plot a histogram and where the real data is in that
plt.hist(richness_samples, color='black', alpha=0.5, label='samples from neutral model')
plt.axvline(richness_real, color='blue', label='real data')
plt.xlabel('total species richness in archipelago')
plt.ylabel('frequency')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig(dir_results + 'archipelago_richness' + suffix + '.pdf')
plt.close()

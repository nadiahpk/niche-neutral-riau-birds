# check the total number of species in the archipelago against the neutral samples

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#import sys
#sys.path.insert(0,'../../functions')



# parameters
# ---

# which fit should we use for the parameter values? 
rho = 1700
subset_name = 'survey_only'
# subset_name = 'peninsula_only'

# where to put results
dir_results = '../../results/neutral_data/'

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

fname = dir_results + 'samples_' + subset_name + '_rho' + str(rho)  + '.csv'
df = pd.read_csv(fname)
richness_samples = df['S'].values

# print mean, percentiles to screen
print(f"mean is {np.mean(richness_samples)} with 95-percentile range {np.percentile(richness_samples, [2.5, 97.5])}")


# plot a histogram and where the real data is in that
plt.hist(richness_samples, color='blue', edgecolor='blue', alpha=0.7, label='niche-neutral model')
plt.axvline(richness_real, color='red', label='observed')
plt.xlabel('total species richness in archipelago', fontsize='xx-large')
plt.ylabel('frequency', fontsize='xx-large')
plt.legend(loc='best', fontsize='medium')
plt.tight_layout()
plt.savefig(dir_results + 'archipelago_richness_' + subset_name + '.pdf')
plt.close()

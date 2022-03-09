# plot summaries how of the nestedness depends on K

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import sem
import numpy as np

# parameters
# ---

# where's the results directory?
dir_results = '../../results/nestedness_rowpack_neutral_survey_vary_K/'

# which K values should we make a histogram for?
suffix = '_1'
KV = [1, 3, 5, 7]


# read in each sim9 results table to a dict
# ---

K2df = { K: pd.read_csv( dir_results + 'sim9_NODF' + suffix + '_K_' + str(K) + '.csv' ) for K in KV }


# create a new df_out to save statistics
# ---

df_out = pd.DataFrame(KV, columns=['K'])


# K vs raw nestedness
# ---

# plot
data_raw = [ K2df[K]['observed_NODF'].values for K in KV ]
plt.boxplot(data_raw)
plt.xticks(range(1,len(KV)+1), KV)
plt.xlabel(r'number of niches, $K$', fontsize='xx-large')
plt.ylabel(r'raw nestedness score, NODF', fontsize='xx-large')
plt.tight_layout()
plt.savefig(dir_results + 'summary_rawscore.pdf')
plt.close()

# save summary stats to df_out
df_out['mean_observed_NODF'] = [ np.mean(v) for v in data_raw ]
df_out['SE_observed_NODF'] = [ sem(v) for v in data_raw ]


# K vs SES NODF
# ---

# plot
data_ses = [ K2df[K]['standardised_effect_size'].values for K in KV ]
plt.boxplot(data_ses)
plt.xticks(range(1,len(KV)+1), KV)
plt.xlabel(r'number of niches, $K$')
plt.ylabel(r'SES NODF')
plt.tight_layout()
plt.savefig(dir_results + 'summary_SES.pdf')
plt.close()

# save summary stats to df_out
df_out['mean_standardised_effect_size'] = [ np.mean(v) for v in data_ses ]
df_out['SE_standardised_effect_size'] = [ sem(v) for v in data_ses ]


# write summary statistics to a csv
# ---

fname = dir_results + 'summary.csv'
df_out.to_csv(fname, index=False)

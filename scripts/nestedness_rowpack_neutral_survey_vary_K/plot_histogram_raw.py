# get a histogram of the raw metric scores across K values

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# parameters
# ---

# where's the results directory?
dir_results = '../../results/nestedness_rowpack_neutral_survey_vary_K/'

# which K values should we make a histogram for?
suffix = '_1'
KV = [1, 3, 5, 7]


# read in all the metric's info
# ---

raw_valsV = list()
for K in KV:

    fname = dir_results + 'sim9_NODF' + suffix + '_K_' + str(K) + '.csv'
    df = pd.read_csv(fname)

    # raw NODF values
    raw_vals = df['observed_NODF'].values
    raw_valsV.append(raw_vals)


# create bins
# ---

vv = 5
min_val = vv*(min( min( raw_vals ) for raw_vals in raw_valsV ) // vv)
max_val = vv*(1 + max( max( raw_vals ) for raw_vals in raw_valsV ) // vv)
bins = np.linspace(min_val, max_val, 11)

plt.hist(raw_valsV, bins, alpha=0.7, label=[ r'$K = ' + str(K) + r'$' for K in KV ])

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
for K, raw_vals, color in zip(KV, raw_valsV, colors):
    plt.axvline(np.mean(raw_vals), color=color)

plt.xlabel('raw NODF')
plt.ylabel('normalised frequency')
plt.legend(loc='best')

# save it
fname_plt = dir_results + 'histogram_raw' + suffix + '.pdf'
plt.savefig(fname_plt)
plt.close()



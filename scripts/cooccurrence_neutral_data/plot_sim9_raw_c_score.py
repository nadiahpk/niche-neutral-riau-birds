# plot a histogram of the raw C-scores for the simulated data, and compare it to the raw observed

import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np


# parameters
# ---

# which data subset to use
subset = 'survey_only'

# where the simulated data is and also where to save this plot
dir_simulated = '../../results/cooccurrence_neutral_data/'

# where the observed data is
dir_observed = '../../results/cooccurrence_data/'


# get raw for observed data
# ---

# read in all the results
df = pd.read_csv(dir_observed + 'sim9_c_score.csv')

# subset out the results we're interested in
df = df[df['subset_name'] == subset]

# get the value
raw_obs = df.iloc[0]['observed_c_score']


# get raw for simulated data
# ---

# read in all the results
df = pd.read_csv(dir_simulated + 'sim9_c_score.csv')

# subset out the results we're interested in
df = df[df['subset_name'] == subset]

# all raw
raw_all = df['observed_c_score'].values


# plot a histogram of raw
# ---

'''
# default min and max range for the raw
def_min = -2.5; def_max = 2.5

# find the min and max values from the experiment
exp_min = min(raw_all); exp_max = max(raw_all)

# round down and up to the nearest 0.5
exp_min_rnd = (int(exp_min / 0.5)-1)*.5
exp_max_rnd = (int(exp_max / 0.5)+1)*.5

# create bins
bin_min = min([def_min, exp_min_rnd])
bin_max = max([def_max, exp_max_rnd])
bins = np.arange( bin_min, bin_max, 0.1 ) # steps of 0.1
'''

# plot the values within and outside the sample range separately
plt.hist(raw_all, color='blue',   edgecolor='blue',    alpha=0.7, label='niche-neutral model')

# show where the observed value was
plt.axvline(raw_obs, color='red', label='observed')

plt.xlabel('raw C-Score')
plt.ylabel('frequency')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig(dir_simulated + 'sim9_raw_c_score_' + subset + '.pdf')
plt.close()

# plot a histogram of the SES C-scores for the simulated data, and compare it to the SES observed

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# parameters
# ---

# which data subset to use
subset = 'survey_only'

# where the simulated data is and also where to save this plot
dir_simulated = '../../results/cooccurrence_neutral_data_fitm/'

# where the observed data is
dir_observed = '../../results/cooccurrence_data/'


# get SES for observed data
# ---

# read in all the results
df = pd.read_csv(dir_observed + 'sim9_c_score.csv')

# subset out the results we're interested in
df = df[df['subset_name'] == subset]

# get the value of the standardised effect
SES_obs = df.iloc[0]['standardised_effect_size']


# get SES for simulated data
# ---

# read in all the results
df = pd.read_csv(dir_simulated + 'sim9_c_score.csv')

# subset out the results we're interested in
df = df[df['subset_name'] == subset]

# get the portion whose SES could be calculated (i.e., observed was within the sample range)
df_win = df[df['p_type'] == '==']

# and the portion whose SES was outside the sample range
df_out = df[df['p_type'] != '==']

# all SES
SES_all = df['standardised_effect_size'].values

# SES within and outside of the null distribution
SES_win = df_win['standardised_effect_size'].values
SES_out = df_out['standardised_effect_size'].values


# plot a histogram of SES
# ---

# default min and max range for the SES
def_min = -2.5; def_max = 2.5

# find the min and max values from the experiment
exp_min = min(SES_all); exp_max = max(SES_all)

# round down and up to the nearest 0.5
exp_min_rnd = (int(exp_min / 0.5)-1)*.5
exp_max_rnd = (int(exp_max / 0.5)+1)*.5

# create bins
bin_min = min([def_min, exp_min_rnd])
bin_max = max([def_max, exp_max_rnd])
bins = np.arange( bin_min, bin_max, 0.1 ) # steps of 0.1

# plot the values within and outside the sample range separately
plt.hist(SES_win, color='blue',   edgecolor='blue',    alpha=0.7, bins=bins, label='neutral model')
plt.hist(SES_out, color='orange', edgecolor='orange',  alpha=0.7, bins=bins, label='neutral model outliers')

# show the 95%-ile for a normal distribution and the 0
ninety_five = 1.96
plt.axvline(ninety_five, ls='dotted', color='black', alpha=0.7)
plt.axvline(-ninety_five, ls='dotted', color='black', alpha=0.7)
plt.axvline(0, ls='dotted', color='black', alpha=0.7)

# show where the observed value was
plt.axvline(SES_obs, color='red', label='observed')

plt.xlabel('SES C-Score')
plt.ylabel('frequency')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig(dir_simulated + 'sim9_c_score_' + subset + '.pdf')
plt.close()

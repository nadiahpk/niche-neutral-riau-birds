# get a histogram of the SES for the c-scores

import pandas as pd
import matplotlib.pyplot as plt


# parameters
# ---

# where's the results directory?
dir_results = '../../results/cooccurrence_neutral_area_vs_m/'

# which archipelago IDs should we make a histogram for?
suffix = '_3'
# archipelago_IDs = ['J1_m5', 'J3_m3', 'J3_m1']
archipelago_IDs = ['J3_m5']


# read in all the c-score info
# ---

fname = dir_results + 'sim9_c_score.csv'
df = pd.read_csv(fname)

for archipelago_ID in archipelago_IDs:

    # subset the data matching this ID
    df_sub = df[df['archipelago_ID'] == archipelago_ID]

    # C-score effect sizes
    effect_sizes = df_sub['standardised_effect_size'].values

    # make the histogram
    plt.hist(effect_sizes, density=True, label=r'$n = ' + str(len(effect_sizes)) + r'$')
    plt.axvline(0, color='black', ls='dotted')
    plt.xlabel('standardised effect size')
    plt.ylabel('normalised frequency')
    plt.title('scenario ' + archipelago_ID)
    plt.legend(loc='best')

    # save it
    fname_plt = dir_results + 'histogram_ses' + suffix + '_archipelago_' + archipelago_ID + '.pdf'
    plt.savefig(fname_plt)
    plt.close()


# get a histogram of the SES

import pandas as pd
import matplotlib.pyplot as plt


# parameters
# ---

# where's the results directory?
dir_results = '../../results/nestedness_rowpack_neutral_survey_vary_K/'

# which K values should we make a histogram for?
suffix = '_1'
KV = [1, 3, 5, 7]


# read in all the metric's info
# ---

for K in KV:

    fname = dir_results + 'sim9_NODF' + suffix + '_K_' + str(K) + '.csv'
    df = pd.read_csv(fname)

    # effect sizes
    effect_sizes = df['standardised_effect_size'].values

    # make the histogram
    plt.hist(effect_sizes, density=True, label=r'$n = ' + str(len(effect_sizes)) + r'$')
    plt.axvline(0, color='black', ls='dotted')
    plt.xlabel('standardised effect size')
    plt.ylabel('normalised frequency')
    plt.title(r'scenario $K = ' + str(K) + r'$')
    plt.legend(loc='best')

    # save it
    fname_plt = dir_results + 'histogram_ses' + suffix + '_K_' + str(K) + '.pdf'
    plt.savefig(fname_plt)
    plt.close()


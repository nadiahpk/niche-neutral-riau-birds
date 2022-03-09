# double check that my species-generator samples look how I want them to
# by just plotting the first-drawn sample

import pandas as pd
import matplotlib.pyplot as plt


# parameters
# ---

# where samples are stored and where the parameters are stored
dir_results = '../../results/neutral_survey_vary_K/'

# which parameter set / experiment?
suffix = '_1'

# which K values I looked at
KV = [1, 3, 5, 7]


# for each K value, read in the first sample and plot
# ---

for K in KV:

    # get the JV, the carrying capacity of each island in this archipelago
    fname_params = dir_results + 'archipelago_params' + suffix + '.csv'
    df_params = pd.read_csv(fname_params)
    row = df_params[(df_params['K'] == K) & (df_params['suffix'] == suffix) ]
    H = row.iloc[0]['H']
    JV = [ row.iloc[0][ 'J_' + str(h) ] for h in range(H) ]

    # get the number of species on each island for the first sample
    fname = dir_results + 'samples' + suffix + '_K_' + str(K) + '.csv'
    df = pd.read_csv(fname)
    row = df[df['sample_ID'] == 1 ]
    SV = [ row.iloc[0]['no_spp_island_' + str(h)] for h in range(H) ]

    # plot it
    plt.scatter(JV, SV, alpha=0.7, label=r'$K = ' + str(K) + r'$')


# decorate the plot and save
# ---

plt.legend(loc='best')
plt.xscale('log')
plt.xlabel(r'carrying capacity (num. individuals)')
plt.ylabel(r'number of species')
plt.tight_layout()
plt.savefig(dir_results + 'check_curves_samples' + suffix + '.pdf')
plt.close()

# plot histograms of species richness for each of our archipelagos

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# parameters
# ---

# where's the results directory?
dir_results = '../../results/neutral_vary_K/'

# which archipelago IDs should we make a histogram for?
suffix = '_3'
archipelago_IDs = [1, 8, 9, 10]


# plot a histogram of total archipelago species richness for each archipelago
# ---

for archipelago_ID in archipelago_IDs:

    # read in all samples info
    fname = dir_results + 'samples' + suffix + '_archipelago_' + str(archipelago_ID) + '.csv'
    df = pd.read_csv(fname)

    # richness
    Ss = df['S'].values
    meanSs = np.mean(Ss)

    # make the histogram
    plt.hist(Ss, density=True, label=r'$n = ' + str(len(Ss)) + r'$')
    plt.axvline(meanSs, color='black', ls='dashed')
    plt.xlabel('total archipelago species richness')
    plt.ylabel('normalised frequency')
    plt.title('scenario ' + str(archipelago_ID) + ', mean = {:.1f}'.format(meanSs))
    plt.legend(loc='best')

    # save it
    fname_plt = dir_results + 'histogram_richness' + suffix + '_archipelago_' + str(archipelago_ID) + '.pdf'
    plt.savefig(fname_plt)
    plt.close()




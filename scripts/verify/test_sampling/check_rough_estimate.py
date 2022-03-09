# a method for obtaining a rough estimate of species richness on islands with transient dynamics
# check it gives reasonable estimates 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# check a range of parameter values
# ---

# where to save results
dir_results = '../../../results/verify/test_sampling/'
suffix = '_rough_estimate'

J = 10000   # number of individuals on an island
theta = 30  # fundamental biodiversity number

# immigration rates
mV = [0.0005, 0.005, 0.01, 0.05, 0.1]

# time in generations since an island separated from the mainland
TV = [50, 100, 500, 1000, 5000, 100000]


# for each parameter combination, make rough estimate of species richness
# ---

E_SM = list() # a place to store species richnesses
for T in TV:

    E_SV = list()
    for m in mV:

        # find the expected number of founders using Chen & Chen's asymptotic approximation
        W = J*m / (1-m)
        alpha = T/2
        beta = (W-1)*T/(2*J)
        D = ( T*(W-1)/2 ) / ( alpha*(np.exp(beta)-1) + beta*np.exp(beta) )
        D = int(round(D))

        # expected number of ancestors given the number of founders
        E_C = D + sum( W / (W+i) for i in range(D,J) )
        E_C = int(round(E_C))

        # expected number of species given the number of ancestors
        E_S = sum( theta / (theta+i) for i in range(E_C) )

        # store
        E_SV.append(E_S)

    # store
    E_SM.append(E_SV)


# for each parameter combination, average the species richnesses from the samples
# ---

# read in the dataframe

fname = dir_results + 'samples' + suffix + '.csv'
df = pd.read_csv(fname)

S_SM = list() # a place to store species richnesses from samples for each T
for T in TV:

    # find the entries that match the T
    df_sub = df[ df['T_0'] == T ]

    # the islands are in the same order as mV (5 of them), so find the no species on each island
    SV = df_sub['no_spp_S'].values
    HV = df_sub['no_isles_H'].values
    data_row_as_strV = df_sub['presence_absence_matrix_cols_(isles)_concatenated'].values

    richness_islands = list()
    for S, H, data_row_as_str in zip(SV, HV, data_row_as_strV):

        isle_strings = [ data_row_as_str[i:i+S] for i in range(0, S*H, S) ]
        richnesses = [ this_isle.count('p') for this_isle in isle_strings ]
        richness_islands.append(richnesses)

    S_SV = np.mean(np.array(richness_islands), axis=0)
    S_SM.append(S_SV)


# plot it
# ---

colour_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

# add fake markes so I can label rough estimate versus sample
plt.plot([], [], color='black', alpha=0.5, label='rough estimate')
plt.scatter([], [], marker='o', color='black', alpha=0.5, label='average over 30 samples')


for T, E_SV, S_SV, colour in zip(TV, E_SM, S_SM, colour_cycle):

    plt.plot(mV, E_SV, color=colour, alpha=0.5, label = r'$T = ' + str(T) + '$')
    plt.scatter(mV, S_SV, marker='o', color=colour, alpha=0.5)

plt.legend(loc='best')
plt.xlabel('immigrant probability')
plt.ylabel('number of species')
plt.xscale('log')
plt.tight_layout()
plt.savefig(dir_results + 'check_rough_richness_estimate.pdf')
plt.close()

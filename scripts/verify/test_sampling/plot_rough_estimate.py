# a method for obtaining a rough estimate of species richness on islands with transient dynamics
# check it gives reasonable estimates 

import numpy as np
import matplotlib.pyplot as plt


# check a range of parameter values
# ---

# where to save results
dir_results = '../../../results/verify/test_sampling/'

J = 10000   # number of individuals on an island
theta = 30  # fundamental biodiversity number

# immigration rates
mV = [0.0005, 0.005, 0.01, 0.05, 0.1]

# time in generations since an island separated from the mainland
TV = [50, 100, 500, 1000, 5000, 100000]

# for now, choose some NOTE
#mV = [0.01]
TV = [50]


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


# plot it
# ---

for T, E_SV in zip(TV, E_SM):

    plt.plot(mV, E_SV, '-o', alpha=0.7, label = r'$m = ' + str(T) + '$')

plt.legend(loc='best')
plt.xlabel('immigrant probability')
plt.ylabel('average no. species')
#plt.xscale('log')
plt.tight_layout()
plt.savefig(dir_results + 'plot_rough_richness_estimate.pdf')
plt.close()

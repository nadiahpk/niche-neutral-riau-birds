# create one example of co-occurrence data and verify that it matches the Chisholm formula

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import digamma
import pandas as pd


np.random.seed(42)

# parameters
# ---

'''
suffix = '_1'

# choose parameter values similar to the survey example
rho = 1259          # individuals per km^2
K = 5               # number of niches
theta = 8           # fundamental biodiversity number across all niches
m = 0.03            # immigration parameter
H = 10              # number of islands

# range of area of each island (10**pwr km^2)
pwr_min = -3; pwr_max = 2;
'''

suffix = '_2'

# choose parameter values similar to the survey example
rho = 1259          # individuals per km^2
K = 9               # number of niches
theta = 30          # fundamental biodiversity number across all niches
m = 0.0002          # immigration parameter
H = 10              # number of islands

# range of area of each island (10**pwr km^2)
pwr_min = -2; pwr_max = 2;

# where to save results
dir_results = '../../../results/verify/sampling_matches_Chisholm/'


# create JV, number of individuals on each island
# ---

# create island areas
pwrV = np.linspace(pwr_min, pwr_max, H)
AV = [ 10**pwr for pwr in pwrV ]

thetak = theta/K        # fundamental biodiversity number per niche (assumes equal niches)
JV = [ A*rho for A in AV ]


# create Jkh, the number of individuals in niche k on island h
# ---

J = list()
for k in range(K):

    J.append([])

    for h in range(H):

        A = AV[h]                   # area of island h
        Jkh_float = A * rho / K     # number of individuals that can fit

        # treat the fractional component of Jkh_float probabilistically
        Jkh, prob = (int(Jkh_float // 1), Jkh_float%1)
        if np.random.rand() < prob:
            Jkh += 1

        J[k].append(Jkh)


# create mV, constant for now but I'd like to vary it in the future
# ---

mV = [m]*H
# mV = [ 0.03, 0.01, 0.03, 0.05, 0.06, 0.02, 0.01, 0.02, 0.8, 0.04]


# create a sample using Etienne's sequential sampling method
# ---

# rows are niches, index is species ID and value is the no. of times that species has immigrated
ancestors = list() # stores a_k
community = list() # stores n_{k,h,i}

# count how many ancestors sampled from each niche
no_ancestors = [ 0 for k in range(K) ] # l_k

for k in range(K): # for each niche

    ancestors.append([])
    community.append([])

    for h in range(H): # for each island

        community[k].append([ 0 for a_k in range(len(ancestors[k])) ])
        
        Jkh = J[k][h]

        # deal with special case, if Jkh = 1
        # necessary bc if Jkh = 1, then I = 0, then I/(I+j) = nan
        if Jkh == 1:

            # has to be a new immigrant
            if np.random.rand() < thetak / ( thetak + no_ancestors[k] ):

                # the immigrant was a new species
                ancestors[k].append(1)
                community[k][h].append(1)

            else:

                # the immigrant was a species we've seen before
                prob_i = [ ai / no_ancestors[k] for ai in ancestors[k] ] 
                i_star = np.random.choice( range(len(prob_i)), 1, p = prob_i )[0]
                ancestors[k][i_star] += 1
                community[k][h][i_star] += 1

            # increment the ancestors counter
            no_ancestors[k] += 1

        else:

            # Etienne's immigration parameter
            I = mV[h] * (Jkh-1) / (1-mV[h])

            # sample individuals
            for j in range(Jkh):

                if (np.random.rand() < I / (I+j)):

                    # we have drawn an immigrant

                    if np.random.rand() < thetak / ( thetak + no_ancestors[k] ):

                        # the immigrant was a new species
                        ancestors[k].append(1)
                        community[k][h].append(1)

                    else:

                        # the immigrant was a species we've seen before
                        prob_i = [ ai / no_ancestors[k] for ai in ancestors[k] ]
                        i_star = np.random.choice( range(len(prob_i)), 1, p = prob_i )[0]
                        ancestors[k][i_star] += 1
                        community[k][h][i_star] += 1

                    # increment the ancestors counter
                    no_ancestors[k] += 1

                else:

                    # it's a birth-death
                    prob_i = [ ni / j for ni in community[k][h] ]
                    i_star = np.random.choice( range(len(prob_i)), 1, p = prob_i )[0]
                    community[k][h][i_star] += 1


# create a presence-absence matrix of the data
# ---

isle_names = [ 'simulated_' + str(h) for h in range(H) ]
spp_IDs = [ (k, i) for k in range(K) for i in range(len(ancestors[k])) ]
spp_names = [ 'species_' + str(k) + '_' + str(i) for k, i in spp_IDs ]
S = len(spp_IDs)

data = { isle_name: [0]*S for isle_name in isle_names }
for k in range(K):
    for h in range(H):
        isle_name = 'simulated_' + str(h)
        for i, ni in enumerate(community[k][h]):
            if ni > 0:
                spp_idx = spp_IDs.index( (k, i) )
                data[isle_name][spp_idx] += 1

df = pd.DataFrame(data, index=spp_names)
df.to_csv(dir_results + 'example_1.csv', index=True)


# count the number of species on each island
# ---

'''
# use this if you don't make presence-absence matrix above

no_sppV = [0]*H
for k in range(K):
    for h in range(H):
        no_sppV[h] += sum( 1 for ni in community[k][h] if ni > 0 )
'''

no_sppV = df.sum(axis=0).values


# plot species area relationship for verifying correctness
# ---

plt.xscale('log')

# do the sample
plt.scatter(AV, no_sppV, alpha=0.7, color='black', label='sample')

# do the theoretical curve
A_pwr_min = np.log10(AV[0]); A_pwr_max = np.log10(AV[-1])
A_pwrV = np.linspace( A_pwr_min, A_pwr_max, 100 )
AV = 10**A_pwrV
JV = [ A*rho for A in AV ]

S_fnc = lambda theta, K, J, m: theta*( digamma( theta/K + ((J-1)*m/(1-m))*( digamma(((J-1)*m/(1-m))+J) - digamma(((J-1)*m/(1-m))) ) ) - digamma( theta/K ) )

SV = [ S_fnc(theta, K, J/K, m) for J in JV ]

plt.plot(AV, SV, color='blue', label='theoretical curve')

# plot critical A
A_crit = theta*(1-m)*(np.exp(K/theta)-1) / ( m*rho*np.log(1/m) )

# decorations
plt.legend(loc='best')
plt.axvline(A_crit, color='black', ls='dashed')
plt.xlabel(r'area (km$^2$)')
plt.ylabel(r'number of species')
plt.tight_layout()
plt.savefig(dir_results + 'example' + suffix + '.pdf')
plt.close()

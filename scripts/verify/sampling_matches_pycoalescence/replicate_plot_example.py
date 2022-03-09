# use the species generator approach to try to replicate 
# ../../../results/verify/sampling_matches_pycoalescence/plot_example_10000_eventrate_5.pdf
# creates fig_name = 'replicate_plot_example_10000_eventrate_' + str(int(1e4*m)) + '.pdf'

import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('../../../functions/')

from my_functions import sad2octaves

np.random.seed(42)


# parameters
# ---

dir_results = '../../../results/verify/sampling_matches_pycoalescence/'

m = 0.0005 # also called "event_rate", it's the chance of immigration
J = 10000  # number of individuals = population size
theta = 30 # Fisher's alpha for the metacommunity, equivalent to theta as used in the other generators

max_genV = [50, 100, 500, 1000, 5000]

max_pwr = 14 # the upper-most octave boundary used for plotting
reps = 100 # number of samples over which the Preston octave plot is averaged

# NOTE debugging
# max_genV = [100]
# reps = 1

# secondary parameters
# ---

W = J*m / (1-m) # Watterson's theta for the local community

octave_barriers = [ 2**(i) for i in range(max_pwr+1) ] # actually the octave barriers
# labs = [ str(octaves[idx-1]) + '-' + str(octaves[idx]) for idx in range(1, max_pwr+1) ] # octave labels for plot


# go through each max_gen, sampling a Preston plot, and take the average

mean_spp_per_octaveV = list()
for max_gen in max_genV:

    # find the expected number of old lineages using Chen & Chen's asymptotic approximation
    # ---

    Chens_alpha = max_gen/2
    Chens_beta = (W-1)*max_gen/(2*J)
    k = ( max_gen*(W-1)/2 ) / ( Chens_alpha*(np.exp(Chens_beta)-1) + Chens_beta*np.exp(Chens_beta) )

    # round it
    k = int(round(k))


    # double sampling
    # ---

    spp_per_octaveV = list() # count the number of species falling within each octave
    for rep in range(reps):

        # sample a species abundance distribution
        # ---

        community = list()  # indices are species and values are abundances
        ancestors = list()  # indices are species and values are no. times they've been drawn from metacommunity
        a = 0 # ancestors counter

        # first, sample the individuals linking to the old lineages from the metacommunity
        for j in range(k):

            if np.random.rand() < theta / (theta+j):

                # add a new individual of a new species
                community.append(1)
                ancestors.append(1)

            else:

                # add one new individual of an already-sampled old species
                old = np.random.choice( range(len(ancestors)), 1, p=[i/a for i in ancestors] )[0]
                community[old] += 1
                ancestors[old] += 1

            # added an ancestor (an immigrant)
            a += 1

        # j = k # meaning, I have sampled j individuals from the metacommunity

        # now sample the remaining individuals

        # In Etienne's algorithm, I / (I+j) 
        # where I = m*(Js-1)/(1-m) where Js is individuals/niche and m is fitted immigration rate
        I = m*(J-1)/(1-m)
        for i in range(k, J):

            if np.random.rand() < I / (I+i):

                # add a new individual from the metacommunity
                
                # In Etienne's algorithm, theta / (theta+a) where 
                # theta = theta_orig/K where theta_orig is fitted fundamental biodiversity
                if np.random.rand() < theta / (theta+a): 

                    # add a new individual of a new species
                    community.append(1)
                    ancestors.append(1)

                else:

                    # add one new individual of an already-sampled old species
                    old = np.random.choice( range(len(ancestors)), 1, p=[i/a for i in ancestors] )[0]
                    community[old] += 1
                    ancestors[old] += 1

                # increment a to indicate how many ancestors we've drawn, how many immigrants have been drawn from the metacommunity
                a += 1

            else:

                # add one new individual of an already-sampled old species
                old = np.random.choice( range(len(community)), 1, p=[c/i for c in community] )[0]
                community[old] += 1


        # get octaves and store it
        # ---

        spp_per_octave = list() # count the number of species falling within each octave
        for idx in range(1, max_pwr+1):

            # octave bounds
            oct_hi = octave_barriers[idx]; oct_lo = octave_barriers[idx-1];

            # count how many species fall in this octave's abundance range
            # Preston style Octave counting -- abundances on the octave barrier are split between the two octaves
            no_spp = sum( 1 for abund in community if (abund > oct_lo) and (abund < oct_hi) ) + \
                0.5 * (community.count(oct_hi) + community.count(oct_lo))

            spp_per_octave.append(no_spp)


        # store it
        spp_per_octaveV.append(spp_per_octave)


    # take the mean Preston octave distn and store it
    # ---

    mean_spp_per_octave = np.mean(spp_per_octaveV, axis=0)
    mean_spp_per_octaveV.append( mean_spp_per_octave )


# plot them
# ---

fig_name = dir_results + 'replicate_plot_example_10000_eventrate_' + str(int(1e4*m)) + '.pdf'

# plot the metacommunity

x = J / (theta + J)
sad_meta = [ theta*x**j / j for j in range(1,J+1) ] # expected distribution
spp_per_octave_meta, labs = sad2octaves(sad_meta, octave_barriers)
plt.plot(range(max_pwr), spp_per_octave_meta, ls='dotted', color='red', alpha=0.7, label='metacommunity')

# plot each sample mean

for max_gen, mean_spp_per_octave in zip(max_genV, mean_spp_per_octaveV):

    plt.plot(range(max_pwr), mean_spp_per_octave, '-o', label = r'max gen = ' + str(max_gen))

# decorate

plt.xticks(range(max_pwr), labs, rotation=90)
plt.xlabel('abundance octaves (Preston style)')
plt.ylabel('number of species')
plt.ylim( (-1,24) ) # just to match previous
plt.legend(loc='best')
plt.tight_layout()
plt.savefig(fig_name)
plt.close()

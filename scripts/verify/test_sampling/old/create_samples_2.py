# for checking the rough estimate

import os
import numpy as np
import matplotlib.pyplot as plt
# from scipy.special import digamma
# import pandas as pd
import csv

from species_generator_funcs import draw_sample_species_generator, calculate_D, draw_J
from helpers import get_maximum_sample_ID


# parameters
# ---

no_samples = 10 # number of samples per parameter combination

# where to save results
dir_results = '../../../results/verify/test_sampling/'
suffix = '_2'

# choose parameter values for convenience
K = 1               # number of niches
theta = 30          # fundamental biodiversity number across all niches

# define the characteristics of each island, also for convenience
mV = [0.0005, 0.005, 0.01, 0.05, 0.1]
JV = [1e4]*5
# TM = [[50]*5]
TM = [[100]*5, [500]*5]


# secondary parameters
# ---

H = len(mV)
isle_names = [ 'simulated_' + str(h) for h in range(H) ]


# write header of the csv or, if csv exists, get last sample_ID
# ---

fname = dir_results + 'samples' + suffix + '.csv'

if not os.path.isfile(fname):

    sample_ID = 0

    # write column names
    column_names  = [ 'sample_ID', 'no_spp_S', 'no_isles_H', 'K', 'theta' ]
    column_names += [ 'T_' + str(h) for h in range(H) ]
    column_names += [ 'J_' + str(h) for h in range(H) ]
    column_names += [ 'm_' + str(h) for h in range(H) ]
    column_names += [ 'no_spp_niche_' + str(k) for k in range(K) ]
    column_names += [ 'presence_absence_on_islands_concatenated' ]

    with open(fname, 'w', newline='') as csvfile:

        writer = csv.writer(csvfile, lineterminator = os.linesep)
        writer.writerow(column_names)

else:

    # get maximum sample_ID
    sample_ID = get_maximum_sample_ID(fname)



# only need to do this once because JV are all large

# create J[k,h], the number of individuals in niche k on island h
J = draw_J(K, JV) 

for TV in TM:

    # create D[k,h], the number of founding individuals in each niche k on island h
    D = calculate_D(mV, TV, J)


    # draw samples
    # ---

    for sample_ID in range(sample_ID+1,sample_ID+1+no_samples):

        # draw one sample archipelago
        # ---

        # create a sample using my species generator
        ancestors, community = draw_sample_species_generator(theta, mV, J, D)


        # extract information about the simulated archipelago
        # ---

        spp_in_niches = [ len(ak) for ak in ancestors ]  # number of species in each niche
        S = sum(spp_in_niches)                           # total no. spp in archipelago

        # create names for each island and each species
        spp_IDs = [ (k, i) for k in range(K) for i in range(len(ancestors[k])) ]
        spp_names = [ 'species_' + str(k) + '_' + str(i) for k, i in spp_IDs ]


        # put data into a dictionary
        # data = { island names: [1s and 0s for presence and absence of species in order in spp_IDs] }

        data = { isle_name: [0]*S for isle_name in isle_names }
        for k in range(K):
            for h in range(H):
                isle_name = 'simulated_' + str(h)
                for i, ni in enumerate(community[k][h]):
                    if ni > 0:
                        spp_idx = spp_IDs.index( (k, i) )
                        data[isle_name][spp_idx] += 1


        # turn it into a flat row so it can be written to a csv
        data_row = list()
        for isle_name in isle_names:
            data_row += data[isle_name]

        # to reverse this process
        # data2 = {isle_name: data_row[i:i+S] for i, isle_name in zip(range(0, S*H, S), isle_names) }


        # write a row to a csv
        # ---

        record  = [sample_ID, S, H, K, theta] 
        record += [ T for T in TV ] 
        record += [ J for J in JV ] 
        record += [ m for m in mV ] 
        record += [ spp_in_niche for spp_in_niche in spp_in_niches ] 
        record += data_row

        with open(fname, 'a', newline='') as csvfile:

            writer = csv.writer(csvfile, lineterminator = os.linesep)
            writer.writerow(record)

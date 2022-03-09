# a species generator that handles multiple islands + transient dynamics
# small example where I put the entire matrix into one string

import os
import numpy as np
import matplotlib.pyplot as plt
# from scipy.special import digamma
import pandas as pd
import csv

from species_generator_funcs import draw_sample_species_generator, calculate_D, draw_J


# parameters
# ---

# where to save results
dir_results = '../../../results/verify/test_sampling/'
suffix = '_3'

# choose parameter values for convenience
K = 5               # number of niches
theta = 8           # fundamental biodiversity number across all niches
m = 0.0001          # immigration rate

# define the characteristics of each island, also for convenience
TV = [  np.inf, np.inf,   6,      6,    10 ]
JV = [  1e2,    1e2,    1e2,    1e2,    1e2 ]
mV = [  m,      m,      m,      m,      m]


# secondary parameters
# ---

H = len(JV)
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
    column_names += [ 'presence_absence_matrix_cols_(isles)_concatenated' ]

    with open(fname, 'w', newline='') as csvfile:

        writer = csv.writer(csvfile, lineterminator = os.linesep)
        writer.writerow(column_names)

else:

    df = pd.read_csv(fname, skiprows=[0], header=None) # NOTE: has issues here because of uneven number of columns
    sample_ID = int(max(df.iloc[:,0].values))


# draw samples
# ---

sample_ID += 1
if True: # TODO - make into a loop


    # draw one sample archipelago
    # ---

    # create J[k,h], the number of individuals in niche k on island h
    J = draw_J(K, JV)

    # create D[k,h], the number of founding individuals in each niche k on island h
    D = calculate_D(mV, TV, J)

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
    record += [ ''.join([ 'p' if v == 1 else 'a' for v in data_row ]) ]

    with open(fname, 'a', newline='') as csvfile:

        writer = csv.writer(csvfile, lineterminator = os.linesep)
        writer.writerow(record)

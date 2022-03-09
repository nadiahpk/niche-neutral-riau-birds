# create samples of the presence-absence matrix using the hypothetical archipelagos in this experiment

import pandas as pd
import os
import csv

import sys
sys.path.insert(0,'../../functions')

from my_functions import draw_J_from_float, draw_sample_species_generator_general, calculate_D


# parameters
# ---

# which parameter set and archipelagos to sample
suffix = '_2'

# where is the file storing parameter values and where to save results
dir_results = '../../results/neutral_vary_JK/'

# how many samples to take of each archipelago
no_samples = 20

print('doing no_samples = ' + str(no_samples))


# get parameter values common to all islands
# ---

fname_params = dir_results + 'archipelago_params' + suffix + '.csv'
df = pd.read_csv(fname_params)
df_sub = df[df['suffix'] == suffix]
params = df_sub.iloc[0]

H = params['H']
theta_k = params['theta_k']
T = params['T']
K = params['K']
m = params['m']

mV = [m]*H
TV = [T]*H
thetakV = [theta_k]*K


J_f = list()
for k in range(K):

    Jk = list()

    for h in range(H):

        Jkh = params['J_' + str(k) + '_' + str(h)]
        Jk.append(Jkh)

    J_f.append(Jk)


# write header of the csv for results, and get sample_ID if some samples already taken
# ---

fname = dir_results + 'samples_archipelago' + str(suffix) + '.csv'

if not os.path.isfile(fname):

    # write column names 
    # [ sample_ID, S, H, K, no_spp_niche_0..K, no_spp_island_0..H, presence_absence_matrix ]
    column_names  = [ 'sample_ID', 'S', 'H', 'K']
    column_names += [ 'no_spp_niche_' + str(k) for k in range(K) ]
    column_names += [ 'no_spp_isle_' + str(h) for h in range(H) ]
    column_names += [ 'presence_absence_matrix_cols_isles_concatenated' ]

    with open(fname, 'w', newline='') as csvfile:

        writer = csv.writer(csvfile, lineterminator = os.linesep)
        writer.writerow(column_names)

    sample_ID = 0

else:

    df_already = pd.read_csv(fname)
    sample_IDs_already = df_already['sample_ID'].values
    sample_ID = max(sample_IDs_already)


# draw sample archipelagos
# ---

for sam in range(no_samples):

    sample_ID += 1
    print('sample: ' + str(sample_ID))

    # draw J[k,h], the integer number of individuals in niche k on island h
    J = draw_J_from_float(J_f)

    # create D[k,h], the number of founding individuals in each niche k on island h
    D = calculate_D(mV, TV, J)

    # create a sample using my species generator
    ancestors, community = draw_sample_species_generator_general(thetakV, mV, J, D)

    # extract information about the simulated archipelago

    # number of species on each island
    spp_in_isles = [ sum(sum( 1 if i > 0 else 0 for i in ls ) for ls in v ) for v in zip(*community) ]

    # number of species in each niche
    spp_in_niches = [ len(ak) for ak in ancestors ] 

    # total no. spp in archipelago
    S = sum(spp_in_niches)

    # create the data dictionary
    # data = { island index: [1s and 0s for presence and absence of species in order in spp_IDs] }

    spp_IDs = [ (k, i) for k in range(K) for i in range(len(ancestors[k])) ] # names and index each species
    data = { h: [0]*S for h in range(H) }

    for k in range(K):
        for h in range(H):
            for i, ni in enumerate(community[k][h]):
                if ni > 0:
                    spp_idx = spp_IDs.index( (k, i) )
                    data[h][spp_idx] += 1

    # turn it into a flat row so it can be written to a csv

    data_row = list()
    for h in range(H):
        data_row += data[h]
    # to reverse this process: data2 = {isle_name: data_row[i:i+S] for i, isle_name in zip(range(0, S*H, S), isle_names) }

    # write a row to a csv
    # [ sample_ID, S, H, K, no_spp_niche_0..K, no_spp_island_0..H, presence_absence_matrix ]

    record  = [sample_ID, S, H, K]
    record += [ spp_in_niche for spp_in_niche in spp_in_niches ]
    record += [ spp_in_isle for spp_in_isle in spp_in_isles ]
    record += [ ''.join([ 'p' if v == 1 else 'a' for v in data_row ]) ]

    with open(fname, 'a', newline='') as csvfile:

        writer = csv.writer(csvfile, lineterminator = os.linesep)
        writer.writerow(record)

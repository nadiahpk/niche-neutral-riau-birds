# create samples of the presence-absence matrix using the hypothetical archipelagos in this experiment

import pandas as pd
import os
import csv

import sys
sys.path.insert(0,'../../functions')

from my_functions import draw_J, calculate_D, draw_sample_species_generator


# parameters
# ---

# how many samples to take of each archipelago
no_samples = 30

# samples distinguished by their K values - which K value?
KV = [1, 3, 5, 7]

# which parameter set / experiment?
suffix = '_1'

# where is the file storing parameter values and where to save results
dir_results = '../../results/neutral_survey_vary_K/'


# draw no_samples or archipelagos for each K in KV
# ---

for K in KV:

    print('doing K = ' + str(K))

    # get parameter values
    # ---

    fname_params = dir_results + 'archipelago_params' + suffix + '.csv'
    df_params = pd.read_csv(fname_params)
    row = df_params[(df_params['K'] == K) & (df_params['suffix'] == suffix) ]

    theta = row.iloc[0]['theta']
    H = row.iloc[0]['H']
    T = row.iloc[0]['T']; TV = [T]*H
    m = row.iloc[0]['m']; mV = [m]*H
    JV = [ row.iloc[0][ 'J_' + str(h) ] for h in range(H) ]


    # write header of the csv for results, and get sample_ID if some samples already taken
    # ---

    fname = dir_results + 'samples' + suffix + '_K_' + str(K) + '.csv'

    if not os.path.isfile(fname):

        # write column names 
        column_names  = [ 'K', 'sample_ID', 'S', 'H']
        column_names += [ 'no_spp_niche_' + str(k) for k in range(K) ]
        column_names += [ 'no_spp_island_' + str(h) for h in range(H) ]
        column_names += [ 'presence_absence_matrix_cols_isles_concatenated' ]

        with open(fname, 'w', newline='') as csvfile:

            writer = csv.writer(csvfile, lineterminator = os.linesep)
            writer.writerow(column_names)

        sample_ID = 0

    else:

        df_already = pd.read_csv(fname)
        sample_IDs_already = df_already[df_already['K'] == K]['sample_ID'].values
        if len(sample_IDs_already) == 0:
            sample_ID = 0
        else:
            sample_ID = max(sample_IDs_already)


    # take each sample
    # ---

    for sam in range(no_samples):

        sample_ID += 1
        print('sample: ' + str(sample_ID))


        # draw one sample archipelago
        # ---

        # draw J[k,h], the number of individuals in niche k on island h
        J = draw_J(K, JV)

        # create D[k,h], the number of founding individuals in each niche k on island h
        D = calculate_D(mV, TV, J)

        # create a sample using my species generator
        ancestors, community = draw_sample_species_generator(theta, mV, J, D)


        # extract information about the simulated archipelago
        # ---

        # number of species on each island
        spp_in_isles = [ sum(sum( 1 if i > 0 else 0 for i in ls ) for ls in v ) for v in zip(*community) ]

        # number of species in each niche
        spp_in_niches = [ len(ak) for ak in ancestors ] 

        # total no. spp in archipelago
        S = sum(spp_in_niches)


        # create the data dictionary
        # ---

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


        # write this row the csv
        # ---

        # columns of csv are: ['K', 'sample_ID', 'S', 'H', 'no_spp_niche_0', .. ,'no_spp_niche_K-1', 
        #                      'no_spp_island_0', .., 'no_spp_island_H-1', 'presence_absence_matrix_cols_isles_concatenated']

        record  = [K, sample_ID, S, H]
        record += [ spp_in_niche for spp_in_niche in spp_in_niches ]
        record += [ spp_in_isle for spp_in_isle in spp_in_isles ]
        record += [ ''.join([ 'p' if v == 1 else 'a' for v in data_row ]) ]

        with open(fname, 'a', newline='') as csvfile:

            writer = csv.writer(csvfile, lineterminator = os.linesep)
            writer.writerow(record)

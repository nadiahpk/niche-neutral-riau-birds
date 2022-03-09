# create samples of the presence-absence matrix using the parameters fitted to Keita's data

import pandas as pd
#import numpy as np
import os
import csv

import sys
sys.path.insert(0,'../../functions')

from my_functions import draw_sample_species_generator, calculate_D, draw_J


# parameters
# ---

no_samples = 60 # number of samples to draw using the spp generator

# where are the parameter values from when the Chisholm model was fitted to Keita's data
fname_fit = '../../results/neutral_data_fitm/archipelago_params.csv'

# which fit should we use for the parameter values? 
rho = 1700
subset_name = 'survey_only'

# where is processed information about islands?
dir_processed = '../../data/processed/'

# where to put results
dir_results = '../../results/neutral_data_fitm/'


# get information about the islands used for this subset
# ---

# get names of islands
fname_islands = dir_processed + 'island_subsets/' + subset_name + '.csv'
island_names = list( pd.read_csv( fname_islands, header=0 )['island_name'] )

# get their areas
fname_area = dir_processed + 'island_area.csv'
df_area = pd.read_csv(fname_area)
df_area.set_index('island_name', inplace=True)
areas = [ df_area.loc[island_name]['area_sq_km'] for island_name in island_names ]


# get fitted parameter values
# ---

df_fit = pd.read_csv(fname_fit)
row = df_fit[(df_fit['subset_name'] == subset_name) & (df_fit['rho'] == rho) ]
K = row.iloc[0]['K']
theta = row.iloc[0]['theta']
T = row.iloc[0]['T']
H = row.iloc[0]['H']
TV = [T]*H
mV = [ row.iloc[0]['m_' + island_name] for island_name in island_names ]
JV = [ row.iloc[0]['J_' + island_name] for island_name in island_names ]


# write header of the csv or, if csv exists, get last sample_ID
# ---

fname = dir_results + 'samples_' + subset_name + '_rho_' + str(rho)  + '.csv'

if not os.path.isfile(fname):

    sample_ID = 0

    # write column names 
    column_names  = [ 'sample_ID', 'S', 'H', 'K', 'theta', 'T' ]
    column_names += [ 'J_' + island_name for island_name in island_names ]
    column_names += [ 'm_' + island_name for island_name in island_names ]
    column_names += [ 'no_spp_niche_' + str(k) for k in range(K) ]
    column_names += [ 'presence_absence_matrix_cols_isles_concatenated' ]

    with open(fname, 'w', newline='') as csvfile:

        writer = csv.writer(csvfile, lineterminator = os.linesep)
        writer.writerow(column_names)

else:

    df = pd.read_csv(fname)
    sample_ID = max(df['sample_ID'].values)


# sample archipelagos using the species generator
# ---

for sample_ID in range(sample_ID+1,sample_ID+1+no_samples):

    print('doing sample ' + str(sample_ID))

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

    data = { island_name: [0]*S for island_name in island_names }
    for k in range(K):
        for h, island_name in enumerate(island_names):
            for i, ni in enumerate(community[k][h]):
                if ni > 0:
                    spp_idx = spp_IDs.index( (k, i) )
                    data[island_name][spp_idx] += 1


    # turn it into a flat row so it can be written to a csv
    data_row = list()
    for island_name in island_names:
        data_row += data[island_name]

    # to reverse this process
    # data2 = {isle_name: data_row[i:i+S] for i, isle_name in zip(range(0, S*H, S), isle_names) }


    # write a row to a csv
    # ---

    record  = [sample_ID, S, H, K, theta, T]
    record += [ J for J in JV ]
    record += [ m for m in mV ]
    record += [ spp_in_niche for spp_in_niche in spp_in_niches ]
    record += [ ''.join([ 'p' if v == 1 else 'a' for v in data_row ]) ]

    with open(fname, 'a', newline='') as csvfile:

        writer = csv.writer(csvfile, lineterminator = os.linesep)
        writer.writerow(record)

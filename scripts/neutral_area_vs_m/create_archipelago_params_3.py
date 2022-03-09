# use parameter_3_Jm.csv to create a friendlier version of the parameter values that defines
# each archipelago separately and the parameter values (J, m, T) for each island within
# in a way we can standardise across the simulation experiments

import pandas as pd
import numpy as np

# parameters
# ---

# where to save results
dir_results = '../../results/neutral_area_vs_m/'
suffix = '_3'


# read in the baseline parameter values
# ---

# the number of islands, fundamental biodiversity, and number of niches does not change between runs

fname_base = dir_results + 'baseline.csv'
df_base = pd.read_csv(fname_base)
df_base = df_base[df_base['suffix'] == suffix ]

theta = df_base.iloc[0]['theta']
K = df_base.iloc[0]['K']
H = df_base.iloc[0]['H']

T = np.inf # assume these islands have been separated from the mainland for a long time

# read in the parameter values for the different archipelagos
# ---

fname = dir_results + 'parameter' + suffix + '_Jm.csv'
df = pd.read_csv(fname) # rows are islands

# I set it up so it was organised into archipelagos that can be indexed (J_j, m_i)
# where j = 1 .. 3 and i = 1 .. 5; 
# this is going to get confusing bc I also index by island in the same way, so rename those columns

rename_Js = { 'J'+str(j): 'archJ'+str(j) for j in range(1,4) }
rename_ms = { 'm'+str(i): 'archm'+str(i) for i in range(1,6) }
df = df.rename(columns = rename_Js)
df = df.rename(columns = rename_ms)


# create an entry for each archipelago
# ---

# columns:
# suffix, archipelago_ID, H, theta, K, theta_0..theta_K, K_0..K_{H-1}, T_0..T_{H-1}, J_0..J_{H-1}, m_0..m_{H-1}

thetaV = [theta/K]*K
KV = [ '|'.join( str(k) for k in range(K)) ]*H
TV = [T]*H

data_rows = list() # each of these will be a row of the new data frame

for j in range(1,4):

    archJ = 'archJ' + str(j)

    for i in range(1,6):

        archm = 'archm' + str(i)
        archipelago_ID = 'J' + str(j) + '_m' + str(i)

        # extract each islands J and m values
        JV = list(df[archJ].values)
        mV = list(df[archm].values)

        data_row = [suffix, archipelago_ID, H, theta, K] + thetaV + KV + TV + JV + mV
        data_rows.append(data_row)


# write new parameters dataframe to file
# ---

fname_csv = dir_results + 'archipelago_params' + suffix + '.csv'

# columns:
# suffix, archipelago_ID, H, theta, theta_0..theta_K, K_0..K_{H-1}, T_0..T_{H-1}, J_0..J_{H-1}, m_0..m_{H-1}
columns = ['suffix', 'archipelago_ID', 'H', 'theta', 'K'] + \
        [ 'theta_' + str(k) for k in range(K) ] + \
        [ 'K_' + str(h) for h in range(H) ] + \
        [ 'T_' + str(h) for h in range(H) ] + \
        [ 'J_' + str(h) for h in range(H) ] + \
        [ 'm_' + str(h) for h in range(H) ]

df = pd.DataFrame.from_records(data_rows, columns=columns)

df.to_csv(fname_csv, mode='w', header=True, index=False)

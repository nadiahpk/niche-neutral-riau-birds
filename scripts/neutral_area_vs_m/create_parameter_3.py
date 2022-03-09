# create a parameter set of varying J and m to explore the model

import numpy as np
import matplotlib.pyplot as plt
#from scipy.special import digamma
import pandas as pd


# parameters
# ---

# where to save results
dir_results = '../../results/neutral_area_vs_m/'
suffix = '_3'


# a place to store the sets of JV and mV
# ---

# numbered them for now (see notebook)
JVD = dict()
mVD = dict()


# get the baseline parameter values (ie not the ones we vary J and S)
# ---

fname_csv = dir_results + 'baseline.csv'
df = pd.read_csv(fname_csv)
df = df[df['suffix'] == suffix] # subset the suffix we want

# record each of the baseline parameter values
# columns = ['suffix', 'K', 'H', 'm', 'theta', 'J', 'S']
K = df['K'].values[0]
H = df['H'].values[0]
theta = df['theta'].values[0]


# store the baseline as m3, J3
mV = df['m'].values
JV = df['J'].values

JVD[3] = JV
mVD[3] = mV


# increasing m is numbered as m5, J1
# ---

fname_csv = dir_results + 'increasing_m.csv'
df = pd.read_csv(fname_csv)
df = df[df['baseline_suffix'] == suffix] # subset the suffix we want

JV = df['J'].values
mV = df['m'].values

JVD[1] = JV
mVD[5] = mV


# decreasing m is numbered as m1, J3
# ---

fname_csv = dir_results + 'decreasing_m.csv'
df = pd.read_csv(fname_csv)
df = df[df['baseline_suffix'] == suffix] # subset the suffix we want

# JV = df['J'].values already have
mV = df['m'].values
mVD[1] = mV


# create points half-way between m1, m3; m3, m5; J1, J3 on a log scale
# ---

# m1, m3
m1V = mVD[1]; pwr1V = np.log10(m1V)
m3V = mVD[3]; pwr3V = np.log10(m3V)

pwr2V = [ (pwr1+pwr3)/2 for pwr1, pwr3 in zip(pwr1V, pwr3V) ]
m2V = [ 10**pwr2 for pwr2 in pwr2V ]

mVD[2] = m2V

# m3, m5
m5V = mVD[5]; pwr5V = np.log10(m5V)
m3V = mVD[3]; pwr3V = np.log10(m3V)

pwr4V = [ (pwr5+pwr3)/2 for pwr5, pwr3 in zip(pwr5V, pwr3V) ]
m4V = [ 10**pwr4 for pwr4 in pwr4V ]

mVD[4] = m4V

# J1, J3
J1V = JVD[1]; pwr1V = np.log10(J1V)
J3V = JVD[3]; pwr3V = np.log10(J3V)

pwr2V = [ (pwr1+pwr3)/2 for pwr1, pwr3 in zip(pwr1V, pwr3V) ]
J2V = [ 10**pwr2 for pwr2 in pwr2V ]

JVD[2] = J2V


# plot each one to visually verify
# ---

if True:

    for ID in sorted(mVD.keys()):
        V = mVD[ID]
        plt.plot(V, '-o', label='m'+str(ID))
    plt.yscale('log');
    plt.xlabel('islands');
    plt.ylabel(r'immigration rate, $m$')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(dir_results + 'parameter' + suffix + '_mID.pdf')
    plt.close()

    for ID in sorted(JVD.keys()):
        V = JVD[ID]
        plt.plot(V, '-o', label='J'+str(ID));
    plt.yscale('log');
    plt.xlabel('islands');
    plt.ylabel(r'island size, $J$')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(dir_results + 'parameter' + suffix + '_JID.pdf')
    plt.close()


# store them
# ---

fname_csv = dir_results + 'parameter' + suffix + '_Jm.csv'

# create a dictionary for the dataframe
data = {
        **{ 'm'+str(i): v for i, v in mVD.items() },
        **{ 'J'+str(i): v for i, v in JVD.items() },
        'suffix': [suffix]*H,
        'island_ID': list(range(H))
        }

df = pd.DataFrame.from_dict(data)
df.set_index('island_ID', inplace=True)

df.to_csv(fname_csv, mode='w', header=True, index=True)


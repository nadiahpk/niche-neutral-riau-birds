# create two 'baseline' scenarios from which we can vary the parameters to explore
# the effect of area, immigration rate, and number of niches

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import digamma
import pandas as pd
import os

import sys
sys.path.append("../../functions")

from my_functions import S_fnc


# parameters
# ---

# where to save results
dir_results = '../../results/neutral_jump_migration/'

# write_csv = False

# choose parameter values similar to the survey example
H = 16          # number of islands

m = 0.00075
pwr_min = np.log10(1e2);    # range of area of each island (10**pwr km^2)
pwr_max = np.log10(1e5);    # aim for J_crit = 3.2e3
K = 10

suffix = '_4'

# vary m and theta over scenarios
vary_theta = {
        1: 5,
        2: 20,
        }

vary_m = {
        1: [0.00075]*12 + [0.1]*4,
        2: [0.00075]*12 + [0.01]*4,
        }


# plot the theoretical curve for the first one
# ---

# get the colour cycle
colours = plt.rcParams['axes.prop_cycle'].by_key()['color']

# the first one with constant m
m = vary_m[1][0]
theta = vary_theta[1]

# get a smooth curve
pwrV_theor = np.linspace(pwr_min, pwr_max, 50)
JV_theor = [ 10**pwr for pwr in pwrV_theor ]
SV = [ S_fnc(theta, K, J/K, m) for J in JV_theor ]

# plot
plt.xscale('log')
plt.plot(JV_theor, SV, color=colours[0], alpha=0.3, label=r'theoretical curve constant $m$')         # smooth curve


# plot points for each other m scenario
# ---

# create points for each island linear along the J range
pwrV = np.linspace(pwr_min, pwr_max, H)
JV_pts = [ 10**pwr for pwr in pwrV ]

for colour, archipelago_ID in zip(colours, vary_m.keys()):

    mV = vary_m[archipelago_ID]
    theta = vary_theta[archipelago_ID]

    # number of species for the points
    SV_pts = [ S_fnc(theta, K, J/K, m) for m, J in zip(mV, JV_pts) ]

    # plot points
    plt.plot(JV_pts, SV_pts, '-o', color=colour, alpha=0.5, label='scenario ' + str(archipelago_ID))    # sample points


# plot decorations and save
# ---
plt.legend(loc='best')
plt.xlabel(r'carrying capacity (no. individuals)')
plt.ylabel(r'number of species')
plt.tight_layout()
plt.savefig(dir_results + 'richness' + suffix + '.pdf')
plt.close()


# save to a csv file
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

data_rows = list()

for archipelago_ID, mV in vary_m.items():

    data_row = [suffix, archipelago_ID, H, theta, K ]

    data_row += [ theta/K ]*K

    # append each of the K_h, which are strings with the niche IDs e.g., 0|1|2 means island h has niches 0, 1, and 2
    for h in range(H):
        data_row += ['|'.join([ str(i) for i in range(K) ])]

    data_row += [ np.inf ]*H

    data_row += JV_pts

    data_row += mV

    data_rows.append(data_row)


# make dataframe and save
df = pd.DataFrame.from_records(data_rows, columns=columns)
df.to_csv(fname_csv, mode='w', header=True, index=False)

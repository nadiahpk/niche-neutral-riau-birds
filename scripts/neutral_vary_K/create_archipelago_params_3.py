# create two 'baseline' scenarios from which we can vary the parameters to explore
# the effect of area, immigration rate, and number of niches

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import digamma
import pandas as pd


# parameters
# ---

# where to save results
dir_results = '../../results/neutral_vary_K/'

# write_csv = False

# choose parameter values similar to the survey example
H = 16          # number of islands

theta = 10
m = 0.00075
pwr_min = 2 # range of area of each island (10**pwr km^2)
pwr_max = 5 # aim for J_crit = 3.2e3

suffix = '_3'

# vary K { archipelago_ID: KV }
vary_K = {
        1: [10]*16,
        2: [10]*8 + [11]*8,
        3: [10]*8 + [11]*4 + [12]*4,
        4: [10]*8 + [12]*8,
        5: [10]*8 + [12]*4 + [14]*4,
        6: [10]*8 + [16]*8,
        7: [10]*8 + [16]*4 + [18]*4,
        8: [10]*8 + list(range(11,19)),
        9: [10]*12 + [18]*4,
        10: [10]*15 + [18]
        }


# plot the theoretical curve for the first one
# ---

# function to define theoretical curve
S_fnc = lambda theta_k, K, J_k, m: theta_k*K*( digamma( theta_k + ((J_k-1)*m/(1-m))*( digamma(((J_k-1)*m/(1-m))+J_k) - digamma(((J_k-1)*m/(1-m))) ) ) - digamma( theta_k ) )
# K is the no. niches on this island, theta_k is the fundamental biodiversity in niche k, and J_k is the no. of individuals in niche k

# get the colour cycle
colours = plt.rcParams['axes.prop_cycle'].by_key()['color']

# the first one with constant K
K = vary_K[1][0]

# get a smooth curve
pwrV_theor = np.linspace(pwr_min, pwr_max, 50)
JV_theor = [ 10**pwr for pwr in pwrV_theor ]
SV = [ S_fnc(theta/K, K, J/K, m) for J in JV_theor ]

# plot
plt.xscale('log')
plt.plot(JV_theor, SV, color=colours[0], alpha=0.3, label=r'theoretical curve constant $K$')         # smooth curve


# plot points for each other K scenario
# ---

# create points for each island linear along the J range
pwrV = np.linspace(pwr_min, pwr_max, H)
JV_pts = [ 10**pwr for pwr in pwrV ]

for colour, (archipelago_ID, KV) in zip(colours, vary_K.items()):

    # number of species for the points
    theta_kV = [ theta / max(KV) ] * H # evently split between max no. niches
    J_kV = [ J / k for J, k in zip(JV_pts, KV) ]
    SV_pts = [ S_fnc(theta_k, K, J_k, m) for theta_k, K, J_k in zip(theta_kV, KV, J_kV) ]

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

for archipelago_ID, KV in vary_K.items():

    K_max = max(KV)
    data_row = [suffix, archipelago_ID, H, theta, K_max ]

    data_row += [ theta/K_max]*K

    # append each of the K_h, which are strings with the niche IDs e.g., 0|1|2 means island h has niches 0, 1, and 2
    for h in range(H):
        data_row += ['|'.join([ str(i) for i in range(KV[h]) ])]

    data_row += [ np.inf ]*H

    data_row += JV_pts

    data_row += [m]*H

    data_rows.append(data_row)


# make dataframe and save
df = pd.DataFrame.from_records(data_rows, columns=columns)
df.to_csv(fname_csv, mode='w', header=True, index=False)

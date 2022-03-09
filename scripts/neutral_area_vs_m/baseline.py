# create two 'baseline' scenarios from which we can vary the parameters to explore
# the effect of area, immigration rate, and number of niches

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import digamma
import pandas as pd
import os


# parameters
# ---

# where to save results
dir_results = '../../results/neutral_area_vs_m/'

write_csv = True

# choose parameter values similar to the survey example
H = 16          # number of islands

# choose theta and m so that J_crit is roughly in the middle of the range

'''
# max no. spp ~ 40
suffix = '_1'
K = 5           # number of niches
theta = 8       # fundamental biodiversity number across all niches
m = 0.0010      # immigration parameter
pwr_min = 1;    # range of area of each island (10**pwr km^2)
pwr_max = 5;

# max no. spp ~ 100
K = 5           # number of niches
suffix = '_2'
theta = 35
m = 0.0007
pwr_min = 1;    # range of area of each island (10**pwr km^2)
pwr_max = 5;
'''
# max no. spp ~ 40
K = 10           # number of niches
suffix = '_3'
theta = 10
m = 0.00075
pwr_min = np.log10(1e2);    # range of area of each island (10**pwr km^2)
pwr_max = np.log10(1e5);    # aim for J_crit = 3.2e3



# create curves
# ---

# function to define theoretical curve
S_fnc = lambda theta, K, Js, m: theta*( digamma( theta/K + ((Js-1)*m/(1-m))*( digamma(((Js-1)*m/(1-m))+Js) - digamma(((Js-1)*m/(1-m))) ) ) - digamma( theta/K ) )

# create points for each island linear along the J range
pwrV = np.linspace(pwr_min, pwr_max, H)
JV_pts = [ 10**pwr for pwr in pwrV ]

# number of species for the points
SV_pts = [ S_fnc(theta, K, J/K, m) for J in JV_pts ]


# save to a csv file
# ---

if write_csv:

    # create dataframe
    columns = ['suffix', 'K', 'H', 'm', 'theta', 'J', 'S']

    suffixV = [suffix]*H
    KV = [K]*H
    HV = [H]*H
    mV = [m]*H
    thetaV = [theta]*H

    df = pd.DataFrame(
            list(zip( suffixV, KV, HV, mV, thetaV, JV_pts, SV_pts )), 
            columns = columns )

    # save to file, or append if file already exists

    fname_csv = dir_results + 'baseline.csv'
    if not os.path.isfile(fname_csv):
        # write with headers
        df.to_csv(fname_csv, mode='w', header=True, index=False)
    else:
        # append
        df.to_csv(fname_csv, mode='a', header=False, index=False)


# plotting data for a smooth curve in the range
# ---

pwrV_theor = np.linspace(np.log10(min(JV_pts)), np.log10(max(JV_pts)), 50)
JV_theor = [ 10**pwr for pwr in pwrV_theor ]
SV = [ S_fnc(theta, K, J/K, m) for J in JV_theor ]


# plot relationships to verify how it looks
# ---

plt.xscale('log')

plt.plot(JV_theor, SV, color='blue', label='theoretical curve')         # smooth curve
J_crit = theta*(1-m)*(np.exp(K/theta)-1) / ( m*np.log(1/m) )            # critical J
plt.scatter(JV_pts, SV_pts, color='black', label='sample locations')    # sample points

# plot decorations and save
plt.legend(loc='best')
plt.axvline(J_crit, color='black', ls='dashed')
plt.xlabel(r'carrying capacity (no. individuals)')
plt.ylabel(r'number of species')
plt.tight_layout()
plt.savefig(dir_results + 'baseline' + suffix + '.pdf')
plt.close()

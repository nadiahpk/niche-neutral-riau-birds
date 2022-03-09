# see if you can fit a flat J and varying m to the baseline

from scipy.special import digamma
from scipy.optimize import bisect
import pandas as pd
import numpy as np


# parameters
# ---

# which run
suffix = '_3'

# fixed value of J - chose J_crit
# J_fixed = 3.2e3 # chosen to be in the middle of the range

# where the results are
dir_results = '../../results/neutral_area_vs_m/'


# read in the data and grab the J vs S relationship
# ---

fname_csv = dir_results + 'baseline.csv'
df = pd.read_csv(fname_csv)

# subset the suffix we want
df = df[df['suffix'] == suffix]

# info we need
JV = df['J'].values
SV = df['S'].values

K = df['K'].values[0]
theta = df['theta'].values[0]
m = df['m'].values[0]
H = df['H'].values[0]


# set J_fixed to be J_crit
# ---

J_fixed = theta*(1-m)*(np.exp(K/theta)-1) / ( m*np.log(1/m) )            # critical J


# find the m that satisfies each S given that J = J_fixed
# ---

# function to define theoretical curve
S_fnc = lambda theta, K, Js, m: theta*( digamma( theta/K + ((Js-1)*m/(1-m))*( digamma(((Js-1)*m/(1-m))+Js) - digamma(((Js-1)*m/(1-m))) ) ) - digamma( theta/K ) )

# for each J, find the value of m that makes S_fnc = S
m_lo = 1e-10; m_hi = 1 - 1e-10

mV = list()
for J, S in zip(JV, SV):

    fnc = lambda m: S - S_fnc(theta, K, J_fixed/K, m)
    S_lo = fnc(m_lo)
    S_hi = fnc(m_hi)

    if np.sign(S_lo) != np.sign(S_hi):

        m_est = bisect(fnc, m_lo, m_hi)

    else:

        m_est = np.nan

    mV.append(m_est)


# save them to a file
# ---

# create dataframe
columns = ['baseline_suffix', 'island_ID', 'K', 'H', 'm', 'theta', 'J', 'S']

baseline_suffixV = [suffix]*H
island_IDV = list(range(H))
KV = [K]*H
HV = [H]*H
mV = mV
thetaV = [theta]*H
JV = [J_fixed]*H
# SV

df = pd.DataFrame(
        list(zip( baseline_suffixV, island_IDV, KV, HV, mV, thetaV, JV, SV )), 
        columns = columns )

fname_csv = dir_results + 'increasing_m.csv'
df.to_csv(fname_csv, mode='w', header=True, index=False)


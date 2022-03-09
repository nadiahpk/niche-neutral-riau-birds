# create two 'baseline' scenarios from which we can vary the parameters to explore
# the effect of area, immigration rate, and number of niches

#import numpy as np
import matplotlib.pyplot as plt
from scipy.special import digamma
import pandas as pd


# parameters
# ---

# where to save results
dir_results = '../../results/neutral_vary_K/'

# which one to plot
suffix = '_3'
archipelago_ID = 1 # scenario


# read in parameter values
# ---

fname_params = dir_results + 'archipelago_params' + suffix + '.csv'
df_params = pd.read_csv(fname_params)

row = df_params[df_params['archipelago_ID'] == archipelago_ID].iloc[0]

H = row['H']
K = row['K']
m = row['m_0']
theta = row['theta']
JV = [ row[ 'J_' + str(h) ] for h in range(H) ]


# plot the theoretical curve for the first one
# ---

# function to define theoretical curve
S_fnc = lambda theta_k, K, J_k, m: theta_k*K*( digamma( theta_k + ((J_k-1)*m/(1-m))*( digamma(((J_k-1)*m/(1-m))+J_k) - digamma(((J_k-1)*m/(1-m))) ) ) - digamma( theta_k ) )
# K is the no. niches on this island, theta_k is the fundamental biodiversity in niche k, and J_k is the no. of individuals in niche k

SV = [ S_fnc(theta/K, K, J/K, m) for J in JV ]


# plot and save
# ---

plt.xscale('log')
plt.plot(JV, SV, color='black', alpha=0.3) # background curve
plt.scatter(JV, SV, color='black') # actual islands
plt.xlabel(r'carrying capacity (no. individuals)')
plt.ylabel(r'number of species')
plt.tight_layout()
plt.savefig(dir_results + 'richness' + suffix + '_archipelago_' + str(archipelago_ID) + '.pdf')
plt.close()

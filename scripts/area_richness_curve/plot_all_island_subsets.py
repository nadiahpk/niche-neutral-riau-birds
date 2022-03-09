import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.insert(0,'../../functions')

from my_functions import S_fnc # S_fnc(theta, K, J, m)


# parameters
# ---

# where to put the plots
dirname_plots = '../../results/area_richness_curve/'

# where to find the island area and richness data
fname_area = '../../data/processed/island_area.csv'     # island_name,area_sq_m,area_sq_km
fname_rich = '../../data/processed/island_richness.csv' # island_name,richness

# which island subsets info kept
dirname_subsets = '../../data/processed/island_subsets/'

# where fits of island subsets
fname_fits = '../../results/area_richness_curve/best_fits.csv'


# create a dataframe: island_name, area, richness
# ---

df_area = pd.read_csv(fname_area)
df_rich = pd.read_csv(fname_rich)
assert len(df_area) == len(df_rich), f'Number of islands in {fname_area} =/= {fname_rich}'
df_data = pd.merge(df_area, df_rich, on="island_name")


# read in the fits
# ---

df_fits = pd.read_csv(fname_fits, header=0)


# Eq. 
#S_fnc = lambda theta, K, J, m: theta*( digamma( theta/K + ((J-1)*m/(1-m))*( digamma(((J-1)*m/(1-m))+J) - digamma(((J-1)*m/(1-m))) ) ) - digamma( theta/K ) )


# make a plot for each island subset and rho combination
# ---

subsets = set(df_fits['subset_name'])
rhos = set(df_fits['rho'])

for subset in subsets:

    # which islands are these
    islands = list( pd.read_csv( dirname_subsets + subset + '.csv', header=0 )['island_name'] )

    # subset the data to those islands
    df_data_sub = df_data[df_data['island_name'].isin(islands)]
    
    for rho in rhos:

        # write the name for the plot
        fname_plot = dirname_plots + subset + '_rho_' + str(rho) + '.pdf'

        # find the best fit row and extract values
        best_fit = df_fits[ (df_fits['subset_name'] == subset) & (df_fits['rho'] == rho) ]
        K = best_fit['K'].values[0]
        theta = best_fit['theta_est'].values[0]
        m = best_fit['m_est'].values[0]
        A_crit = best_fit['A_crit_est'].values[0]

        # create a good range of J values
        A_max = np.max(df_data_sub['area_sq_km'])
        A_min = np.min(df_data_sub['area_sq_km'])
        A_pwr_min = np.log10(A_min); A_pwr_max = np.log10(A_max)
        A_pwrV = np.linspace( A_pwr_min, A_pwr_max, 100 )
        AV = 10**A_pwrV
        JV = AV*rho/K # the total area is divided into K niches and multiplied by the density

        # predict species richness for each J value
        SV = [ S_fnc(theta, K, J, m) for J in JV ]

        # plot everything
        plt.scatter(df_data_sub['area_sq_km'], df_data_sub['richness'], alpha=0.7, color='black', label='data')    # data
        plt.plot(AV, SV, color='blue', label='fitted')                                                              # fitted
        plt.axvline(A_crit, color='black', ls='dashed')                                                             # A_critical
        plt.legend(loc='best')
        plt.xscale('log')
        plt.xlabel(r'area (km$^2$)')
        plt.ylabel(r'number of species')
        plt.xlim( (1e-4, 5e5) )
        plt.ylim( (-5, 160) )
        plt.tight_layout()
        plt.savefig(fname_plot)
        plt.close()




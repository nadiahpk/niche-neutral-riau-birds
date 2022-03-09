# create parameters for an archipelago based on the Chisholm model fits to the survey data
# for different values of K

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys
sys.path.append('../../functions/')

from my_functions import S_fnc # Eq. 2.5 in Chisholm et al. (2016) S_fnc(theta, K, J, m)


# parameters
# ---

# a suffix for grouping parameter sets / experiments
suffix = '_1'

# which plot to make
plot_name = 'check_2'

# number of individuals / sq-km
rho = 1700

# number of islands
H = 16

# range of K values to explore
KV = [1, 3, 5, 7]

# range of island areas based on the approximate range of survey_only
A_pwr_min = -3
A_pwr_max = 3

# range of Js roughly based on areas above
J_pwr_min = 1
J_pwr_max = 5

# where all fits stored
fname_fits = '../../results/area_richness_curve/all_fits.csv'

# where to find the island area and richness data
fname_area = '../../data/processed/island_area.csv'     # island_name,area_sq_m,area_sq_km
fname_rich = '../../data/processed/island_richness.csv' # island_name,richness

# which island subsets info kept
dirname_subsets = '../../data/processed/island_subsets/'

# where to save results
dir_results = '../../results/neutral_survey_vary_K/'


# secondary parameter values
# ---

# range of areas
A_pwrV = np.linspace(A_pwr_min, A_pwr_max, 100)
AV = 10**A_pwrV


# read in and plot the data
# ---

if plot_name == 'check_1':

    # create a dataframe: island_name, area, richness
    df_area = pd.read_csv(fname_area)
    df_rich = pd.read_csv(fname_rich)
    assert len(df_area) == len(df_rich), f'Number of islands in {fname_area} =/= {fname_rich}'
    df_data = pd.merge(df_area, df_rich, on="island_name")

    # which islands are these
    islands = list( pd.read_csv( dirname_subsets + 'survey_only.csv', header=0 )['island_name'] )

    # subset the data to those islands
    df_data_sub = df_data[df_data['island_name'].isin(islands)]

    # plot
    plt.scatter(df_data_sub['area_sq_km'], df_data_sub['richness'], alpha=0.7, color='black', label='data')    # data


# read in the fitted parameter values
# ---

# all fits
df_fits = pd.read_csv(fname_fits)

# get the survey_only rho subset we're interested in
df_fits = df_fits[df_fits['subset_name'] == 'survey_only']
df_fits = df_fits[df_fits['rho'] == rho]


# for each K value, plot the best-fitting line to the data (for checking)
# ---

if plot_name == 'check_1':

    for K in KV:

        # number of individuals per niche
        JV = AV * rho / K

        # extract other parameter values
        best_fit = df_fits[df_fits['K'] == K]
        theta = best_fit.iloc[0]['theta_est']
        m = best_fit.iloc[0]['m_est']

        # calculate richness S using Chisholm model
        SV = [S_fnc(theta, K, J, m) for J in JV ]

        label = r'$K = ' + str(K) + r'$'
        plt.plot(AV, SV, alpha=0.7, label=label)

    plt.legend(loc='best')
    plt.xscale('log')
    plt.xlabel(r'area (km$^2$)', fontsize='xx-large')
    plt.ylabel(r'number of species', fontsize='xx-large')
    plt.tight_layout()
    plt.savefig(dir_results + 'check_curves.pdf')
    plt.close()


# create the artificial archipelago
# ---

J_pwrV = np.linspace(J_pwr_min, J_pwr_max, H)
JV = list(10**J_pwrV)

# check the curves again

data_rows = list()
for K in KV:

    # extract other parameter values
    best_fit = df_fits[df_fits['K'] == K]
    theta = best_fit.iloc[0]['theta_est']
    m = best_fit.iloc[0]['m_est']

    # create data row for csv file
    data_row = [suffix, K, H, theta, m, np.inf] + JV
    data_rows.append(data_row)

    if plot_name != 'check_1':
        # calculate richness S using Chisholm model
        SV = [S_fnc(theta, K, J/K, m) for J in JV ]

        label = r'$K = ' + str(K) + r'$'
        plt.plot(JV, SV, '-o', alpha=0.7, label=label)

if plot_name != 'check_1':
    plt.legend(loc='best', fontsize='medium')
    plt.xscale('log')
    plt.xlabel(r'island carrying capacity (individuals)', fontsize='xx-large')
    plt.ylabel(r'species richness', fontsize='xx-large')
    plt.tight_layout()
    plt.savefig(dir_results + 'check_curves_2.pdf')
    plt.close()


# write parameters to a dataframe to file
# ---

# suffix, archipelago_ID, H, theta, theta_0..theta_K, K_0..K_{H-1}, T_0..T_{H-1}, J_0..J_{H-1}, m_0..m_{H-1}
fname_csv = dir_results + 'archipelago_params' + suffix + '.csv'
columns = ['suffix', 'K', 'H', 'theta', 'm', 'T'] + [ 'J_' + str(h) for h in range(H) ]

df = pd.DataFrame.from_records(data_rows, columns=columns)
df.to_csv(fname_csv, mode='w', header=True, index=False)

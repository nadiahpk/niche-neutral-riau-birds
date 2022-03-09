import sys
sys.path.insert(0,'../../functions')

import pandas as pd
import numpy as np

from my_functions import fit_area_richness


# parameters
# ---

# where to find the island area and richness data
fname_area = '../../data/processed/island_area.csv'     # island_name,area_sq_m,area_sq_km
fname_rich = '../../data/processed/island_richness.csv' # island_name,richness

# which island subsets to fit - correspond to file names
subsets = ['all',  'peninsula_only',  'riau_only',  'survey_only']
dirname_subsets = '../../data/processed/island_subsets/'

# which rho values to assume
rhos = [2115, 1259, 1700]     # these are density birds per km^2

# 2115: 
#   Estimated by taking the average density in Sheldon et al (2011) 
#   of the primary rainforest habitats (albizia softwoods, logged forest softwoods, peatswamp softwoods). 
#   https://lkcnhm.nus.edu.sg/app/uploads/2017/04/59rbz295-309.pdf 
# 1259 
#   Estimated from Figure 3 of Castelletta et al (2005) of resident birds in Old Secondary Forests.
#   https://www.sciencedirect.com/science/article/abs/pii/S0006320704001740 

# range of K values to fit
Ks = [ i for i in range(1, 15) ]  # just a bit of a guess


# create a dataframe: island_name, area, richness
# ---

df_area = pd.read_csv(fname_area)
df_rich = pd.read_csv(fname_rich)
assert len(df_area) == len(df_rich), f'Number of islands in {fname_area} =/= {fname_rich}'
df = pd.merge(df_area, df_rich, on="island_name")


# loop over all rho and subset combinations, finding fits
# ---

# create our subset_rho combinations
subset_rhos = [ (subset, rho) for subset in subsets for rho in rhos ]

results = list()        # place to store results for every fitting (every K value)
best_results = list()   # only the best K value
for subset, rho in subset_rhos:

    # get the list of islands we want
    islands = list( pd.read_csv( dirname_subsets + subset + '.csv', header=0 )['island_name'] )

    # subset the relevant array of richness S and areas A
    S_true = np.array(df[df['island_name'].isin(islands)]['richness'])
    A = np.array(df[df['island_name'].isin(islands)]['area_sq_km'])

    # find all fits and the best fitting
    fits = fit_area_richness(A, S_true, rho, Ks) # [[ K, residual_est, theta_est, m_est, A_crit ], ...]
    _, residual_ests, _, _, _ = zip(*fits)
    lowest_residual_idx = np.argmin(residual_ests)
    best_fit = fits[lowest_residual_idx]

    # append
    for fit in fits:
        results.append( [subset, rho] + fit )
    best_results.append( [subset, rho] + best_fit )


# write them to csv
# ---

df_tmp = pd.DataFrame(best_results, 
        columns=['subset_name', 'rho', 'K', 'residual', 'theta_est', 'm_est', 'A_crit_est'])
df_tmp.to_csv('../../results/area_richness_curve/best_fits.csv', index=False)

df_tmp = pd.DataFrame(results, 
        columns=['subset_name', 'rho', 'K', 'residual', 'theta_est', 'm_est', 'A_crit_est'])
df_tmp.to_csv('../../results/area_richness_curve/all_fits.csv', index=False)


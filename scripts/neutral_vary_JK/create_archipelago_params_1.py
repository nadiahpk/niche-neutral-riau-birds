# how does area of two niche types vary with island size?

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# parameters
# ---

# where to save results
dir_results = '../../results/neutral_vary_JK/'

# number of islands
H = 16

theta = 10
m = 0.00075

# range of island carrying capacities (10**pwr km^2)
pwr_min = 2
pwr_max = 5

suffix = '_1'

# assumption of this parameter set: when J = 1000, half of the area is coastal and half interior

K = 10 # total number of niches (needs to be an even number of this assumption)
J = 1000 # the point where half-half

# radius of two habitat types
rad_tot = np.sqrt(J/np.pi)      # total island radius 17.841241161527712
rad_inn = np.sqrt(J/(2*np.pi))  # inner habitat radius 12.6156626101008
rad_out = rad_tot - rad_inn     # coastal habitat 'radius' 5.225578551426912


# secondary parameters
# ---

theta_k = theta / K
pwrV = np.linspace(pwr_min, pwr_max, H)
JV = [ 10**pwr for pwr in pwrV ]

# assume a circular island, and assume the outer "radius" (coastal) stays the same width
rad_totV = [ np.sqrt(J/np.pi) for J in JV ]
rad_innV = [ rad_tot - rad_out for rad_tot in rad_totV ]
J_innV = [ np.pi*rad_inn**2 for rad_inn in rad_innV ]
J_outV = [ J - J_inn for J, J_inn in zip(JV, J_innV) ]


# visualise
# ---

plt.plot(JV, J_innV, label='island interior')
plt.plot(JV, J_outV, label='island coastal')
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'island carrying capacity (individuals)')
plt.ylabel(r'habitat carrying carrying capacity')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig(dir_results + 'archipelago' + suffix + '.pdf')
plt.close()


# create J[k][h], the number of individuals in each niche k on each island h
# ---

# get per-niche number of individuals for island inner and outer
niche_per_habitat = K // 2
Jk_innV = [ J_inn/niche_per_habitat for J_inn in J_innV ]
Jk_outV = [ J_out/niche_per_habitat for J_out in J_outV ]

# construct J[k][h]
Jkh = list()

# the first half of niches are interior
for k in range(K // 2):
    Jkh.append(Jk_innV)

# the second half are exterior
for k in range(K // 2):
    Jkh.append(Jk_outV)


# write the new parameter set to file
# ---

# flatten Jkh to a list for writing
JkhL = [ Jkh[k][h] for h in range(H) for k in range(K) ]
headL = ['J_' + str(k) + '_' + str(h) for h in range(H) for k in range(K) ]

# create dataframe to save
columns = ['suffix', 'H', 'theta_k', 'K', 'T', 'm']
columns += headL

data_row = [suffix, H, theta_k, K, np.inf, m] + JkhL
data_rows = [data_row]
df_out = pd.DataFrame.from_records(data_rows, columns=columns)

# save datafrmae
fname_csv = dir_results + 'archipelago_params' + suffix + '.csv'
df_out.to_csv(fname_csv, mode='w', header=True, index=False)

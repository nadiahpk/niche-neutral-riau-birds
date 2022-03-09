# not possible to use the Chisholm model to get richness on each island because niches change size
# so use the samples instead

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# parameters
# ---

scenarios = [
        # baseline
        {
            'label': '(0) baseline',
            'fname': '../../results/neutral_vary_K/average_richness_3_archipelago1.csv',
            },
        # scenario 9
        {
            'label': '(1) larger islands have additional niches',
            'fname': '../../results/neutral_vary_K/average_richness_3_archipelago9.csv',
            },
        # nested niches scenario 2
        {
            'label': '(2) inland niche area grows faster with island size',
            'fname': '../../results/neutral_vary_JK/average_richness_archipelago_2.csv',
            },
        ]

# number of islands NOTE being lazy
H = 16

# range of island carrying capacities (10**pwr km^2)
pwr_min = 2
pwr_max = 5

# range of carrying capacities
pwrV = np.linspace(pwr_min, pwr_max, H)
JV = [ 10**pwr for pwr in pwrV ]


# plot them together
# ---

plt.xscale('log')
for scenario in scenarios:

    label = scenario['label']
    fname = scenario['fname']

    # read in samples and find mean richnesses
    df = pd.read_csv(fname)
    JV = df['J'].values
    SV = df['mean_S'].values

    # plot
    plt.plot(JV, SV, alpha=0.3, label=label) # background curve
    plt.scatter(JV, SV) # actual islands

plt.xlabel(r'island carrying capacity (individuals)', fontsize='xx-large')
plt.ylabel(r'species richness', fontsize='xx-large')
plt.legend(loc='best')
plt.tight_layout()
plt.savefig('../../results/summary_stats/average_richness_K_effect.pdf')
plt.close()

# create a boxplot showing the baseline and two scenarios that increase the niche diversity with island size:
# (1) scenario 9, which adds niches to largest islands, and (2) nested niches suffix 2, which increases the size of interior islands

import pandas as pd
import matplotlib.pyplot as plt

# parameters
# ---

# column names depend on whether we're doing NODF or c-score
raw_col_name = 'observed_c_score'           # the column name for the raw score
ses_col_name = 'standardised_effect_size'   # the column name for the SES score

# plot names
raw_plot_fname = '../../results/summary_stats/boxplot_raw_c_score_K_effect.pdf'
ses_plot_fname = '../../results/summary_stats/boxplot_ses_c_score_K_effect.pdf'

ylabel = 'C-score'

# plot file name

scenarios = [
        # baseline
        {
            'xtick': '(0) baseline',
            'fname': '../../results/cooccurrence_neutral_vary_K/sim9_c_score_3.csv',
            'subset': [('archipelago_ID', 1)],
            },
        # scenario 9
        {
            'xtick': '(1) larger islands\nhave additional\nniches',
            'fname': '../../results/cooccurrence_neutral_vary_K/sim9_c_score_3.csv',
            'subset': [('archipelago_ID', 9)],
            },
        # nested niches scenario 2
        {
            'xtick': '(2) inland niche area\ngrows faster\nwith island size',
            'fname': '../../results/cooccurrence_neutral_vary_JK/sim9_c_score.csv',
            'subset': [('suffix', '_2')],
            },
        ]


# plot the raw scores
# ---

data_raws = list()
xticks = list()
for scenario in scenarios:

    # grab the raw data
    fname = scenario['fname']
    df = pd.read_csv(fname)

    # get the appropriate subset
    subset = scenario['subset']
    if subset:
        for (col_name, col_val) in scenario['subset']:
            df = df[df[col_name] == col_val]

    data_raw = df[raw_col_name].values

    data_raws.append(data_raw)
    xticks.append(scenario['xtick'])

plt.boxplot(data_raws)
plt.xticks(range(1,len(xticks)+1), xticks)
plt.xlabel(r'scenario')
plt.ylabel(r'raw ' + ylabel)
plt.tight_layout()
plt.savefig(raw_plot_fname)
plt.close()


# plot the ses scores
# ---

data_sess = list()
xticks = list()
for scenario in scenarios:

    # grab the ses data
    fname = scenario['fname']
    df = pd.read_csv(fname)

    # get the appropriate subset
    subset = scenario['subset']
    if subset:
        for (col_name, col_val) in scenario['subset']:
            df = df[df[col_name] == col_val]

    data_ses = df[ses_col_name].values

    data_sess.append(data_ses)
    xticks.append(scenario['xtick'])

plt.boxplot(data_sess)
plt.axhline(0, ls='dotted', color='black')
plt.xticks(range(1,len(xticks)+1), xticks)
plt.xlabel(r'scenario', fontsize='xx-large')
plt.ylabel(r'SES ' + ylabel, fontsize='xx-large')
plt.tight_layout()
plt.savefig(ses_plot_fname)
plt.close()

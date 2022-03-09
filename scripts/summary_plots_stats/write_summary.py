# write to a csv file the mean and SE for each of the items below

import pandas as pd
#import matplotlib.pyplot as plt
from scipy.stats import sem
import numpy as np


# parameters
# ---

scenarios = [
        {
            'fname': '../../results/nestedness_rowpack_neutral_survey_vary_K/sim9_NODF_1_K_1.csv',
            'subset': None,
            'data_col': 'observed_NODF',
            'note': 'how nestedness changes with K',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_survey_vary_K/sim9_NODF_1_K_3.csv',
            'subset': None,
            'data_col': 'observed_NODF',
            'note': 'how nestedness changes with K',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_survey_vary_K/sim9_NODF_1_K_5.csv',
            'subset': None,
            'data_col': 'observed_NODF',
            'note': 'how nestedness changes with K',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_survey_vary_K/sim9_NODF_1_K_7.csv',
            'subset': None,
            'data_col': 'observed_NODF',
            'note': 'how nestedness changes with K',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_survey_vary_K/sim9_NODF_1_K_1.csv',
            'subset': None,
            'data_col': 'standardised_effect_size',
            'note': 'how nestedness changes with K',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_survey_vary_K/sim9_NODF_1_K_3.csv',
            'subset': None,
            'data_col': 'standardised_effect_size',
            'note': 'how nestedness changes with K',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_survey_vary_K/sim9_NODF_1_K_5.csv',
            'subset': None,
            'data_col': 'standardised_effect_size',
            'note': 'how nestedness changes with K',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_survey_vary_K/sim9_NODF_1_K_7.csv',
            'subset': None,
            'data_col': 'standardised_effect_size',
            'note': 'how nestedness changes with K',
            },
        {
            'fname': '../../results/cooccurrence_neutral_data/sim9_c_score.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'observed_c_score',
            'note': 'first fit raw c_score',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_data/sim9_NODF.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'observed_NODF',
            'note': 'first fit raw NODF',
            },
        {
            'fname': '../../results/cooccurrence_neutral_data/sim9_c_score.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'standardised_effect_size',
            'note': 'first fit SES c-score',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_data/sim9_NODF.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'standardised_effect_size',
            'note': 'first fit SES NODF',
            },
        # increase the number of niches with island size
        {
            'fname': '../../results/cooccurrence_neutral_vary_K/sim9_c_score_3.csv',
            'subset': [('archipelago_ID', 1)],
            'data_col': 'observed_c_score',
            'note': 'baseline vary K effect on C-score',
            },
        {
            'fname': '../../results/cooccurrence_neutral_vary_K/sim9_c_score_3.csv',
            'subset': [('archipelago_ID', 1)],
            'data_col': 'standardised_effect_size',
            'note': 'baseline vary K effect on C-score',
            },
        {
            'fname': '../../results/cooccurrence_neutral_vary_K/sim9_c_score_3.csv',
            'subset': [('archipelago_ID', 9)],
            'data_col': 'observed_c_score',
            'note': 'scenario 9 increase segregation',
            },
        {
            'fname': '../../results/cooccurrence_neutral_vary_K/sim9_c_score_3.csv',
            'subset': [('archipelago_ID', 9)],
            'data_col': 'standardised_effect_size',
            'note': 'scenario 9 increase segregation',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_vary_K/sim9_NODF_3.csv',
            'subset': [('archipelago_ID', 1)],
            'data_col': 'observed_NODF',
            'note': 'baseline scenario 1',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_vary_K/sim9_NODF_3.csv',
            'subset': [('archipelago_ID', 1)],
            'data_col': 'standardised_effect_size',
            'note': 'baseline scenario 1',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_vary_K/sim9_NODF_3.csv',
            'subset': [('archipelago_ID', 9)],
            'data_col': 'observed_NODF',
            'note': 'scenario 9',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_vary_K/sim9_NODF_3.csv',
            'subset': [('archipelago_ID', 9)],
            'data_col': 'standardised_effect_size',
            'note': 'scenario 9',
            },
        # inland niches increase more with island size
        {
            'fname': '../../results/cooccurrence_neutral_vary_JK/sim9_c_score.csv',
            'subset': [('suffix', '_2')],
            'data_col': 'observed_c_score',
            'note': 'inland niches increase segregation',
            },
        {
            'fname': '../../results/cooccurrence_neutral_vary_JK/sim9_c_score.csv',
            'subset': [('suffix', '_2')],
            'data_col': 'standardised_effect_size',
            'note': 'inland niches increase segregation',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_vary_JK/sim9_NODF.csv',
            'subset': [('suffix', '_2')],
            'data_col': 'observed_NODF',
            'note': 'inland niches increase',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_vary_JK/sim9_NODF.csv',
            'subset': [('suffix', '_2')],
            'data_col': 'standardised_effect_size',
            'note': 'inland niches increase',
            },
        # verify that the effect on co-occurrence is not just about the change in richness
        {
            'fname': '../../results/cooccurrence_neutral_jump_migration/sim9_c_score.csv',
            'subset': [('archipelago_ID', 1)],
            'data_col': 'observed_c_score',
            'note': 'jump in migration doesnt affect co-occurence like jump in K',
            },
        {
            'fname': '../../results/cooccurrence_neutral_jump_migration/sim9_c_score.csv',
            'subset': [('archipelago_ID', 1)],
            'data_col': 'standardised_effect_size',
            'note': 'jump in migration doesnt affect co-occurence like jump in K',
            },
        # fitting m to each individual island's richness (insofar as possible)
        {
            'fname': '../../results/nestedness_rowpack_neutral_data_fitm/sim9_NODF.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'observed_NODF',
            'note': 'fitting m so richness isnt strictly increasing greatly reduces raw nestedness',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_data_fitm/sim9_NODF.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'standardised_effect_size',
            'note': 'fitting m so richness isnt strictly increasing is anti-nested',
            },
        {
            'fname': '../../results/cooccurrence_neutral_data_fitm/sim9_c_score.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'observed_c_score',
            'note': 'fitting m so richness isnt strictly increasing not much effect on c-score',
            },
        {
            'fname': '../../results/cooccurrence_neutral_data_fitm/sim9_c_score.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'standardised_effect_size',
            'note': 'fitting m so richness isnt strictly increasing not much effect on c-score',
            },
        # an example of contrivance of K and m to bring the metrics closer to observations
        {
            'fname': '../../results/cooccurrence_neutral_data_fitmK/sim9_c_score.csv',
            'subset': [('suffix', '_3')],
            'data_col': 'observed_c_score',
            'note': 'contrived on c-score',
            },
        {
            'fname': '../../results/cooccurrence_neutral_data_fitmK/sim9_c_score.csv',
            'subset': [('suffix', '_3')],
            'data_col': 'standardised_effect_size',
            'note': 'contrived on c-score',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_data_fitmK/sim9_NODF.csv',
            'subset': [('suffix', '_3')],
            'data_col': 'observed_NODF',
            'note': 'contrived on NODF',
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_data_fitmK/sim9_NODF.csv',
            'subset': [('suffix', '_3')],
            'data_col': 'standardised_effect_size',
            'note': 'contrived on NODF',
            },
        ]


# store mean and SE for each scenario
# ---


M = list()
for scenario in scenarios:

    # read in dataframe from data file
    fname = scenario['fname']
    df = pd.read_csv(fname)

    # get the appropriate subset
    subset = scenario['subset']
    if subset:

        for col_name, col_val in scenario['subset']:
            df = df[df[col_name] == col_val]

        subset_str = ' '.join([ str(v[0]) + '=' + str(v[1]) for v in subset ])

    else:

        subset_str = ''

    # get data
    data_col = scenario['data_col']
    data = df[data_col].values

    # find the mean and SE
    data_mean = np.mean(data)
    data_SE = sem(data)

    # store
    note = scenario['note'] 
    m = [fname, subset_str, data_col, data_mean, data_SE, note]
    M.append(m)


# write summary statistics to a csv
# ---

fname = '../../results/summary_stats/summary.csv'
df_out = pd.DataFrame.from_records(M, columns = ['file_name', 'subset', 'measure', 'mean', 'standard_error', 'note_to_self'])
df_out.to_csv(fname, index=False)

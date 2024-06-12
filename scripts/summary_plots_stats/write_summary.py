# write to a csv file the statistics for each of the items below

import pandas as pd
#import matplotlib.pyplot as plt
from scipy.stats import sem
import numpy as np


# parameters
# ---

# where are the observed metric values stored?
observed_metrics = {
    "raw_c_score": {
        "fname": "../../results/cooccurrence_data/c_score.csv",
        "subset": ("subset_name", "survey_only"),
        "data_col": "c_score"
    },
    "ses_c_score": {
        "fname": "../../results/cooccurrence_data/sim9_c_score.csv",
        "subset": ("subset_name", "survey_only"),
        "data_col": "standardised_effect_size"
    },
    "raw_NODF": {
        "fname": "../../results/nestedness_data/NODF.csv",
        "subset": ("subset_name", "survey_only"),
        "data_col": "NODF"
    },
    "ses_NODF": {
        "fname": "../../results/nestedness_data/sim9_NODF.csv",
        "subset": ("subset_name", "survey_only"),
        "data_col": "standardised_effect_size"
    },
}

# which scenarios will we summarise?
"""
scenarios = [
        {
            'fname': '../../results/cooccurrence_neutral_data/sim9_c_score.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'observed_c_score',
            'note': 'first fit raw c_score',
            'compare_to': "raw_c_score", # so we can compare it to the observed metric value
            },
        ]

"""
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
            'compare_to': "raw_c_score",
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_data/sim9_NODF.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'observed_NODF',
            'note': 'first fit raw NODF',
            'compare_to': "raw_NODF",
            },
        {
            'fname': '../../results/cooccurrence_neutral_data/sim9_c_score.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'standardised_effect_size',
            'note': 'first fit SES c-score',
            'compare_to': "ses_c_score",
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_data/sim9_NODF.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'standardised_effect_size',
            'note': 'first fit SES NODF',
            'compare_to': "ses_NODF",
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
            'compare_to': "raw_NODF",
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_data_fitm/sim9_NODF.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'standardised_effect_size',
            'note': 'fitting m so richness isnt strictly increasing is anti-nested',
            'compare_to': "ses_NODF",
            },
        {
            'fname': '../../results/cooccurrence_neutral_data_fitm/sim9_c_score.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'observed_c_score',
            'note': 'fitting m so richness isnt strictly increasing not much effect on c-score',
            'compare_to': "raw_c_score",
            },
        {
            'fname': '../../results/cooccurrence_neutral_data_fitm/sim9_c_score.csv',
            'subset': [('subset_name', 'survey_only')],
            'data_col': 'standardised_effect_size',
            'note': 'fitting m so richness isnt strictly increasing not much effect on c-score',
            'compare_to': "ses_c_score",
            },
        # an example of contrivance of K and m to bring the metrics closer to observations
        {
            'fname': '../../results/cooccurrence_neutral_data_fitmK/sim9_c_score.csv',
            'subset': [('suffix', '_3')],
            'data_col': 'observed_c_score',
            'note': 'contrived on c-score',
            'compare_to': "raw_c_score",
            },
        {
            'fname': '../../results/cooccurrence_neutral_data_fitmK/sim9_c_score.csv',
            'subset': [('suffix', '_3')],
            'data_col': 'standardised_effect_size',
            'note': 'contrived on c-score',
            'compare_to': "ses_c_score",
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_data_fitmK/sim9_NODF.csv',
            'subset': [('suffix', '_3')],
            'data_col': 'observed_NODF',
            'note': 'contrived on NODF',
            'compare_to': "raw_NODF",
            },
        {
            'fname': '../../results/nestedness_rowpack_neutral_data_fitmK/sim9_NODF.csv',
            'subset': [('suffix', '_3')],
            'data_col': 'standardised_effect_size',
            'note': 'contrived on NODF',
            'compare_to': "ses_NODF",
            },
        ]

# get observed metric values 
# ---


observed_metric_values = dict()
for metric_name, where_stored in observed_metrics.items():

    # get the observed metric's value from where it's stored
    df = pd.read_csv(where_stored["fname"])
    subset_name, subset_value = where_stored["subset"]
    df = df[df[subset_name] == subset_value]
    assert(len(df) == 1)
    observed_metric_value = df[where_stored["data_col"]].iloc[0]

    # save it to our new dictionary
    observed_metric_values[metric_name] = observed_metric_value


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

    # get simulated data
    data_col = scenario['data_col']
    simdata = df[data_col].values

    # find the mean and SE
    simdata_mean = np.mean(simdata)
    simdata_SE = sem(simdata)

    # 95 percentile lower and upper
    simdata_95_lo = np.percentile(simdata, 2.5)
    simdata_95_hi = np.percentile(simdata, 97.5)

    # calculate p-value of observed metric value given simulation results if applicable
    if "compare_to" in scenario:
        # how many simulated archipelagos
        sample_size = len(simdata)

        # get the observed simdata we are comparing to
        metric_name = scenario["compare_to"]
        observed_metric_value = observed_metric_values[metric_name]

        # calculate p-value and situation
        if observed_metric_value > max(simdata):
            lo_p = (sample_size - 1) / sample_size
            up_p = 1 / sample_size
            sign_p = ">"
        elif observed_metric_value < min(simdata):
            lo_p = 1 / sample_size
            up_p = (sample_size-1) / sample_size
            sign_p = "<"
        else:
            lo_p = sum(observed_metric_value >= simdata) / sample_size
            up_p = sum(observed_metric_value <= simdata) / sample_size
            sign_p = "=="
    else:
        # leave empty
        observed_metric_value = None
        lo_p = None
        up_p = None
        sign_p = None


    # store
    note = scenario['note'] 
    m = [fname, subset_str, data_col, observed_metric_value, simdata_mean, simdata_SE, simdata_95_lo, simdata_95_hi, 
         lo_p, up_p, sign_p, note]
    M.append(m)

# write summary statistics to a csv
# ---

fname = '../../results/summary_stats/summary.csv'
df_out = pd.DataFrame.from_records(
    M, 
    columns = ['file_name', 'subset', 'measure', 'observed', 'mean', 'standard_error', '95_pc_lo', '95_pc_hi', 
               'lower_tail_p', 'upper_tail_p', 'p_type', 'note_to_self']
)

df_out.to_csv(fname, index=False)

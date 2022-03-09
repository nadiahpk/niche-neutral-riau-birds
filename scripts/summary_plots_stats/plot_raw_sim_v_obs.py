# plot a histogram of the raw C-scores for the simulated data, and compare it to the raw observed

import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np


# parameters
# ---

# makes the comparisons between figures easier if the x-range is kept the same
xlim_raw_NODF = (50, 90)
xlim_raw_c_score = (0.7, 3)

# a list of plots to create
plot_infos = [ 
        # basic fitting to the data
        { 
            'obs_subset': [('subset_name', 'survey_only')], 
            'sim_subset': [('subset_name', 'survey_only')], 
            'simdata_fname': '../../results/cooccurrence_neutral_data/sim9_c_score.csv',
            'obsdata_fname': '../../results/cooccurrence_data/sim9_c_score.csv',
            'data_col': 'observed_c_score',
            'xlabel': 'raw C-score',
            'plot_fname': '../../results/cooccurrence_neutral_data/sim9_raw_c_score_survey_only.pdf',
            'xlim': xlim_raw_c_score,
            },
        { 
            'obs_subset': [('subset_name', 'survey_only')], 
            'sim_subset': [('subset_name', 'survey_only')], 
            'simdata_fname': '../../results/nestedness_rowpack_neutral_data/sim9_NODF.csv',
            'obsdata_fname': '../../results/nestedness_rowpack_data/sim9_NODF.csv',
            'data_col': 'observed_NODF',
            'xlabel': 'raw NODF',
            'plot_fname': '../../results/nestedness_rowpack_neutral_data/sim9_raw_NODF_survey_only.pdf',
            'xlim': xlim_raw_NODF,
            },
        { 
            'obs_subset': [('subset_name', 'survey_only')], 
            'sim_subset': [('subset_name', 'survey_only')], 
            'simdata_fname': '../../results/cooccurrence_neutral_data_fitm/sim9_c_score.csv',
            'obsdata_fname': '../../results/cooccurrence_data/sim9_c_score.csv',
            'data_col': 'observed_c_score',
            'xlabel': 'raw C-score',
            'plot_fname': '../../results/cooccurrence_neutral_data_fitm/sim9_raw_c_score_survey_only.pdf',
            'xlim': xlim_raw_c_score,
            },
        { 
            'obs_subset': [('subset_name', 'survey_only')], 
            'sim_subset': [('subset_name', 'survey_only')], 
            'simdata_fname': '../../results/nestedness_rowpack_neutral_data_fitm/sim9_NODF.csv',
            'obsdata_fname': '../../results/nestedness_rowpack_data/sim9_NODF.csv',
            'data_col': 'observed_NODF',
            'xlabel': 'raw NODF',
            'plot_fname': '../../results/nestedness_rowpack_neutral_data_fitm/sim9_raw_NODF_survey_only.pdf',
            'xlim': xlim_raw_NODF,
            },
        # contrive m + K
        { 
            'obs_subset': [('subset_name', 'survey_only')], 
            'sim_subset': [('suffix', '_4')], 
            'simdata_fname': '../../results/cooccurrence_neutral_data_fitmK/sim9_c_score.csv',
            'obsdata_fname': '../../results/cooccurrence_data/sim9_c_score.csv',
            'data_col': 'observed_c_score',
            'xlabel': 'raw C-score',
            'plot_fname': '../../results/cooccurrence_neutral_data_fitmK/sim9_raw_c_score_4.pdf',
            'xlim': xlim_raw_c_score,
            },
        { 
            'obs_subset': [('subset_name', 'survey_only')], 
            'sim_subset': [('suffix', '_4')], 
            'simdata_fname': '../../results/nestedness_rowpack_neutral_data_fitmK/sim9_NODF.csv',
            'obsdata_fname': '../../results/nestedness_rowpack_data/sim9_NODF.csv',
            'data_col': 'observed_NODF',
            'xlabel': 'raw NODF',
            'plot_fname': '../../results/nestedness_rowpack_neutral_data_fitmK/sim9_raw_NODF_4.pdf',
            'xlim': xlim_raw_NODF,
            },
        { 
            'obs_subset': [('subset_name', 'survey_only')], 
            'sim_subset': [('suffix', '_3')], 
            'simdata_fname': '../../results/cooccurrence_neutral_data_fitmK/sim9_c_score.csv',
            'obsdata_fname': '../../results/cooccurrence_data/sim9_c_score.csv',
            'data_col': 'observed_c_score',
            'xlabel': 'raw C-score',
            'plot_fname': '../../results/cooccurrence_neutral_data_fitmK/sim9_raw_c_score_3.pdf',
            'xlim': xlim_raw_c_score,
            },
        { 
            'obs_subset': [('subset_name', 'survey_only')], 
            'sim_subset': [('suffix', '_3')], 
            'simdata_fname': '../../results/nestedness_rowpack_neutral_data_fitmK/sim9_NODF.csv',
            'obsdata_fname': '../../results/nestedness_rowpack_data/sim9_NODF.csv',
            'data_col': 'observed_NODF',
            'xlabel': 'raw NODF',
            'plot_fname': '../../results/nestedness_rowpack_neutral_data_fitmK/sim9_raw_NODF_3.pdf',
            'xlim': xlim_raw_NODF,
            },
        ]

for plot_info in plot_infos:


    # get raw for observed data
    # ---

    # read in all the results
    fname = plot_info['obsdata_fname']
    df = pd.read_csv(fname)

    # get the appropriate subset
    subset = plot_info['obs_subset']
    if subset:
        for (col_name, col_val) in plot_info['obs_subset']:
            df = df[df[col_name] == col_val]

    # get the value
    data_col = plot_info['data_col']
    raw_obs = df.iloc[0][data_col]


    # get raw for simulated data
    # ---

    # read in all the results
    fname = plot_info['simdata_fname']
    df = pd.read_csv(fname)

    # get the appropriate subset
    subset = plot_info['sim_subset']
    if subset:
        for (col_name, col_val) in plot_info['sim_subset']:
            df = df[df[col_name] == col_val]

    # all raw
    data_col = plot_info['data_col']
    raw_all = df[data_col].values


    # plot a histogram of raw
    # ---

    # plot the values within and outside the sample range separately
    plt.hist(raw_all, color='blue',   edgecolor='blue',    alpha=0.7, label='niche-neutral model')

    # show where the observed value was
    plt.axvline(raw_obs, color='red', label='observed')

    xlim = plot_info['xlim']
    if xlim:
        plt.xlim(xlim)

    plt.xlabel(plot_info['xlabel'], fontsize='xx-large')
    plt.ylabel('frequency', fontsize='xx-large')
    plt.legend(loc='best', fontsize='large')
    plt.tight_layout()
    plt.savefig(plot_info['plot_fname'])
    plt.close()

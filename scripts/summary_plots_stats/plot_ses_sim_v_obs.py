# plots histograms of the SES scores for the simulated data, and compares it to the SES observed

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# parameters
# ---

# a list of plots to create
plot_infos = [ 
        { 
            'sim_subset': [('subset_name', 'survey_only')], 
            'obs_subset': [('subset_name', 'survey_only')], 
            'simdata_fname': '../../results/cooccurrence_neutral_data/sim9_c_score.csv',
            'obsdata_fname': '../../results/cooccurrence_data/sim9_c_score.csv',
            'xlabel': 'SES C-score',
            'plot_fname': '../../results/cooccurrence_neutral_data/sim9_c_score_survey_only.pdf' 
            },
        { 
            'sim_subset': [('subset_name', 'survey_only')], 
            'obs_subset': [('subset_name', 'survey_only')], 
            'simdata_fname': '../../results/nestedness_rowpack_neutral_data/sim9_NODF.csv',
            'obsdata_fname': '../../results/nestedness_rowpack_data/sim9_NODF.csv',
            'xlabel': 'SES NODF',
            'plot_fname': '../../results/nestedness_rowpack_neutral_data/sim9_NODF_survey_only.pdf' 
            },
        { 
            'sim_subset': [('archipelago_ID', 1)],
            'obs_subset': [('archipelago_ID', 1)],
            'simdata_fname': '../../results/cooccurrence_neutral_vary_K/sim9_c_score_3.csv',
            'obsdata_fname': None,
            'xlabel': 'SES C-Score',
            'plot_fname': '../../results/cooccurrence_neutral_vary_K/sim9_c_score_3_archipelago_1.pdf',
            },
        { 
            'sim_subset': [('archipelago_ID', 9)],
            'obs_subset': [('archipelago_ID', 9)],
            'simdata_fname': '../../results/cooccurrence_neutral_vary_K/sim9_c_score_3.csv',
            'obsdata_fname': None,
            'xlabel': 'SES C-Score',
            'plot_fname': '../../results/cooccurrence_neutral_vary_K/sim9_c_score_3_archipelago_9.pdf',
            },
        { 
            'sim_subset': [('suffix', '_2')],
            'obs_subset': [('suffix', '_2')],
            'simdata_fname': '../../results/cooccurrence_neutral_vary_JK/sim9_c_score.csv',
            'obsdata_fname': None,
            'xlabel': 'SES C-Score',
            'plot_fname': '../../results/cooccurrence_neutral_vary_JK/sim9_c_score_2.pdf',
            },
        { 
            'sim_subset': [('subset_name', 'survey_only')], 
            'obs_subset': [('subset_name', 'survey_only')], 
            'simdata_fname': '../../results/cooccurrence_neutral_data_fitm/sim9_c_score.csv',
            'obsdata_fname': '../../results/cooccurrence_data/sim9_c_score.csv',
            'xlabel': 'SES C-score',
            'plot_fname': '../../results/cooccurrence_neutral_data_fitm/sim9_c_score_survey_only.pdf' 
            },
        { 
            'sim_subset': [('subset_name', 'survey_only')], 
            'obs_subset': [('subset_name', 'survey_only')], 
            'simdata_fname': '../../results/nestedness_rowpack_neutral_data_fitm/sim9_NODF.csv',
            'obsdata_fname': '../../results/nestedness_rowpack_data/sim9_NODF.csv',
            'xlabel': 'SES NODF',
            'plot_fname': '../../results/nestedness_rowpack_neutral_data_fitm/sim9_NODF_survey_only.pdf',
            },
        # contrive m + K
        { 
            'sim_subset': [('suffix', '_4')], 
            'obs_subset': [('subset_name', 'survey_only')], 
            'simdata_fname': '../../results/cooccurrence_neutral_data_fitmK/sim9_c_score.csv',
            'obsdata_fname': '../../results/cooccurrence_data/sim9_c_score.csv',
            'xlabel': 'SES C-score',
            'plot_fname': '../../results/cooccurrence_neutral_data_fitmK/sim9_c_score_4.pdf',
            },
        { 
            'sim_subset': [('suffix', '_4')], 
            'obs_subset': [('subset_name', 'survey_only')], 
            'simdata_fname': '../../results/nestedness_rowpack_neutral_data_fitmK/sim9_NODF.csv',
            'obsdata_fname': '../../results/nestedness_rowpack_data/sim9_NODF.csv',
            'xlabel': 'SES NODF',
            'plot_fname': '../../results/nestedness_rowpack_neutral_data_fitmK/sim9_NODF_4.pdf',
            },
        { 
            'sim_subset': [('suffix', '_3')], 
            'obs_subset': [('subset_name', 'survey_only')], 
            'simdata_fname': '../../results/cooccurrence_neutral_data_fitmK/sim9_c_score.csv',
            'obsdata_fname': '../../results/cooccurrence_data/sim9_c_score.csv',
            'xlabel': 'SES C-score',
            'plot_fname': '../../results/cooccurrence_neutral_data_fitmK/sim9_c_score_3.pdf',
            },
        { 
            'sim_subset': [('suffix', '_3')], 
            'obs_subset': [('subset_name', 'survey_only')], 
            'simdata_fname': '../../results/nestedness_rowpack_neutral_data_fitmK/sim9_NODF.csv',
            'obsdata_fname': '../../results/nestedness_rowpack_data/sim9_NODF.csv',
            'xlabel': 'SES NODF',
            'plot_fname': '../../results/nestedness_rowpack_neutral_data_fitmK/sim9_NODF_3.pdf',
            },
        ]

for plot_info in plot_infos:


    # get SES for observed data
    # ---

    # read in all the results
    fname = plot_info['obsdata_fname']

    if fname:

        df = pd.read_csv(fname)

        # get the appropriate subset
        subset = plot_info['obs_subset']
        if subset:
            for (col_name, col_val) in plot_info['obs_subset']:
                df = df[df[col_name] == col_val]


        # get the value of the standardised effect
        SES_obs = df.iloc[0]['standardised_effect_size']

    else:

        SES_obs = None


    # get SES for simulated data
    # ---

    # read in all the results
    fname = plot_info['simdata_fname']
    df = pd.read_csv(fname)

    # get the appropriate subset
    subset = plot_info['sim_subset']
    if subset:
        for (col_name, col_val) in plot_info['sim_subset']:
            df = df[df[col_name] == col_val]

    # all SES
    SES_all = df['standardised_effect_size'].values


    # plot a histogram of SES
    # ---

    # default min and max range for the SES
    def_min = -2.5; def_max = 2.5

    # find the min and max values from the experiment
    exp_min = min(SES_all); exp_max = max(SES_all)

    # round down and up to the nearest 0.5
    exp_min_rnd = (int(exp_min / 0.5)-1)*.5
    exp_max_rnd = (int(exp_max / 0.5)+1)*.5

    # create bins
    bin_min = min([def_min, exp_min_rnd])
    bin_max = max([def_max, exp_max_rnd])
    bins = np.arange( bin_min, bin_max, 0.2 ) # NOTE bin size here

    # plot the values within and outside the sample range separately
    plt.hist(SES_all, color='blue',   edgecolor='blue',    alpha=0.7, bins=bins, label='niche-neutral model')

    # show the 95%-ile for a normal distribution and the 0
    ninety_five = 1.96
    plt.axvline(ninety_five, ls='dotted', color='black', alpha=0.7)
    plt.axvline(-ninety_five, ls='dotted', color='black', alpha=0.7)
    plt.axvline(0, ls='dotted', color='black', alpha=0.7)

    # show where the observed value was
    if SES_obs:
        plt.axvline(SES_obs, color='red', label='observed')

    plt.xlabel(plot_info['xlabel'], fontsize='xx-large')
    plt.ylabel('frequency', fontsize='xx-large')
    plt.legend(loc='best', fontsize='large')
    plt.tight_layout()
    plt.savefig(plot_info['plot_fname'])
    plt.close()

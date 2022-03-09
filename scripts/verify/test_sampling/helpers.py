import csv
import pandas as pd

# turn the sample_ID row in fname into a presence-absence matrix
def sample2matrix(fname, sample_ID):

    # read in desired record
    # ---

    df_in = pd.read_csv(fname)
    row = df_in[df_in['sample_ID'] == sample_ID ]

    S = row.iloc[0]['no_spp_S']
    H = row.iloc[0]['no_isles_H']
    K = row.iloc[0]['K']

    spp_in_niches = [ row.iloc[0]['no_spp_niche_' + str(idx)] for idx in range(K) ]

    data_row_as_str = row.iloc[0]['presence_absence_matrix_cols_(isles)_concatenated']
    data_row = [ 1 if s == 'p' else 0 for s in data_row_as_str ]


    # turn the data row into a presence-absence matrix
    # ---

    # create island names, species names
    isle_names = [ 'simulated_' + str(h) for h in range(H) ]
    spp_IDs = [ (k, i) for k, spp_in_niche in zip(range(K), spp_in_niches) for i in range(spp_in_niche) ]
    spp_names = [ 'species_' + str(k) + '_' + str(i) for k, i in spp_IDs ]

    # create the data frame
    data = {isle_name: data_row[i:i+S] for i, isle_name in zip(range(0, S*H, S), isle_names) }
    df = pd.DataFrame(data, index=spp_names)

    return(df)

# turn a vector of strings (e.g., read using csv.reader) into numbers
def strings2numbers(vec):

    new_vec = list()
    for s in vec:

        if s == 'inf':
            val = np.inf
        elif '.' in s:
            val = float(s)
        else:
            try:
                val = int(s)
            except:
                val = np.nan

        new_vec.append(val)

    return(new_vec)

def get_maximum_sample_ID(fname):
    '''
    Inputs:
    ---

    fname, str
        Filename of a csv file

    Outputs:
    ---

    max_sample_ID, int
        The maximum valued entry in the 'sample_ID' column
    '''

    with open(fname, newline='') as csvfile:

        reader = csv.reader(csvfile, delimiter=',')

        # which column is the sample_ID in?
        header = next(reader, None)
        idx_sample_ID = header.index('sample_ID')

        sample_ID_strings = list()
        for row_strings in reader:
            sample_ID_strings.append(row_strings[idx_sample_ID])

    sample_IDs = strings2numbers(sample_ID_strings)
    max_sample_ID = max(sample_IDs)

    return(max_sample_ID)

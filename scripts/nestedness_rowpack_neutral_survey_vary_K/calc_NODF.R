# Calculate the NODF for all the samples in the simulated data

source('../../functions/NODF_functions.R')


# parameters
# ---

# which parameter set / suffix to run
suffix <- '_1'

# which K values
KV <- c(1, 3, 5, 7)

# where samples are stored and the parameter values used to generate them
dir_samples <- '../../results/neutral_survey_vary_K/'

# where to put the results
dir_results <- '../../results/nestedness_rowpack_neutral_survey_vary_K/'


# get the island areas so that we can sort islands from largest to smallest
# ---

fname_params <- paste(c(dir_samples, 'archipelago_params', suffix, '.csv'), collapse = '')
df_params <- read.csv(file = fname_params, stringsAsFactors = FALSE)

# all archipelagos have the same number of islands and island sizes, so just take the first row
H <- df_params[1,'H']
island_capacitys <- c()
for (h in 0:H-1){

    s <- paste(c('J_', h), collapse = '')
    island_capacitys <- c(island_capacitys, df_params[1,s])
}

# find the sort order of the island carrying capacities
idx_order <- order(island_capacitys, decreasing = TRUE)


for (K in KV) {

    # get the samples
    # ---

    fname_samples <- paste( c(dir_samples, 'samples', suffix, '_K_', K, '.csv'), collapse = '' )

    df_samples <- read.csv(file = fname_samples, stringsAsFactors = FALSE)
    rownames(df_samples) <- df_samples$sample_ID


    # for each sample, calculate the NODF
    # ---

    sample_IDs <- df_samples$sample_ID

    NODFs <- c()            # a place to store NODFs
    Ss <- c()               # a place to store archipelago richnesses
    df_out <- data.frame()  # a dataframe for storing results
    for ( sample_ID in sample_IDs ){

        # get the row of interest and basic info
        row <- df_samples[sample_ID,] 
        S <- row$S
        Ss <- c(Ss, S)

        # turn the concatenated presence-absence matrix into concatenated list of 1s and 0s

        pamatrix_as_char <- row$presence_absence_matrix_cols_isles_concatenated
        pamatrix_as_vec <- strsplit(pamatrix_as_char, '')[[1]]

        data_row <- c()
        for ( letter in pamatrix_as_vec ){

            if ( letter == 'p' ){

                data_row <- c(data_row, 1)
                
            } else {

                data_row <- c(data_row, 0)

            }
        }

        # turn the list of 1s and 0s into a matrix suitable for calculating the NODF
        pamatrix <- matrix(data_row, nrow = S, ncol = H, byrow=FALSE)

        # sort the matrix
        pamatrix <- pamatrix[,idx_order]    # sort columns in order from large to small island area
        pamatrix <- pack_rows(pamatrix)     # sort rows in order from most common to least common species

        # calculate and store the NODF
        NODF_sample <- calc_NODF(pamatrix)
        NODFs <- c(NODFs, NODF_sample)

        new_row <- data.frame(
                              sample_ID = sample_ID,
                              S = S,
                              H = H,
                              NODF = NODF_sample
                              )
        df_out <- rbind(df_out, new_row)

    }


    # write results to a csv
    # ---

    fname_out <- paste(c(dir_results, 'NODF', suffix, '_K_', K, '.csv'), collapse = '')
    write.csv(df_out, fname_out, row.names = FALSE)

}

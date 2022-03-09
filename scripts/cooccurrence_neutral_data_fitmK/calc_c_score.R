# Calculate the C-score for all the samples in the simulated data
library(EcoSimR)


# parameters
# ---

# suffix used
suffix <- '_4'

# where samples are stored
dir_samples <- '../../results/neutral_data_fitmK/'

# where to put results
dir_results <- '../../results/cooccurrence_neutral_data_fitmK/'


# get the samples
# ---

fname_samples <- paste( 
                  c(dir_samples, 'samples_archipelago', suffix, '.csv'), 
                  collapse = '' )

df_samples <- read.csv(file = fname_samples, stringsAsFactors = FALSE)
rownames(df_samples) <- df_samples$sample_ID


# for each sample, calculate the c_score
# ---

c_scores <- c() # a place to store them
sample_IDs <- df_samples$sample_ID
Ss <- c()

df_out <- data.frame()
for ( sample_ID in sample_IDs ){

    # get the row of interest and basic info
    row <- df_samples[sample_ID,] 
    S <- row$S
    Ss <- c(Ss, S)
    H <- row$H

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

    # turn the list of 1s and 0s into a matrix suitable for calculating the c-score

    pamatrix <- matrix(data_row, nrow = S, ncol = H, byrow=FALSE)
    c_score_sample <- c_score(pamatrix)

    # store c-score
    c_scores <- c(c_scores, c_score_sample)

    new_row <- data.frame(
                          sample_ID = sample_ID,
                          S = S,
                          H = H,
                          c_score = c_score_sample
                          )
    df_out <- rbind(df_out, new_row)

}

# write results to a csv
# ---

fname_out <- paste(c(dir_results, 'c_score', suffix, '.csv'), collapse = '')
write.csv(df_out, fname_out, row.names = FALSE)


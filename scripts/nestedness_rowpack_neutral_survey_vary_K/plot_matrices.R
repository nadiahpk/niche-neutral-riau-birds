# plot some example matrices

source('../../functions/NODF_functions.R')


# parameters
# ---

# which matrices to plot
suffix <- '_1'          # which parameter set / suffix to run
KV <- c(1, 3, 5, 7)     # which K values, number of niches
sample_IDs <- c(1)      # which samples

# for the randomised matrix, how many randomisation steps to take
burn_in <- 5000


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


# for each K, for each sample, plot the observed matrix and a randomised matrix
# ---

for (K in KV) {

    # get the samples
    fname_samples <- paste( c(dir_samples, 'samples', suffix, '_K_', K, '.csv'), collapse = '' )
    df_samples <- read.csv(file = fname_samples, stringsAsFactors = FALSE)
    rownames(df_samples) <- df_samples$sample_ID

    for (sample_ID in sample_IDs) {


        # get the sample matrix ("observed", though the result of neutral model)
        # ---

        # get the row of interest and basic info
        row <- df_samples[sample_ID,] 
        S <- row$S
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

        # turn the list of 1s and 0s into a matrix suitable for calculating NODF
        df <- matrix(data_row, nrow = S, ncol = H, byrow=FALSE)

        # sort the matrix
        df <- df[,idx_order]    # sort columns in order from large to small island area
        df <- pack_rows(df)     # sort rows in order from most common to least common species


        # plot observed matrix
        # ---

        NODF <- calc_NODF(df)

        fname_plot <- paste(c(dir_results, 'matrix_obs', suffix, '_K_', K, '_sample_ID_', sample_ID, '.pdf'), collapse = '')
        pdf(fname_plot, height=(nrow(df)/10), width=(ncol(df)/10))
        par(mar=c(0,0,0,0))
        image(1:ncol(df), 1:nrow(df), t(apply(df, 2, rev)), col = c("white", "blue"), asp=1, axes=F)
        dev.off()


        # plot randomised matrix
        # ---

        for (i in 1:burn_in) {
            df <- sim9_single(df)
        }

        NODF <- calc_NODF(df)

        fname_plot <- paste(c(dir_results, 'matrix_rand', suffix, '_K_', K, '_sample_ID_', sample_ID, '.pdf'), collapse = '')
        pdf(fname_plot, height=(nrow(df)/10), width=(ncol(df)/10))
        par(mar=c(0,0,0,0))
        image(1:ncol(df), 1:nrow(df), t(apply(df, 2, rev)), col = c("white", "blue"), asp=1, axes=F)
        dev.off()

    }
}

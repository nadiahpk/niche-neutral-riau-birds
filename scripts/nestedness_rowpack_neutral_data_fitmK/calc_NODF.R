# Calculate the NODF for all the samples in the simulated data

source('../../functions/NODF_functions.R')



# parameters
# ---

# identifiers of experiment
subset_name <- 'survey_only'
rho <- 1700
suffix <- '_4'

# where samples are stored
dir_samples <- '../../results/neutral_data_fitmK/'

# where the island name ordering for subsets are stored
dir_processed <- '../../data/processed/'

# where to put results
dir_results <- '../../results/nestedness_rowpack_neutral_data_fitmK/'


# get the sort order for the islands (largest area to smallest)
# ---

# get names of islands
fname_islands <- paste(c(dir_processed, 'island_subsets/', subset_name, '.csv'), collapse = '')
df_islands <- read.csv(file = fname_islands, stringsAsFactors = FALSE)
island_names <- df_islands$island_name

# find the area of each island of interest

fname <- '../../data/processed/island_area.csv'     # read in island areas
df_area <- read.csv(file = fname)

rownames(df_area) <- df_area$island_name            # make the island name the index - convenient later
island_areas <- c()
for (island_name in island_names) {
    island_areas <- c(island_areas, df_area[island_name, 'area_sq_km'])
}

# find the sort order of the island_areas
idx_order <- order(island_areas, decreasing = TRUE)


# get the samples
# ---

fname_samples <- paste( 
                  c(dir_samples, 'samples_archipelago', suffix, '.csv'), 
                  collapse = '' )

df_samples <- read.csv(file = fname_samples, stringsAsFactors = FALSE)
rownames(df_samples) <- df_samples$sample_ID


# for each sample, calculate the NODF
# ---

NODFs <- c() # a place to store them
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

fname_out <- paste(c(dir_results, 'NODF', suffix, '.csv'), collapse = '')
write.csv(df_out, fname_out, row.names = FALSE)


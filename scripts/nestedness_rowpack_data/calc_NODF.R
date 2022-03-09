# Calculate the NODF for all subsets in the data, but only pack by row, column order is according to island area

source('../../functions/NODF_functions.R')


# parameters
# ---

# which data shall we do
dirname_subsets <- '../../data/processed/island_subsets/'
# subset_name <- 'survey_only'
subset_name <- 'peninsula_only'

# where to put the results
dirname_out <- '../../results/nestedness_rowpack_data/'


# NOTE could loop this over subset_names if you want


# read the presence-absence matrix
# ---

fname_sub <- paste( 
                  c(dirname_subsets, 'island_bird_presence_absence_', subset_name, '.csv'), 
                  collapse = '' )

df_sub <- read.csv(file = fname_sub)


# reorder the presence-matrix so that largest island is leftmost
# ---

df_sub <- sort_by_island_area(df_sub)


# calculate observed NODF after row packing only
# ---

M <- as.matrix(df_sub[,2:ncol(df_sub)])
NODF <- calc_rowpacked_NODF(M)


# save to a csv file
# ---

NODFs = c(NODF)
subsets = c(subset_name)

df_out <- data.frame(subset_name = subsets, NODF = NODFs)

fname_out <- paste( c(dirname_out, 'NODF.csv'), collapse='' )

if (file.exists(fname_out)) {

    write.table(df_out, file = fname_out, sep = ",", append = TRUE, col.names = FALSE, row.names = FALSE)

} else {

    write.csv(df_out, fname_out, row.names = FALSE)

}


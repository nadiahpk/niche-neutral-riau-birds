# plot observed data matrix after rowpacked

source('../../functions/NODF_functions.R')


# parameters
# ---

# which data shall we do
dirname_subsets <- '../../data/processed/island_subsets/'
# subset_names <- c('survey_only', 'peninsula_only')
subset_names <- c('survey_only')

# where to put the results
dir_results <- '../../results/nestedness_rowpack_data/'


# for each subset, plot the matrix
# ---

for (subset_name in subset_names){

    # read the presence-absence matrix
    fname_sub <- paste( 
                      c(dirname_subsets, 'island_bird_presence_absence_', subset_name, '.csv'), 
                      collapse = '' )
    df_sub <- read.csv(file = fname_sub)

    # reorder the presence-matrix so that largest island is leftmost
    df_sub <- sort_by_island_area(df_sub)
    df <- as.matrix(df_sub[,2:ncol(df_sub)])

    # sort rows in order from most common to least common species
    df <- pack_rows(df, T)

    # plot observed matrix
    fname_plot <- paste(c(dir_results, 'matrix_', subset_name, '.pdf'), collapse = '')
    pdf(fname_plot, height=(nrow(df)/10), width=(ncol(df)/10))
    par(mar=c(0,0,0,0))
    image(1:ncol(df), 1:nrow(df), t(apply(df, 2, rev)), col = c("white", "blue"), asp=1, axes=F)
    dev.off()

}

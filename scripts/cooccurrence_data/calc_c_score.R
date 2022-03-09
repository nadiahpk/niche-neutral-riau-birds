# Calculate the C-score for all subsets in the data

library(EcoSimR)


# parameters
# ---

# which data shall we do
dirname_subsets <- '../../data/processed/island_subsets/'
# subset_name <- 'survey_only'
subset_name <- 'peninsula_only'

# where to put the results
dirname_out <- '../../results/cooccurrence_data/'

# NOTE could loop this over subset_names if you want

# read the presence-absence matrix
# ---

fname_sub <- paste( 
                  c(dirname_subsets, 'island_bird_presence_absence_', subset_name, '.csv'), 
                  collapse = '' )

df_sub <- read.csv(file = fname_sub)


# calculate observed C-score
# ---

result <- cooc_null_model(speciesData = df_sub, burn_in = 1, nReps = 1, suppressProg = TRUE)
c_score <- result$Obs


# save to a csv file
# ---

c_scores = c(c_score)
subsets = c(subset_name)

df_out <- data.frame(subset_name = subsets, c_score = c_scores)

fname_out <- paste( c(dirname_out, 'c_score.csv'), collapse='' )

if (file.exists(fname_out)) {

    write.table(df_out, file = fname_out, sep = ",", append = TRUE, col.names = FALSE, row.names = FALSE)

} else {

    write.csv(df_out, fname_out, row.names = FALSE)

}

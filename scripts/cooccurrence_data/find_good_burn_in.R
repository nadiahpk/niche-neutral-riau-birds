# Find a reasonable level of burn-in for the randomisation of the presence-absence matrices with C-Score metric
# Create plots of burn-in for visual inspection
# Also estimate effective sample sizes

library(coda)
library(EcoSimR)


# parameters
# ---

# a first guess at what would be a sufficient burn-in (use the plot to verify and increase as needed)
burn_in <- 50000 # to be verified with burn-in plots

# which data shall we do
dirname_subsets <- '../../data/processed/island_subsets/'
#subset_name <- 'survey_only'
subset_name <- 'peninsula_only'

# where to put the results
dirname_out <- '../../results/cooccurrence_data/'


# read the presence-absence matrix
# ---

fname_sub <- paste( 
                  c(dirname_subsets, 'island_bird_presence_absence_', subset_name, '.csv'), 
                  collapse = '' )

df_sub <- read.csv(file = fname_sub)


# do a burn-in
# ---

result <- cooc_null_model(speciesData = df_sub, burn_in = burn_in, suppressProg = TRUE)


# save the result
# ---

# make the plots
fname_out <- paste( c(dirname_out, 'burn_in_', subset_name, '.pdf'), collapse='' )
pdf(fname_out)
plot(result, type = 'burn_in')
dev.off()

# save the final matrix to a file
fname_out <- paste( c(dirname_out, 'burnt_in_', subset_name, '.csv'), collapse='' )
write.csv(result$Randomized.Data, fname_out, row.names = FALSE)

# check the effective sample size of the (default) 1000 samples returned
sample <- mcmc(result$Sim)
cat('Effective sample size of ', subset_name, ': ', effectiveSize(sample), '\n')
# ~ 9

# Find a reasonable level of burn-in for the randomisation of the presence-absence matrices with NODF metric
# Create plots of burn-in for visual inspection
# Also estimate effective sample sizes

library(coda)       # effectiveSize()
library(EcoSimR)    # sim9_single()
source('../../functions/NODF_functions.R')


# parameters
# ---

# a first guess at what would be a sufficient burn-in (use the plot to verify and increase as needed)
burn_in <- 5000 # to be verified with burn-in plots

# which data shall we do
dirname_subsets <- '../../data/processed/island_subsets/'
#subset_name <- 'survey_only'
subset_name <- 'peninsula_only'

# where to put the results
dirname_out <- '../../results/nestedness_rowpack_data/'


# read the presence-absence matrix
# ---

fname_sub <- paste( 
                  c(dirname_subsets, 'island_bird_presence_absence_', subset_name, '.csv'), 
                  collapse = '' )
df_sub <- read.csv(file = fname_sub)

# reorder the columns so that larger area islands are to the left
df_sub <- sort_by_island_area(df_sub)

# I need only columns 2:end to make the matrix
pamatrix <- as.matrix(df_sub[,2:ncol(df_sub)])


# do a burn-in
# ---

# first, get observed value
NODF_obs <- calc_rowpacked_NODF(pamatrix)

# for each step, randomise and find new value, put into 
NODF_samples <- c()
for (sample_num in 1:burn_in){

    # randomise the matrix
    pamatrix <- sim9_single(pamatrix)

    # sample this NODF and append
    NODF_sample <- calc_rowpacked_NODF(pamatrix)
    NODF_samples <- c(NODF_samples, NODF_sample)

}


# check the effective sample size 
# ---

cat('Effective sample size of ', subset_name, ': ', effectiveSize(NODF_samples), '\n')
# Effective sample size of  survey_only :  11.77821
# Effective sample size of  peninsula_only :  14.10725


# save the final matrix to a file
# ---

fname_out <- paste( c(dirname_out, 'burnt_in_', subset_name, '.csv'), collapse='' )
write.csv(pamatrix, fname_out, row.names = FALSE)


# save the plot
# ---

# name the plot and prepare pdf device
fname_out <- paste( c(dirname_out, 'burn_in_', subset_name, '.pdf'), collapse='' )
pdf(fname_out)

# this section of code is borrowed from EcoSimr package
par(mfrow = c(1,1))
v <- NODF_samples       # must be the list of sample values
z <- NODF_obs           # observed value
v <- c(z,v)             # list of actual metric values including the observation
plot(x = 1:length(v),   # plot the trace
     y = v,
     xlab = "Iteration",
     ylab = "Index", 
     las = 1,
     type = "l",
     col = "royalblue3")
abline(h = z, col = "red3")                     # plot a red line for the observation
lines(lowess(1:length(v),v), col="gray",lwd=4)  # lowess line (x,y)

# close pdf device
dev.off()


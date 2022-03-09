# Find a reasonable level of burn-in for the randomisation of the presence-absence matrices with NODF metric
# Create plots of burn-in for visual inspection
# Also estimate effective sample sizes

source('../../functions/NODF_functions.R')
library(coda) # effectiveSize()
library(EcoSimR) # sim9_single

# parameters
# ---

# which sample_ID to do
sample_ID <- 1

# name of subset, rho used
subset_name <- 'survey_only'
rho <- 1700

# a first guess at what would be a sufficient burn-in (use the plot to verify and increase as needed)
burn_in <- 5000 # to be verified with burn-in plots
# -- 2000 looks adequate

# where samples are stored
dir_samples <- '../../results/neutral_data/'

# where to put results
dir_results <- '../../results/nestedness_neutral_data/'


# read the synthetic presence-absence matrix
# ---

# get all the samples
fname_samples <- paste( 
                  c(dir_samples, 'samples_', subset_name, '_rho', rho, '.csv'), 
                  collapse = '' )

df_samples <- read.csv(file = fname_samples, stringsAsFactors = FALSE)
rownames(df_samples) <- df_samples$sample_ID

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

# turn the list of 1s and 0s into a matrix suitable for calculating the c-score

pamatrix <- matrix(data_row, nrow = S, ncol = H, byrow=FALSE)


# do a burn-in
# ---

# first, get observed value
NODF_obs <- calc_packed_NODF(pamatrix)

# for each step, randomise and find new value, put into 
NODF_samples <- c()
for (sample_num in 1:burn_in){

    # randomise the matrix
    pamatrix <- sim9_single(pamatrix)

    # sample this NODF and append
    NODF_sample <- calc_packed_NODF(pamatrix)
    NODF_samples <- c(NODF_samples, NODF_sample)

}


# check the effective sample size 
# ---

cat('Effective sample size of ', subset_name, ': ', effectiveSize(NODF_samples), '\n')


# save the final matrix to a file
# ---

fname_out <- paste( c(dir_results, 'burnt_in_', subset_name, '_sample_ID_', sample_ID, '.csv'), collapse='' )
write.csv(pamatrix, fname_out, row.names = FALSE)


# save the plot
# ---

# name the plot and prepare pdf device
fname_out <- paste( c(dir_results, 'burn_in_', subset_name, '_sample_ID_', sample_ID, '.pdf'), collapse='' )
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

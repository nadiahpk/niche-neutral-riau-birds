# Find a reasonable level of burn-in for the randomisation of the presence-absence matrices with C-Score metric
# Create plots of burn-in for visual inspection
# Also estimate effective sample sizes

library(coda)
library(EcoSimR)

# parameters
# ---

# which archipelago to do
suffix <- '_3'
arch_ID <- 5

# a first guess at what would be a sufficient burn-in (use the plot to verify and increase as needed)
burn_in <- 10000 # to be verified with burn-in plots
# -- 2000 looks adequate

# where samples are stored
dir_samples <- '../../results/neutral_vary_K/'

# where to put results
dir_results <- '../../results/cooccurrence_neutral_vary_K/'


# read the synthetic presence-absence matrix
# ---

# get all the samples
fname_samples <- paste( 
                  c(dir_samples, 'samples', suffix, '_archipelago_', arch_ID, '.csv'), 
                  collapse = '' )

df_samples <- read.csv(file = fname_samples, stringsAsFactors = FALSE)


# get the first row matching the archipelago_ID to do the burnin on it
# ---

df_samples <- subset(df_samples, archipelago_ID == arch_ID)
row <- df_samples[1,]


# turn the concatenated presence-absence matrix into concatenated list of 1s and 0s
# ---

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
# ---

S <- row$S
H <- row$H
pamatrix <- matrix(data_row, nrow = S, ncol = H, byrow=FALSE)


# do a burn-in
# ---

result <- cooc_null_model(speciesData = pamatrix, burn_in = burn_in, suppressProg = TRUE)


# save the result
# ---

# make the plots
fname_out <- paste( c(dir_results, 'burn_in', suffix, '_archipelago_ID_', arch_ID, '.pdf'), collapse='' )
pdf(fname_out)
plot(result, type = 'burn_in')
dev.off()

# save the final matrix to a file
fname_out <- paste( c(dir_results, 'burnt_in', suffix, '_archipelago_ID_', arch_ID, '.csv'), collapse='' )
write.csv(result$Randomized.Data, fname_out, row.names = FALSE)

# check the effective sample size of the (default) 1000 samples returned
sample <- mcmc(result$Sim)
cat('Effective sample size of ', arch_ID, ': ', effectiveSize(sample), '\n')
# ~ 9


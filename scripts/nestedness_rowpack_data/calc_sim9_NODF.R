# Compare the observed NODF to randomised (using fixed-fixed) matrices 

source('../../functions/NODF_functions.R')
library(coda) # effectiveSize()
library(EcoSimR) # sim9_single


# parameters
# ---

# which data shall we do
# subset_name <- 'survey_only'
subset_name <- 'peninsula_only'

# where to find the burnt-in matrix
dir_burn <- '../../results/nestedness_rowpack_data/'

# where to find the data NODF and put the results
dir_results <- '../../results/nestedness_rowpack_data/'

# how many randomisation steps to take per sample
desired_eff_sample_size = 1000  # desired effective sample size
step_check_eff = 100            # how often to check the effective sample size
rands_per_sample = 100          # how many samples before checking effective sample size

# a quick run for debugging
#desired_eff_sample_size <- 10  # desired effective sample size
#rands_per_sample <- 100          # how many randomisation steps before sampling NODF
#step_check_eff <- 100            # how many samples before checking effective sample size


# NOTE could put a loop over subset_names here
# ---

df_out <- data.frame()


# get the observed NODF for each subset we're doing
# ---

fname_NODFs <- paste( c(dir_results, 'NODF.csv'), collapse = '' )
df_NODFs <- read.csv(file = fname_NODFs)
obs_NODF <- df_NODFs[df_NODFs$subset_name == subset_name,]$NODF # the observe NODF for this subset


# obtain a randomised sample of NODF that exceeds the desired effective sample size
# ---

# get the burnt-in starting matrix 
fname_burnt <- paste(c(dir_burn, 'burnt_in_', subset_name, '.csv'), collapse = '')
df <- as.matrix( read.csv(file = fname_burnt) ) # NODF() takes a matrix

# order the 

# prepare a list to receive NODF samples
NODF_i <- calc_rowpacked_NODF(df)
NODFs <- c(NODF_i)

# do eff_sample_size draws to start with, because we'll need at least that many
for (sam in 2:desired_eff_sample_size) {

    # randomise the matrix rands_per_sample times
    for (randomisation in 1:rands_per_sample) {
        df <- sim9_single(df)
    }

    # sample this NODF and append
    NODFs <- c(NODFs, calc_rowpacked_NODF(df))

}

# check the effective sample size and do more draws as needed
eff_sample_size <- effectiveSize(NODFs)
no_draws <- 1

while (eff_sample_size < desired_eff_sample_size) {

    # randomise the matrix rands_per_sample times
    for (randomisation in 1:rands_per_sample) {
        df <- sim9_single(df)
    }

    # sample this NODF and append
    NODFs <- c(NODFs, calc_rowpacked_NODF(df))

    no_draws <- no_draws + 1

    # update effective sample size occassionally for checking
    if (no_draws %% step_check_eff == 0) {
        eff_sample_size <- effectiveSize(NODFs)
    }

}

# calculate metrics on sample
# ---

# borrowing from code from https://github.com/GotelliLab/EcoSimR/blob/master/R/coccurrence_null.R

# about the sample
mean_NODF <- mean(NODFs)
act_sample_size <- length(NODFs)

# p-values
if (obs_NODF > max(NODFs)) {

    lo_p <- (act_sample_size - 1)/act_sample_size
    up_p <- 1/act_sample_size
    sign_p <- '>'

} else if(obs_NODF < min(NODFs)) {

    lo_p <- 1/act_sample_size
    up_p <- (act_sample_size - 1)/act_sample_size
    sign_p <- '<'

} else {

    lo_p <- sum(obs_NODF >= NODFs)/act_sample_size
    up_p <- sum(obs_NODF <= NODFs)/act_sample_size
    sign_p <- '=='

}

# standardised effect size
ses <- (obs_NODF - mean(NODFs))/sd(NODFs)


# store results
# ---

new_row <- data.frame(
                      subset_name = subset_name,
                      observed_NODF = obs_NODF,
                      actual_sample_size = act_sample_size,
                      effective_sample_size = eff_sample_size,
                      mean_NODF = mean_NODF,
                      lower_tail_p = lo_p,
                      upper_tail_p = up_p,
                      p_type = sign_p,
                      standardised_effect_size = ses
                      )

df_out <- rbind(df_out, new_row)


# plot histogram
# ---

fname_hist <- paste(c(dir_results, 'sim9_NODF_', subset_name, '.pdf'), collapse = '')
pdf(fname_hist)
opar <- par(no.readonly = TRUE)
par(mfrow = c(1, 1))
par(cex = 1, cex.axis = 1.5, cex.main = 1, cex.lab = 1.6)
par(mar = c(5,6,4,2)+0.1)
hist(NODFs,
     breaks = 20,
     col ="royalblue3",
     xlab = "NODF",
     ylab = "Frequency",
     main = "",
     xlim = range(c(NODFs, obs_NODF)))
abline(v = obs_NODF, col = "red", lty = "solid", lwd = 2.5)
abline(v = quantile(NODFs, c(0.05, 0.95)),   col = "black", lty = "dashed", lwd = 2.5)
abline(v = quantile(NODFs, c(0.025, 0.975)), col = "black", lty = "dotted", lwd = 2.5)
dev.off()

# NOTE the loop over subset_names would end here


# write statistical results to a csv
# ---

fname_out <- paste(c(dir_results, 'sim9_NODF.csv'), collapse = '')

if (file.exists(fname_out)) {

    write.table(df_out, file = fname_out, sep = ",", append = TRUE, col.names = FALSE, row.names = FALSE)

} else {

    write.csv(df_out, fname_out, row.names = FALSE)

}


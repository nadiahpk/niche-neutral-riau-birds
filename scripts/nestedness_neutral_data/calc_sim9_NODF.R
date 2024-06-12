# Compare the observed NODF to randomised (using fixed-fixed) matrices 

library(coda)
library(EcoSimR)

# parameters
# ---

burn_in <- 2000 # verified this is adequate with some examples

#sample_IDs <- 3:5       # which sample_IDs to do
#plot_histogram <- TRUE  # whether or not to plot a histogram for each
sample_IDs <- 6:100      # which sample_IDs to do
plot_histogram <- FALSE  # whether or not to plot a histogram for each

# name of subset, rho used
subset_name <- 'survey_only'
# subset_name <- 'peninsula_only'
rho <- 1700

# where samples are stored
dir_samples <- '../../results/neutral_data/'

# where to put results
dir_results <- '../../results/nestedness_neutral_data/'

# how many randomisation steps to take per sample
desired_eff_sample_size = 1000  # desired effective sample size
step_check_eff = 100            # how often to check the effective sample size
rands_per_sample = 100          # how many samples before checking effective sample size


# read in all the synthetic presence-absence matrices
# ---

# get all the samples
fname_samples <- paste( 
                  c(dir_samples, 'samples_', subset_name, '_rho', rho, '.csv'), 
                  collapse = '' )

df_samples <- read.csv(file = fname_samples, stringsAsFactors = FALSE)
rownames(df_samples) <- df_samples$sample_ID


# loop over samples and calculate NODF
# ---

df_out <- data.frame()
for (sample_ID in sample_IDs) {

    print(paste( c('calculating sample ', sample_ID), collapse='' ))

    # get the row of interest and basic info
    # ---

    row <- df_samples[sample_ID,] 
    S <- row$S
    H <- row$H


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
    df <- matrix(data_row, nrow = S, ncol = H, byrow=FALSE)


    # observed NODF
    # ---

    obs_NODF <- calc_packed_NODF(df)


    # burn in 
    # ---

    for (i in 1:burn_in) {
        df <- sim9_single(df)
    }


    # obtain a randomised sample of NODFs that exceeds the desired effective sample size
    # ---

    # prepare a list to receive NODF samples
    NODF_i <- calc_packed_NODF(df)
    NODFs <- c(NODF_i)

    # do eff_sample_size draws to start with, because we'll need at least that many
    for (sam in 2:desired_eff_sample_size) {

        # randomise the matrix rands_per_sample times
        for (randomisation in 1:rands_per_sample) {
            df <- sim9_single(df)
        }

        # sample this NODF and append
        NODFs <- c(NODFs, calc_packed_NODF(df))

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
        NODFs <- c(NODFs, calc_packed_NODF(df))

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
                          sample_ID = sample_ID,
                          rho = rho,
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


    if (plot_histogram) {

        # plot histogram
        # ---

        fname_hist <- paste(
                            c(dir_results, 'sim9_NODF_', subset_name, '_sample_ID_', sample_ID, '.pdf'), 
                            collapse = '')
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
    }

}


# write statistical results to a csv
# ---

fname_out <- paste(c(dir_results, 'sim9_NODF.csv'), collapse = '')

if (file.exists(fname_out)) {

    write.table(df_out, file = fname_out, sep = ",", append = TRUE, col.names = FALSE, row.names = FALSE)

} else {

    write.csv(df_out, fname_out, row.names = FALSE)

}


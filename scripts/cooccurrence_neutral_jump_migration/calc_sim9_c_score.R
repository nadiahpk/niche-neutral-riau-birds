# Compare the observed C-scores to randomised (using fixed-fixed) matrices 

library(coda)
library(EcoSimR)


# parameters
# ---

# which archipelago to do
suffix <- '_4'
arch_ID <- 2

plot_histogram <- FALSE # whether or not to plot a histogram for each
burn_in <- 2000 # verified this is adequate with some examples

# which sample_IDs to do
sample_IDs <- 1:30

# where samples are stored
dir_samples <- '../../results/neutral_jump_migration/'

# where to put results
dir_results <- '../../results/cooccurrence_neutral_jump_migration/'

# how many randomisation steps to take per sample
desired_eff_sample_size <- 1000  # desired effective sample size
step_check_eff <- 100            # how often to check the effective sample size
rands_per_sample <- 100          # how many samples before checking effective sample size


# read the synthetic presence-absence matrix matching the archipelagos
# ---

# get all the samples
fname_all_samples <- paste( 
                  c(dir_samples, 'samples', suffix, '.csv'), 
                  collapse = '' )

df_all_samples <- read.csv(file = fname_all_samples, stringsAsFactors = FALSE)


# get this archipelago's samples
# ---

print(paste( c('calculating archipelago ', arch_ID), collapse='' ))

df_samples <- subset(df_all_samples, archipelago_ID == arch_ID)
rownames(df_samples) <- df_samples$sample_ID # index by sample ID for convenience

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


    # observed c-score
    # ---

    obs_c_score <- c_score(df)


    # burn in 
    # ---

    for (i in 1:burn_in) {
        df <- sim9_single(df)
    }


    # obtain a randomised sample of C-Scores that exceeds the desired effective sample size
    # ---

    # prepare a list to receive c-score samples
    c_score_i <- c_score(df)
    c_scores <- c(c_score_i)

    # do eff_sample_size draws to start with, because we'll need at least that many
    for (sam in 2:desired_eff_sample_size) {

        # randomise the matrix rands_per_sample times
        for (randomisation in 1:rands_per_sample) {
            df <- sim9_single(df)
        }

        # sample this C-score and append
        c_scores <- c(c_scores, c_score(df))

    }

    # check the effective sample size and do more draws as needed
    eff_sample_size <- effectiveSize(c_scores)
    no_draws <- 1

    while (eff_sample_size < desired_eff_sample_size) {

        # randomise the matrix rands_per_sample times
        for (randomisation in 1:rands_per_sample) {
            df <- sim9_single(df)
        }

        # sample this C-score and append
        c_scores <- c(c_scores, c_score(df))

        no_draws <- no_draws + 1

        # update effective sample size occassionally for checking
        if (no_draws %% step_check_eff == 0) {
            eff_sample_size <- effectiveSize(c_scores)
        }

    }


    # calculate metrics on sample
    # ---

    # borrowing from code from https://github.com/GotelliLab/EcoSimR/blob/master/R/coccurrence_null.R

    # about the sample
    mean_c_score <- mean(c_scores)
    act_sample_size <- length(c_scores)

    # p-values
    if (obs_c_score > max(c_scores)) {

        lo_p <- (act_sample_size - 1)/act_sample_size
        up_p <- 1/act_sample_size
        sign_p <- '>'

    } else if(obs_c_score < min(c_scores)) {

        lo_p <- 1/act_sample_size
        up_p <- (act_sample_size - 1)/act_sample_size
        sign_p <- '<'

    } else {

        lo_p <- sum(obs_c_score >= c_scores)/act_sample_size
        up_p <- sum(obs_c_score <= c_scores)/act_sample_size
        sign_p <- '=='

    }

    # standardised effect size
    ses <- (obs_c_score - mean(c_scores))/sd(c_scores)


    # store results
    # ---

    new_row <- data.frame(
                          archipelago_ID = arch_ID,
                          sample_ID = sample_ID,
                          observed_c_score = obs_c_score,
                          actual_sample_size = act_sample_size,
                          effective_sample_size = eff_sample_size,
                          mean_c_score = mean_c_score,
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
                            c(dir_results, 'histogram_c_score/sim9_c_score_', arch_ID, '_sample_ID_', sample_ID, '.pdf'), 
                            collapse = '')
        pdf(fname_hist)
        opar <- par(no.readonly = TRUE)
        par(mfrow = c(1, 1))
        par(cex = 1, cex.axis = 1.5, cex.main = 1, cex.lab = 1.6)
        par(mar = c(5,6,4,2)+0.1)
        hist(c_scores,
             breaks = 20,
             col ="royalblue3",
             xlab = "C-Score",
             ylab = "Frequency",
             main = "",
             xlim = range(c(c_scores, obs_c_score)))
        abline(v = obs_c_score, col = "red", lty = "solid", lwd = 2.5)
        abline(v = quantile(c_scores, c(0.05, 0.95)),   col = "black", lty = "dashed", lwd = 2.5)
        abline(v = quantile(c_scores, c(0.025, 0.975)), col = "black", lty = "dotted", lwd = 2.5)
        dev.off()
    }

}


# write statistical results to a csv
# ---

fname_out <- paste(c(dir_results, 'sim9_c_score.csv'), collapse = '')

if (file.exists(fname_out)) {

    write.table(df_out, file = fname_out, sep = ",", append = TRUE, col.names = FALSE, row.names = FALSE)

} else {

    write.csv(df_out, fname_out, row.names = FALSE)

}


# Compare the observed C-scores to neutral-model matrices

library(coda)
library(EcoSimR)


# parameters
# ---

# which data shall we do
subset_name <- 'survey_only'
# subset_name <- 'peninsula_only'

# where to find the observed c-score and put the results
dir_results <- '../../results/cooccurrence_data/'

# where to find the neutral model data c-scores
dir_neut <- '../../results/cooccurrence_neutral_data/'

rho = 1700 # parameter used to generate the neutral matrices


# NOTE could put a loop over subset_names here
# ---

df_out <- data.frame()


# get the observed C-scores for each subset we're doing
# ---

fname_cscores <- paste( c(dir_results, 'c_score.csv'), collapse = '' )
df_cscores <- read.csv(file = fname_cscores)
obs_c_score <- df_cscores[df_cscores$subset_name == subset_name,]$c_score # the observe C-score for this subset


# obtain the sample of C-Scores from the neutral model
# ---

fname_neut <- paste(c(dir_neut, 'c_score_', subset_name, '_rho', rho, '.csv'), collapse = '')
df <- read.csv(file = fname_neut)
c_scores <- df$c_score


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
                      subset_name = subset_name,
                      observed_c_score = obs_c_score,
                      actual_sample_size = act_sample_size,
                      effective_sample_size = act_sample_size,
                      mean_c_score = mean_c_score,
                      lower_tail_p = lo_p,
                      upper_tail_p = up_p,
                      p_type = sign_p,
                      standardised_effect_size = ses
                      )

df_out <- rbind(df_out, new_row)


# plot histogram
# ---

fname_hist <- paste(c(dir_results, 'neut_c_score_', subset_name, '.pdf'), collapse = '')
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

# NOTE the loop over subset_names would end here


# write statistical results to a csv
# ---

fname_out <- paste(c(dir_results, 'neut_c_score.csv'), collapse = '')

if (file.exists(fname_out)) {

    write.table(df_out, file = fname_out, sep = ",", append = TRUE, col.names = FALSE, row.names = FALSE)

} else {

    write.csv(df_out, fname_out, row.names = FALSE)

}


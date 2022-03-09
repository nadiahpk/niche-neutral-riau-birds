
# calculate observed NODF
# ---

M <- as.matrix(df_sub[,2:ncol(df_sub)])
NODF <- calc_packed_NODF(M)


# save to a csv file
# ---

NODFs = c(NODF)
subsets = c(subset_name)

df_out <- data.frame(subset_name = subsets, NODF = NODFs)

fname_out <- paste( c(dirname_out, 'NODF.csv'), collapse='' )

if (file.exists(fname_out)) {

    write.table(df_out, file = fname_out, sep = ",", append = TRUE, col.names = FALSE, row.names = FALSE)

} else {

    write.csv(df_out, fname_out, row.names = FALSE)

}


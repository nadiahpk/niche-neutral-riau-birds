# re-order a matrix so that the rows with the greatest row sum are at the top
# optionally also sort same-sum rows in lexicographic order (helpful visually)
pack_rows <- function(M, lexico_sort=F){

    # find the sum of each row
    row_sums <- rowSums(M)

    # find the order of indices that would put the row sums in decreasing order
    row_ord <- order(row_sums, decreasing=T)

    # reorder the matrix
    M_sorted <- M[row_ord,]

    if (lexico_sort){

        # within blocks of equally abundant species, sort lexicographically
        row_sums <- rowSums(M_sorted)
        row_sumS <- unique(row_sums)
        new_order <- c()
        for (row_sum in row_sumS){

            # find the subset of rows that have this row sum
            idxs <- which(row_sums == row_sum)

            # create a temporary list that we can order
            tmp_list <- c()
            for (idx in idxs){
                tmp_list <- c(tmp_list, paste(M_sorted[idx,], collapse=''))
            }

            # find the ordering for this subset
            sub_order <- order(tmp_list, decreasing=T)

            # apply the ordering to the indexes and store
            new_order <- c(new_order, idxs[sub_order])
        }
        M_sorted <- M_sorted[new_order,]

    }

    return(M_sorted)
}

# re-order a matrix so that the columns with the greatest column sum are to the left
pack_cols <- function(M){

    # find the sum of each column
    col_sums <- colSums(M)

    # find the order of indices that would put the column sums in decreasing order
    col_ord <- order(col_sums, decreasing=T)

    # reorder the matrix
    M_sorted <- M[,col_ord]

    return(M_sorted)
}

# the calculation is the same for rows and columns, just transposed, so write a 
# function for just one (rows)
N_paired_rows <- function(M) {

    Np <- c() # Npaired for each row stored here

    for ( i in 1 : (nrow(M)-1) ){

        # for each upper row
        u <- M[i,]
        MTu <- sum(u)

        for ( j in (i+1) : nrow(M) ){
            
            # for each lower row
            l <- M[j,]
            MTl <- sum(l)

            if ( MTl >= MTu ){

                # if there is not decreasing fill, Npaired = 0
                Np <- c(Np, 0)

            } else {

                # otherwise, Npaired = percentage overlap between upper
                # and lower row
                Np <- c(Np, 100*sum(u*l) / MTl )

            }

        }

    }

    return(Np)

} # N_paired_rows()

# calculate NODF
# note that, if we're using the FF algorithm, can just use this instead of the packed variants
calc_NODF <- function(M) {

    # remove empty rows and columns
    del_rows <- which(rowSums(M) == 0)
    del_cols <- which(colSums(M) == 0)
    if (length(del_rows) > 0){M <- M[-del_rows,]}
    if (length(del_cols) > 0){M <- M[,-del_cols]}

    # find N_paired for every row and column pair
    Npr <- N_paired_rows(M)
    Npc <- N_paired_rows(t(M)) # transposed to do columns

    # NODF is the average
    NODF <- mean(c(Npr, Npc))

    return(NODF)

}

# calculate NODF after packing both rows and columns
calc_packed_NODF <- function(M) {

    M <- pack_rows(M)
    M <- pack_cols(M)
    NODF <- calc_NODF(M)

    return(NODF)

}

# calculate NODF after packing rows only (i.e., species ordering)
calc_rowpacked_NODF <- function(M) {

    M <- pack_rows(M)
    NODF <- calc_NODF(M)

    return(NODF)

}

sort_by_island_area <- function(df_sub){

    # read in island areas
    fname <- '../../data/processed/island_area.csv'
    df_area <- read.csv(file = fname)

    # get our island names of interest
    island_names <- names(df_sub)
    island_names <- island_names[2:length(island_names)]

    # find the area of each island of interest
    rownames(df_area) <- df_area$island_name # make the island name the index - convenient later
    island_areas <- c()
    for (island_name in island_names) {
        island_areas <- c(island_areas, df_area[island_name, 'area_sq_km'])
    }

    # find the sort order of the island_areas
    idx_order <- order(island_areas, decreasing = TRUE)

    # sort the columns of df_sub according to the sort order
    idx_order <- idx_order+1        # need to add 1 because the first column of df_sub is 'species_name'
    idx_order <- c(1, idx_order)    # append the 1 to the front to keep species_name column where it is
    df_sub <- df_sub[, idx_order]   # apply the new sort order

    return(df_sub)

}

# ---------------------------------------------------------

# find NODF for an example matrix
example_NODF <- function() {

    # example matrix
    M  <- matrix( c(1, 0, 1, 1, 1, 
                    1, 1, 1, 0, 0, 
                    0, 1, 1, 1, 0, 
                    1, 1, 0, 0, 0, 
                    1, 1, 0, 0, 0), 
                 nrow = 5, 
                 ncol = 5, 
                 byrow = TRUE)

    print('This is the example presence-absence matrix')
    print(M)

    NODF <- calc_NODF(M)
    print(paste(c('NODF metric = ', NODF), collapse = ''))

}

# reorder an example matrix so the rows and columns with the greatest
# sum are to the top left
example_pack <- function() {

    # example matrix is not in order
    M  <- matrix( c(1, 0, 0, 1, 0, 
                    0, 1, 1, 0, 0, 
                    0, 1, 1, 1, 0, 
                    0, 1, 0, 0, 0, 
                    1, 1, 0, 1, 1), 
                 nrow = 5, 
                 ncol = 5, 
                 byrow = TRUE)

    print('This is the example presence-absence matrix')
    print(M)

    M <- pack_rows(M)
    M <- pack_cols(M)

    print('This is the same matrix sorted')
    print(M)
}

# check my code on the calirept example, NODF = 26.65
# -- correct
check_calirept <- function() {
    M <- matrix( c(
                    0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                    0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,
                    0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,
                    0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                    0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,0,1,0,1,0,0,1,
                    0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                    0,0,1,0,0,0,0,0,1,1,0,1,0,1,0,0,0,0,0,0,0,0,0,1,1,0,1,
                    0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,1,0,0,1,0,0,0,0,
                    0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,
                    0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,
                    1,1,1,0,1,0,1,0,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,
                    0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                    0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0),
                nrow = 15,
                ncol = 27,
                byrow = TRUE)

    M <- pack_rows(M)
    M <- pack_cols(M)
    NODF <- calc_NODF(M)
    print(NODF)
}

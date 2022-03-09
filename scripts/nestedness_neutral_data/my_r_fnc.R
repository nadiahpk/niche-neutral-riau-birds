cooc_null_model <- function(speciesData, 
                            algo = "sim9", 
                            metric = "c_score", 
                            nReps = 1000, 
                            saveSeed = FALSE, 
                            burn_in = 500,
                            algoOpts = list(),
                            metricOpts = list(),
                            suppressProg = FALSE){
    aChoice <- c(paste("sim",c(1:10),sep=""))
    mChoice <- c("species_combo", "checker", "c_score", "c_score_var", "c_score_skew", "v_ratio")

    algo <- match.arg(algo,choices = aChoice)
    metric <- match.arg(metric,choices = mChoice)
    ## Control behavior of whether or not sim9fast is used.
    if(algo != "sim9"){
    params <- list(speciesData = speciesData, algo = algo, metric = metric, nReps = nReps, saveSeed
    = saveSeed
    ,algoOpts = algoOpts,metricOpts = metricOpts,suppressProg = suppressProg)
    output <- do.call(null_model_engine,params)
    output$burn.in <- burn_in
    class(output) <- "coocnullmod"
    return(output)
    } else if(algo == "sim9"){
    params <- list(speciesData = speciesData,algo = algo, metric = metric, nReps = nReps, saveSeed = saveSeed, burn_in = burn_in, suppressProg = suppressProg)
    output <- do.call(sim9,params)
    class(output) <- "coocnullmod"
    return(output)
    }


}

if(type=="burn_in"){

    par(mfrow=c(1,1))               # setting the number of images on the plot?
    v <- nullmodObj$burn.in.metric  # must be the list of sample values
    z <- nullmodObj$Obs             # observed value
    v <- c(z,v)                     # list of actual metric values including the observation
    plot(x = 1:length(v),
         y = v,
         xlab = "Iteration",
         ylab = "Index", 
         las = 1,
         type = "l",
         col = "royalblue3")
    abline(h = z, col = "red3")     # a read line for the observation
    lines(lowess(1:length(v),v), col="gray",lwd=4) # lowess line (x,y)

}

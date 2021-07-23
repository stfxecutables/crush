#!/usr/bin/env Rscript

library(dplyr)
library(Hmisc)

args = commandArgs(trailingOnly=TRUE)
# test if there is at least one argument: if not, return an error
if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  args[2] = "correlations.csv"
}

my_data <- read.csv(args[1], header=TRUE)

correlation <- data.frame(measure=character(),
                     r=numeric(),
                     p=numeric(),
                     df=integer()
)

df_limit=length(my_data$Age)
Age=as.numeric(unlist(my_data['Age']))
#filter(my_data,ROI.Label == 'Brain-Stem')
for (i in names(my_data)){
  
  if(
      typeof(my_data[[i]])=="double" & 
      sum(!is.na(my_data[[i]]))>.8*df_limit & 
      sd(my_data[[i]],na.rm=TRUE)>0
  ) {
    
    x=rcorr(Age,as.numeric(unlist(my_data[[i]])),type = "pearson")
    r=x$r[2]
    p=x$P[2]
    df=x$n[2]
    if(p<0.05) {
      correlation[nrow(correlation)+1,] = c(i,r,p,df)
    } 
  }
  
}
write.csv(correlation,args[2],na="")

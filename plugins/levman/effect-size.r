#!/usr/bin/env Rscript

library(dplyr)

args = commandArgs(trailingOnly=TRUE)
# test if there is at least one argument: if not, return an error
if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  args[2] = "effects.csv"
}

my_data <- read.csv(args[1], header=TRUE)


effect <- data.frame(roistart=character(),
                     roiend=character(),
                     method=character(),
                     measure=character(),
                     sigma=numeric(),
                     m1=numeric(),
                     m2=numeric(),
                     theta=numeric(),
                     df=integer()
)

#filter(my_data,ROI.Label == 'Brain-Stem')

ROIStart= unique(my_data$ROI.Label)
ROIEnd =  unique(my_data$ROI.END.Label)
methods = unique(my_data$Method)


for (startlabel in ROIStart) {
  for (endlabel in ROIEnd){
    if(!all(startlabel==endlabel)) {
      for (method in methods) {
        #meanFA ================================================================
        subset = filter(my_data,ROI.Label == startlabel, ROI.END.Label==endlabel, Method==method)
        sigma=sd(subset$meanFA,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$meanFA,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$meanFA,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(meanFA)))
        measure='meanFA'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)
        
        #NumTracts ================================================================
        sigma=sd(subset$NumTracts,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$NumTracts,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$NumTracts,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(NumTracts)))
        measure='NumTracts'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)
        
        #TractsToRender ================================================================
        sigma=sd(subset$TractsToRender,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$TractsToRender,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$TractsToRender,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(TractsToRender)))
        measure='TractsToRender'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)
        
        #LinesToRender ================================================================
        sigma=sd(subset$LinesToRender,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$LinesToRender,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$LinesToRender,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(LinesToRender)))
        measure='LinesToRender'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)
        
        #MeanTractLen ================================================================
        sigma=sd(subset$MeanTractLen,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$MeanTractLen,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$MeanTractLen,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(MeanTractLen)))
        measure='MeanTractLen'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)
        
        #MeanTractLen_StdDev ================================================================
        sigma=sd(subset$MeanTractLen_StdDev,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$MeanTractLen_StdDev,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$MeanTractLen_StdDev,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(MeanTractLen_StdDev)))
        measure='MeanTractLen_StdDev'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)        

        #stddevFA ================================================================
        sigma=sd(subset$stddevFA,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$stddevFA,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$stddevFA,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(stddevFA)))
        measure='stddevFA'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)    
        
        
        #meanADC ================================================================
        sigma=sd(subset$meanADC,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$meanADC,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$meanADC,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(meanADC)))
        measure='meanADC'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)            
        
        #stddevADC ================================================================
        sigma=sd(subset$stddevADC,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$stddevADC,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$stddevADC,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(stddevADC)))
        measure='stddevADC'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)      
        
        #######################################################################
        ####  Asymmetry
        #######################################################################
        
        #meanFA.asymidx ================================================================
        sigma=sd(subset$meanFA.asymidx,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$meanFA.asymidx,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$meanFA.asymidx,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(meanFA.asymidx)))
        measure='meanFA.asymidx'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)
        
        #NumTracts.asymidx ================================================================
        sigma=sd(subset$NumTracts.asymidx,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$NumTracts.asymidx,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$NumTracts.asymidx,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(NumTracts.asymidx)))
        measure='NumTracts.asymidx'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)
        
        #TractsToRender.asymidx ================================================================
        sigma=sd(subset$TractsToRender.asymidx,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$TractsToRender.asymidx,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$TractsToRender.asymidx,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(TractsToRender.asymidx)))
        measure='TractsToRender.asymidx'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)
        
        #LinesToRender.asymidx ================================================================
        sigma=sd(subset$LinesToRender.asymidx,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$LinesToRender.asymidx,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$LinesToRender.asymidx,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(LinesToRender.asymidx)))
        measure='LinesToRender.asymidx'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)
        
        #MeanTractLen.asymidx ================================================================
        sigma=sd(subset$MeanTractLen.asymidx,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$MeanTractLen.asymidx,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$MeanTractLen.asymidx,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(MeanTractLen.asymidx)))
        measure='MeanTractLen.asymidx'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)
        
        #MeanTractLen_StdDev.asymidx ================================================================
        sigma=sd(subset$MeanTractLen_StdDev.asymidx,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$MeanTractLen_StdDev.asymidx,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$MeanTractLen_StdDev.asymidx,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(MeanTractLen_StdDev.asymidx)))
        measure='MeanTractLen_StdDev.asymidx'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)        
        
        #stddevFA.asymidx ================================================================
        sigma=sd(subset$stddevFA.asymidx,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$stddevFA.asymidx,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$stddevFA.asymidx,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(stddevFA.asymidx)))
        measure='stddevFA.asymidx'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)    
        
        
        #meanADC.asymidx ================================================================
        sigma=sd(subset$meanADC.asymidx,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$meanADC.asymidx,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$meanADC.asymidx,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(meanADC.asymidx)))
        measure='meanADC.asymidx'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)            
        
        #stddevADC.asymidx ================================================================
        sigma=sd(subset$stddevADC.asymidx,na.rm=TRUE)
        m1=mean(filter(subset,Gender=='Male')$stddevADC.asymidx,na.rm = TRUE)
        m2=mean(filter(subset,Gender=='Female')$stddevADC.asymidx,na.rm = TRUE)
        theta=(m1-m2)/sigma
        df=nrow(filter(subset,!is.na(stddevADC.asymidx)))
        measure='stddevADC.asymidx'
        effect[nrow(effect)+1,] = c(startlabel,endlabel,method,measure,sigma,m1,m2,theta,df)      
        
      }
    }
  }
}
write.csv(effect,args[2],na="")

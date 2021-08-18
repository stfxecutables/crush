my_data <- read.csv('/media/dmattie/GENERAL/projects/hcptracts/dataframe3-split/effect-size-results-hcp.csv', header=TRUE)

eightypercent=filter(my_data,df>=max(my_data$df)*.8,is.na(theta)==FALSE,roiend!='Left-UnsegmentedWhiteMatter', roiend!='Right-UnsegmentedWhiteMatter')
top100=tail(eightypercent[order(abs(eightypercent$theta)),],100)

write.csv(eightypercent,"/media/dmattie/GENERAL/projects/hcptracts/dataframe3-split/eightpercent.csv",na="")
write.csv(top100,"/media/dmattie/GENERAL/projects/hcptracts/dataframe3-split/top100.csv",na="")

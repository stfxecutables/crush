library(ggpubr)

my_data <- read.csv('/media/dmattie/GENERAL/MSc-Analysis/2019-06-07.small.csv', header=TRUE)
#cor(x, y,  method = "pearson", use = "complete.obs")

ggscatter(my_data, x = "Age", y = "meanFA", 
          add = "reg.line", conf.int = TRUE, 
          cor.coef = TRUE, cor.method = "pearson",
          xlab = "Age", ylab = "Average Fractional Anisotropy")

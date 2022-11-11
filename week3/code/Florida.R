library(ggplot2)
rm(list=ls())
load("../data/KeyWestAnnualMeanTemperature.RData")
ls()
class(ats)
head(ats)
plot(ats)

#Compute the appropriate correlation coefficient 
corr <- cor(ats$Year, ats$Temp, method = "pearson")
print(corr)

#Repeat the calculation a sufficient 10000 times
corr_sam <- data.frame(matrix(unlist(replicate(10000, cor(ats$Year, sample(ats$Temp, replace = F), method = "pearson")))))

#Calculate what fraction of the random correlation coefficients were greater than the observed one
num <- 0
for (i in corr_sam){ #use loops to calculate abs
  if (abs(i) > abs(corr)){
    num <- num + 1
  }
}
p_value <- num/10000
print(p_value)

#interpret the results
ggplot(corr_sam,aes(num))+ geom_density(color="red",fill="grey") + xlab("Correlation coefficient") + ylab("Frequency")
ggsave("../results/Florida_plot.pdf")
dev.off()                    

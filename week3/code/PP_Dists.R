rm(list = ls())
library(ggplot2)
#read the data
data <- read.csv("../data/EcolArchives-E089-51-D1.csv")

pdf("../results/Pred_Subplots.pdf")
par(mfrow=c(3,2))
for(feeding in unique(data$Type.of.feeding.interaction)){
  feeding_df <- data[data$Type.of.feeding.interaction == feeding, ]
  hist(feeding_df$Predator.mass, 
       main=paste("Distribution of Predator Mass for", feeding), 
       xlab=("Predator Mass"), ylab=("Frequency"),
       cex.main=1,7, cex.lab=0.8)
}
dev.off()

pdf("../results/Prey_Subplots.pdf")
par(mfrow=c(3,2))
for(feeding in unique(data$Type.of.feeding.interaction)){
  feeding_df <- data[data$Type.of.feeding.interaction == feeding, ]
  hist(feeding_df$Prey.mass, 
       main=paste("Distribution of Prey Mass for", feeding), 
       xlab=("Prey Mass"), ylab=("Frequency"),
       cex.main=1,7, cex.lab=0.8)
}
dev.off()

pdf("../results/SizeRatio_Subplots.pdf")
par(mfrow=c(3,2))
for(feeding in unique(data$Type.of.feeding.interaction)){
  feeding_df <- data[data$Type.of.feeding.interaction == feeding, ]
  hist(feeding_df$Prey.mass/feeding_df$Predator.mass,
       main=paste("Distribution of Size Ratio for", feeding), 
       xlab=("Size Ratio"), ylab=("Frequency"),
       cex.main=1,7, cex.lab=0.8)
}
dev.off()

results <- NULL
for(feeding in unique(data$Type.of.feeding.interaction)){
  feeding_df <- data[data$Type.of.feeding.interaction == feeding, ]
  result <- c(feeding, 
              mean(log(feeding_df$Predator.mass)), median(log(feeding_df$Predator.mass)),
              mean(log(feeding_df$Prey.mass)), median(log(feeding_df$Prey.mass)),
              mean(log(feeding_df$Prey.mass/feeding_df$Predator.mass)), median(log(feeding_df$Prey.mass/feeding_df$Predator.mass))
  )
  results <- c(results, result)
}

results <- matrix(results, byrow=T, nrow=5)
colnames(results) <- c("Feeding Type", "Mean of Log Predator Mass", "Median of Log Predator Mass", 
                       "Mean of Log Prey Mass", "Median of Log Prey Mass", "Mean of Log Size Rate", "Median of Log Size Rate")
write.csv(results, "../results/PP_Results.csv", row.names = F)

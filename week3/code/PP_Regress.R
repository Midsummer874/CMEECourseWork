# Language: R
# Script: PP_Regress.R
# Author: Shengge Tong (shengge.tong22@imperial.ac.uk)
# Date: Nov, 2022

library(ggplot2)
data <- read.csv("../data/EcolArchives-E089-51-D1.csv")

pdf("../results/PP_Regress.pdf")
p <- ggplot(data, aes(x = Prey.mass, y = Predator.mass, color = Predator.lifestage)) +
  geom_point(aes(fill = Predator.lifestage, shape = Predator.lifestage)) +
  geom_smooth(method= "lm", fill="darkgrey") +
  facet_wrap(~ Type.of.feeding.interaction, ncol=1, strip.position = "right") + 
  theme_bw() +
  xlab("Prey Mass in grams") +
  ylab("Predator Mass in grams") +
  scale_x_log10() +
  scale_y_log10() +
  theme(legend.position = 'bottom',
        legend.text = element_text(size=6),
        legend.title = element_text(size=6)) +
  guides(fill = guide_legend(ncol = 6))
print(p)
dev.off()

results <- NULL
rows <- 0
for(feeding in unique(data$Type.of.feeding.interaction)){
  feeding_df <- data[data$Type.of.feeding.interaction == feeding, ]
  for(lifestage in unique(feeding_df$Predator.lifestage)){
    select_df <- feeding_df[feeding_df$Predator.lifestage == lifestage, ]
    if(nrow(select_df) > 2){
      model <- lm(log(Predator.mass) ~ log(Prey.mass), select_df)
      sum_model <- summary(model)
      f <- sum_model$fstatistic
      result <- c(feeding, lifestage, sum_model$coefficients[2, 1], sum_model$coefficients[1, 1],
                  sum_model$r.squared, f[1], pf(f[1],f[2],f[3],lower.tail=F))
      results <- c(results, result)
      rows <- rows+1
    }
  }
}
results <- matrix(results, byrow=T, nrow=rows)
colnames(results) <- c("Feeding Type", "Life Stage", "Slope", "Intercept", "R2", "F-statstic", "P-value")
write.csv(results, "../results/PP_Regress_Results.csv", row.names = F)


library(reshape2)
library(ggplot2)

tasks = c("Literature Review", "Data Preprocessing", "Code Writing", "Model Simulation", "Result Analysis", "Thesis Writing")
tasks = factor(tasks, levels = tasks)
start.date = as.Date(c("2023-04-17","2023-04-24","2023-05-08", "2023-05-22", "2023-06-15", "2023-05-15"))
end.date = as.Date(c("2023-04-28", "2023-05-12", "2023-06-02", "2023-06-23", "2023-08-01", "2023-09-01"))
chart = data.frame(tasks, start.date,end.date)
chart = melt(chart, measure.vars = c("start.date", "end.date"))
pdf("Gantt_chart.pdf", width = 9, height = 3)
ggplot(chart, aes(value, tasks)) + 
  geom_line(size = 6) + theme_bw()+
  scale_x_date(date_labels = "%b %Y",date_breaks = "1 months") +
  xlab(NULL) +
  ylab(NULL)
graphics.off()
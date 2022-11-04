# Language: R
# Author: Shengge Tong (shengge.tong22@imperial.ac.uk)
# Script: GPDD_Data.R
# Date: Nov, 2022

load("../data/GPDDFiltered.RData") #load GPDD data

library(maps) #load the maps package

map(database = "world", fill = TRUE, ylim = c(-100,100)) 

points(gpdd, col = "blue")
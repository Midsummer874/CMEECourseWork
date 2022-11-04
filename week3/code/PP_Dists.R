#Language:R
#Auther: Shengge Tong (shengge.tong22@imperial.ac.uk)
#Script: PP_Dists.R
#Date: Nov, 2022

rm(list = ls())

df <- read.csv("../data/EcolArchives-E089-51-D1.csv")

require(ggplot2)
require(tidyverse)

dplyr::glimpse(df) # inspect and explore data



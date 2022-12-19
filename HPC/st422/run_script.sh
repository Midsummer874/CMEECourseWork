#!/bin/bash
#PBS -l walltime=10:00:00
#PBS -l select=1:ncpus=1:mem=1gb
module load anaconda3/personal
echo "Begin to run scripts"
R --vanilla < $HOME/HPC/code/st422_HPC_2022_cluster.R
mv SimulationOutput* $HOME/HPC/results
echo "Finished running"

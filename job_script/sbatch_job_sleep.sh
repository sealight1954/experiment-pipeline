#!/bin/bash
#%x not works for ver.15. ver. 17?
# https://stackoverflow.com/questions/50242293/using-sbatch-job-name-as-a-variable-in-file-output
# https://slurm.schedmd.com/sbatch.html
#SBATCH --output=res_%j.txt
#SBATCH --error=err_%j.txt
#
#SBATCH --ntasks=1
#SBATCH --time=10:00
#SBATCH --mem-per-cpu=100
srun python ./job_script/job_sleep.py
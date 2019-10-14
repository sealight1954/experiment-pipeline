#!/bin/bash
# Plan A
task1_id=$(sbatch --parsable job_script/sbatch_job_sleep.sh)
task2_id=$(sbatch --parsable job_script/sbatch_job_sleep.sh)
sbatch --dependency=afterok:${task1_id}:${task2_id} --job-name=task1-2 job_script/sbatch_job_sleep.sh

# Plan B
sbatch --job-name=task3 job_script/sbatch_job_sleep.sh
sbatch --job-name=task4 job_script/sbatch_job_sleep.sh
sbatch --dependency=afterok:$(squeue --noheader --format %i --name task3):$(squeue --noheader --format %i --name task4) --job-name=task3-4 job_script/sbatch_job_sleep.sh

# jobid=$(sbatch --parsable --job-name=task1 submit.sh) 
# sbatch --dependency=afterok:$(squeue --noheader --format %i --name somejob1):$(squeue --noheader --format %i --name somejob2) submit.sh
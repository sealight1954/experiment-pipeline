#!/bin/bash
# Plan A (better)
task1_id=$(sbatch --parsable job_script/sbatch_job_sleep.sh)
task2_id=$(sbatch --parsable job_script/sbatch_job_sleep.sh)
sbatch --dependency=afterok:${task1_id}:${task2_id} --job-name=task1-2 job_script/sbatch_job_sleep.sh

# Plan B
# TODO: job-name can be assigned to multiple jobs. Multiple runs of followings will collapse pipeline.
# TODO: Must ensure job-name is identical e.g. add timestamp to job-name, in order to avoid conflict with other jobs with same job-name.
sbatch --job-name=task3 job_script/sbatch_job_sleep.sh
sbatch --job-name=task4 job_script/sbatch_job_sleep.sh
sbatch --dependency=afterok:$(squeue --noheader --format %i --name task3):$(squeue --noheader --format %i --name task4) --job-name=task3-4 job_script/sbatch_job_sleep.sh

# jobid=$(sbatch --parsable --job-name=task1 submit.sh) 
# sbatch --dependency=afterok:$(squeue --noheader --format %i --name somejob1):$(squeue --noheader --format %i --name somejob2) submit.sh
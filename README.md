# Overview

## Coordinator
- coordinator.py
    - parallel executor of multiple sequential run
- bash_coordinator.py
    - parallel executor of bash scripts
- pipeline coordinator
    `python run_bash_pipeline.py`
    - pipeline which represents following:
        ```
        task 1
            task 1-1 depends on task 1
            task 1-2 depends on task 1
        task 2 depends on task 1-1, 1-2
            task 2-1
            task 2-2
        ```


# TODO
- [x] Generate class "Coordinator":
    - input: list of jobs including dependency
    - action: submit jobs with dependencies
- [ ] Slurm coordinator
    - interface: same as coordinator
    - action: submit jobs with dependencies
        - Generate temporaly sbatch script, get job id.
- [ ] Implement logger
- [x] See whether coordinator can work with ThreadPoolExecutor
- [ ] --use-cache option
    - Skip if result file already exists. and skip to next job
    - If sbatch, do not even want to submit job?
        - -> If system has max-number-of-jobs property, this will allow other users' job go ahead while executing the skip job.
- [x] Sequential Coordinator
    - Sequential Run
- [x] Interface should be constructor, not instance.
    - For fork-safe execution
- [ ] Handle release worker.
- [ ] Different number of arguments
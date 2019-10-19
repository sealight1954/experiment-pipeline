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
- [x] Slurm coordinator
    - interface: same as coordinator
    - action: submit jobs with dependencies
        - Generate temporaly sbatch script, get job id.
- [x] See whether coordinator can work with ThreadPoolExecutor
    - Skip if result file already exists. and skip to next job
    - If sbatch, do not even want to submit job?
        - -> If system has max-number-of-jobs property, this will allow other users' job go ahead while executing the skip job.
- [x] Sequential Coordinator
    - Sequential Run
- [x] Interface should be constructor, not instance.
    - For fork-safe execution
- [x] Different number of arguments
- [ ] --use-cache option
- [ ] Handle release worker.
- [ ] Implement logger
- [ ] Support dry-run for bash
    - Base bash runner and coordinator
    - Only support sequential? Process Pool, maybe okay, but sbatch it seems we need to immitate job-id
    - Or we call dry_submit() for BaseCoordinator.
    - Runner configuration seems tricky. we want to avoid modify every subclass of BaseBashRunner.
- [x] args to be **kwargs
    - Support Function Runner and Bash Runner.
- [x] remove command specific runner class.
    - Assume every function takes kwargs, at least one argument required.
- [x] run -> __call__
- [ ] Base coordinator to cope with different cmd_args.
    - callable function and cmd_args, or bash commands.
- [ ] stdout and stderr to files.
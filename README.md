# Overview

## Assumption
- For Bash command, arguments must have "--$(key) $(value)" command arguments.
- If can not, use command coordinator (in progress).

## Coordinator
- coordinator.py
    - parallel executor of multiple sequential run
- bash_coordinator.py
    - parallel executor of bash scripts
- pipeline coordinator
    `python run_pipeline.py`
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
- [x] Support dry-run for bash, func
    - Base bash runner and coordinator
    - Only support sequential? Process Pool, maybe okay, but sbatch it seems we need to immitate job-id
    - ~~Or we call dry_submit() for BaseCoordinator.~~
    - Runner configuration seems tricky. we want to avoid modify every subclass of BaseBashRunner.
- [x] args to be **kwargs
    - Support Function Runner and Bash Runner.
- [x] remove command specific runner class.
    - Assume every function takes kwargs, at least one argument required.
- [x] run -> __call__
- [x] Sbatch support
- [n] --use-cache option ... each script will take care?
- [x] Handle release worker.
    - ProcessPoolExecutor.
- [x] CommandRunStrategy.
    - CallableRunnerStrategy: callable function and cmd_args, or CommandStrategy: bash commands.
    - We don't need base strategy. By defining lambda function and arguments to be {}, we can pass commands with some phrase.
    - Maybe we can wrap that to make base strategy.
- [x] stdout and stderr to files.
    - For Process Pool Executor, runner construction must be inside forked process.
    - We need some way to wrap the construction
- [x] stdout of coordinator should be commands to execute and corresponding log files.
    - sbatch
- [x] Error handling. Stop when one command fails.
    - Suppose assertion error.
        - For function call(BaseFuncRunner), no worry and it asserts.
        - For bash call(BaseBashRunner), it will return 1 exit code.
- [x] Support ProcessPool
    - What we want is [parallel, not concurrency](https://medium.com/contentsquare-engineering-blog/multithreading-vs-multiprocessing-in-python-ece023ad55a)
    - How following statements affect the results?
        - This runs spawn instead of fork? spawn like __main__ called multiple times.
        ```
        import multiprocessing
        multiprocessing.set_start_method('spawn', True)
        ```
    - According to [multithreading vs multiprocessing](https://medium.com/contentsquare-engineering-blog/multithreading-vs-multiprocessing-in-python-ece023ad55a), we should focus on multi processing.
    - We have two ways
        - [x] construct_and_run need to be static
        - [no action] [__getstate__ and __setstate__](https://stackoverflow.com/questions/47163820/getting-queue-objects-should-only-be-shared-between-processes-through-inheritan) to runner.
        - [x] make_runner defined in global scope.
- [ ] Error handling for Sbatch coordinator.
    - At least we want to confirm sucessfuly fubmitting jobs.
    - It includes getting resultcode from squeue and scancel the following jobs.
- [x] log file interface to run_pipeline.py
    - BaseBashRunner already have one.
- [x] Implement logger
    - https://stackoverflow.com/questions/49782749/processpoolexecutor-logging-fails-to-log-inside-function-on-windows-but-not-on-u
    - https://docs.python.org/ja/3/library/logging.html#logrecord-attributes
    - stdout
    - file.
- [ ] Error handling more.
- [x] Job list to be class.
    - Subclass of list.
    - User only need to focus on making job_list
- [x] Get job_list from external script. run_pipeline.py as a template.

## stdout and stderr to files
- construct to inside files
    ```
    def _set_construct_run_func(self, make_runner, dry_run=False):
        def construct_run_func(**kwargs):
            cmd_runner = make_runner()
            kwargs["dry_run"] = dry_run
            return cmd_runner
        self.construct_run_func = construct_run_func
    >>> Can't pickle local object 'PoolCoordinator._get_construct_run_func.<locals>.construct_run_func'
    Terminated
    ```
    - cannot access to method local object.
    - make member variable?
        - Same error.
    - It seems it is very hard to pass constructor to ProcessPool runner function.

## ThreadPool stdout, stderr
- In parallel run, it seems log file is same. Follwoing code does not make multiple instance.
    ```
    def func():
        return SomeClass()
    ```
    
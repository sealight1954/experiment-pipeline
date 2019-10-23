from functools import partial

from base_runner import BaseBashRunner, BaseFuncRunner
from job_script.job_sleep import run_job_sleep
from job_list import Job, JobList
from job_script.job_sleep_error import run_job_sleep_error


make_bash_runner = partial(BaseBashRunner, "python job_script/job_sleep.py".split(" "))
make_func_runner = partial(BaseFuncRunner, run_job_sleep)
make_bash_error_runner = partial(BaseBashRunner, "python job_script/job_sleep_error.py".split(" "))

def get_job_list(runner_type):
    if runner_type == "Bash":
        make_runner1 = make_bash_runner
        make_runner2 = make_bash_runner
    elif runner_type == "Function":
        make_runner1 = make_func_runner
        make_runner2 = make_func_runner
    elif runner_type == "Mixed-Error":
        make_runner1 = make_bash_runner
        make_runner2 = make_bash_error_runner

    job_list = JobList([ # job-name, runner, cmd_kwargs, depends_on
        ["task1", partial(BaseBashRunner, "python job_script/job_sleep.py --id task1".split(" ")), {}, None],
        # ["task1", make_runner1, {"id": "task1"}, None],
        ["task1-1", make_runner1, {"id": "task1-1"}, ["task1"]],
        ["task1-2", make_runner1, {"id": "task1-2"}, ["task1"]],
        ["task2", make_runner2, {"id": "task2", "n": 4}, ["task1-1", "task1-2"]],
        ["task2-1", make_runner1, {"id": "task2-1", "n": 4}, ["task2"]],
        ["task2-2", make_runner1, {"id": "task2-2", "n": 4}, ["task2"]],
    ])
    return job_list
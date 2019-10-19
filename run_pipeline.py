import argparse
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

# from sleep_bash_runner import SleepBashRunner0, SleepBashRunner1, SleepBashRunner2
# from sleep_runner import SleepRunner0, SleepRunner1, SleepRunner2
from coordinator import PoolCoordinator, SequentialCoordinator
from base_runner import BaseBashRunner, BaseRunner, BaseFuncRunner
from job_script.job_sleep import run_job_sleep


def run_pipeline(p_id, runner):
    for i in range(3):
        runner.run("{}-{}".format(p_id, i))
    return "{} finished".format(p_id)


def main(args):
    def make_bash_runner():
        return BaseBashRunner("python job_script/job_sleep.py".split(" "))
    def make_func_runner():
        return BaseFuncRunner(run_job_sleep)
    # make_bash_runner2 = SleepBashRunner2
    # make_func_runner2 = SleepRunner2
    if args.runner_type == "Bash":
        make_runner = make_bash_runner
    elif args.runner_type == "Function":
        make_runner = make_func_runner
    job_list = [ # job-name, runner, cmd_kwargs, depends_on
        ["task1", make_runner, {"id": "task1"}, None],
        ["task1-1", make_runner, {"id": "task1-1"}, ["task1"]],
        ["task1-2", make_runner, {"id": "task1-2"}, ["task1"]],
        ["task2", make_runner, {"id": "task2", "n": 4}, ["task1-1", "task1-2"]],
        ["task2-1", make_runner, {"id": "task2-1", "n": 4}, ["task2"]],
        ["task2-2", make_runner, {"id": "task2-2", "n": 4}, ["task2"]],
    ]

    # TODO: Output of submit() should be same type for Sequential and PoolParallel.
    make_coordinator = {
        "Sequential": SequentialCoordinator,
        "ProcessPool": lambda: PoolCoordinator(max_workers=4, coordinator_type="ProcessPool"),
        "ThreadPool": lambda: PoolCoordinator(max_workers=4, coordinator_type="ThreadPool")}.get(
            args.coordinator_type, SequentialCoordinator
        )
    coordinator = make_coordinator()
    results = coordinator.submit(job_list, args.dry_run)

    for idx, result in enumerate(results):
        print("[{}]: Results: {}".format(idx, result))


def parse_args():
    parser = argparse.ArgumentParser()
    # TODO: Add Sbatch
    parser.add_argument('--dry-run', action='store_true',
                        help='Just print commands to execute, no run.')
    parser.add_argument('--runner-type', default="Bash",
                        choices=["Bash", "Function"],
                        help='How to run commands. Bash for call from bash, Func for function call.')
    parser.add_argument('--coordinator-type', default="ProcessPool",
                        choices=["ProcessPool", "ThreadPool", "Sequential"],
                        help='Run commands in sequential manner. Default: parallel using pool')
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
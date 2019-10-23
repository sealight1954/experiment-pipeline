import argparse
import time
import numpy as np
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial

# from sleep_bash_runner import SleepBashRunner0, SleepBashRunner1, SleepBashRunner2
# from sleep_runner import SleepRunner0, SleepRunner1, SleepRunner2
from coordinator import PoolCoordinator, SequentialCoordinator
from sbatch_coordinator import SbatchCoordinator
from job_list import Job, JobList
from get_job_list import get_job_list
from mylogger import logger

  
def main(args):
    job_list = get_job_list(args.runner_type)
    logger.info("job_list is: {}".format(job_list))

    # TODO: Output of submit() should be same type for Sequential and PoolParallel.
    make_coordinator = {
        "Sequential": SequentialCoordinator,
        "ProcessPool": lambda: PoolCoordinator(max_workers=4, coordinator_type="ProcessPool"),
        "ThreadPool": lambda: PoolCoordinator(max_workers=4, coordinator_type="ThreadPool"),
        "Sbatch": SbatchCoordinator}.get(
            args.coordinator_type, SequentialCoordinator
        )
    coordinator = make_coordinator()
    results = coordinator.submit(job_list, args.dry_run)

    for idx, result in enumerate(results):
        logger.debug("[{}]: Results: {}".format(idx, result))


def parse_args():
    parser = argparse.ArgumentParser()
    # TODO: Add Sbatch
    parser.add_argument('--dry-run', action='store_true',
                        help='Just print commands to execute, no run.')
    parser.add_argument('--runner-type', default="Bash",
                        choices=["Bash", "Function", "Mixed-Error1", "Mixed-Error2"],
                        help='How to run commands. Bash for call from bash, Func for function call.')
    parser.add_argument('--coordinator-type', default="ProcessPool",
                        choices=["ProcessPool", "ThreadPool", "Sequential", "Sbatch"],
                        help='Run commands in sequential manner. Default: parallel using pool')
    parser.add_argument('--log-dir', default="./results", type=str, 
                        help='Directory path to store logs.')
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())

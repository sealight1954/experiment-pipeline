import argparse
import time
import numpy as np
import logging
from logging import getLogger, StreamHandler, FileHandler
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial

# from sleep_bash_runner import SleepBashRunner0, SleepBashRunner1, SleepBashRunner2
# from sleep_runner import SleepRunner0, SleepRunner1, SleepRunner2
from coordinator import PoolCoordinator, SequentialCoordinator
from sbatch_coordinator import SbatchCoordinator
from base_runner import BaseBashRunner, BaseRunner, BaseFuncRunner
from job_script.job_sleep import run_job_sleep
from job_script.job_sleep_error import run_job_sleep_error


#TODO: Move to config file.
#TODO: logger name can be __name__? Don't know what to utilize logger name.
#See: https://stackoverflow.com/questions/25187083/python-logging-to-multiple-handlers-at-different-log-levels
logger = getLogger("pipeline")
handler = StreamHandler()
handler.setLevel(logging.DEBUG)
fhandler = FileHandler("results/log.txt")
fhandler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s %(funcName)s() at %(filename)s L%(lineno)d](%(levelname)s) %(message)s')
handler.setFormatter(formatter)
fhandler.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(fhandler)

make_bash_runner = partial(BaseBashRunner, "python job_script/job_sleep.py".split(" "))
make_func_runner = partial(BaseFuncRunner, run_job_sleep)
make_bash_error_runner = partial(BaseBashRunner, "python job_script/job_sleep_error.py".split(" "))
    
def main(args):
    if args.runner_type == "Bash":
        make_runner1 = make_bash_runner
        make_runner2 = make_bash_runner
    elif args.runner_type == "Function":
        make_runner1 = make_func_runner
        make_runner2 = make_func_runner
    elif args.runner_type == "Mixed-Error":
        make_runner1 = make_bash_runner
        make_runner2 = make_bash_error_runner

    job_list = [ # job-name, runner, cmd_kwargs, depends_on
        ["task1", partial(BaseBashRunner, "python job_script/job_sleep.py --id task1".split(" ")), {}, None],
        # ["task1", make_runner1, {"id": "task1"}, None],
        ["task1-1", make_runner1, {"id": "task1-1"}, ["task1"]],
        ["task1-2", make_runner1, {"id": "task1-2"}, ["task1"]],
        ["task2", make_runner2, {"id": "task2", "n": 4}, ["task1-1", "task1-2"]],
        ["task2-1", make_runner1, {"id": "task2-1", "n": 4}, ["task2"]],
        ["task2-2", make_runner1, {"id": "task2-2", "n": 4}, ["task2"]],
    ]
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
                        choices=["Bash", "Function", "Mixed-Error"],
                        help='How to run commands. Bash for call from bash, Func for function call.')
    parser.add_argument('--coordinator-type', default="ProcessPool",
                        choices=["ProcessPool", "ThreadPool", "Sequential", "Sbatch"],
                        help='Run commands in sequential manner. Default: parallel using pool')
    parser.add_argument('--log-dir', default="./results", type=str, 
                        help='Directory path to store logs.')
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())

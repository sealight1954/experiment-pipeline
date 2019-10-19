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
    if args.coordinator_type == "Sequential":
        print("Sequential run start =====================")
        coordinator = SequentialCoordinator()
        results = coordinator.submit(job_list)
    elif args.coordinator_type == "ProcessPool" or args.coordinator_type == "ThreadPool":
        print("Parallel ({}) run start =====================".format(args.coordinator_type))
        coordinator = PoolCoordinator(max_workers=4, coordinator_type=args.coordinator_type)
        futures = coordinator.submit(job_list)
        # Note: submit job already started.

        results = []
        # 各futureの完了を待ち、結果を取得。
        # as_completed()は、与えられたfuturesの要素を完了順にたどるイテレータを返す。
        # 完了したタスクが無い場合は、ひとつ完了するまでブロックされる。
        for idx, future in enumerate(as_completed(futures)):
            # TODO: Want to describe associated jobs to see order of finish, requires future_list.
            # job_name = [job_list[i] for i in range(len(job_list)) if future == futures[i]
            results.append(future.result())
            # print("[{}]: Results:{}".format(idx, future.result()))
    for idx, result in enumerate(results):
        print("[{}]: Results: {}".format(idx, result))


def parse_args():
    parser = argparse.ArgumentParser()
    # TODO: Add Sbatch
    parser.add_argument('--runner-type', default="Bash",
                        choices=["Bash", "Function"],
                        help='How to run commands. Bash for call from bash, Func for function call.')
    parser.add_argument('--coordinator-type', default="ProcessPool",
                        choices=["ProcessPool", "ThreadPool", "Sequential"],
                        help='Run commands in sequential manner. Default: parallel using pool')
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
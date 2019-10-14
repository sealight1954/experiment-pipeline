import argparse
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

from sleep_bash_runner import SleepBashRunner, SleepBashRunner1, SleepBashRunner2
from coordinator import PoolCoordinator, SequentialCoordinator


def run_pipeline(p_id, runner):
    for i in range(3):
        runner.run("{}-{}".format(p_id, i))
    return "{} finished".format(p_id)


def main(args):
    # To wrap
    # def make_runner1():
    #     return SleepBashRunner1
    # def make_runner2():
    #     return SleepBashRunner2
    
    job_list = [ # job-name, runner, args, depends_on
        ["task1", SleepBashRunner1, "task1", None],
        ["task1-1", SleepBashRunner1, "task1-1", ["task1"]],
        ["task1-2", SleepBashRunner1, "task1-2", ["task1"]],
        ["task2", SleepBashRunner2, "task2", ["task1-1", "task1-2"]],
        ["task2-1", SleepBashRunner2, "task2-1", ["task2"]],
        ["task2-2", SleepBashRunner2, "task2-2", ["task2"]],
        ["task3", SleepBashRunner1, "task3", None],
    ]

    # TODO: Output of submit() should be same type for Sequential and PoolParallel.
    if args.coordinator_type == "Sequential":
        print("Sequential run start =====================")
        coordinator = SequentialCoordinator()
        results = coordinator.submit(job_list)
    elif args.coordinator_type == "ProcessPool" or args.coordinator_type == "ThreadPool":
        print("Parallel ({}) run start =====================".format(args.coordinator_type))
        coordinator = PoolCoordinator(4, args.coordinator_type)
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
    parser.add_argument('--coordinator-type', default="ProcessPool",
                        choices=["ProcessPool", "ThreadPool", "Sequential"],
                        help='Run commands in sequential manner. Default: parallel using pool')
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
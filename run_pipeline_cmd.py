import argparse
import time
import numpy as np
from concurrent.futures import as_completed

from sleep_bash_runner import get_sleep_cmd
from coordinator import PoolCoordinator, SequentialCoordinator
from sbatch_coordinator import SbatchCoordinator

def main(args):
    job_list = [ # job-name, command, depends_on
        ["task1", get_sleep_cmd("task1", 5), None],
        ["task1-1", get_sleep_cmd("task1-1", 5), ["task1"]],
        ["task1-2", get_sleep_cmd("task1-2", 5), ["task1"]],
        ["task2", get_sleep_cmd("task2", 5), ["task1-1", "task1-2"]],
        ["task2-1", get_sleep_cmd("task2-1", 5), ["task2"]],
        ["task2-2", get_sleep_cmd("task2-2", 5), ["task2"]],
        ["task3", get_sleep_cmd("task3", 5), None],
        ["task4", get_sleep_cmd("task4", 5), None],
    ]

    # TODO: Output of submit() should be same type for Sequential and PoolParallel.
    if args.coordinator_type == "Sequential":
        print("Sequential run start =====================")
        coordinator = SequentialCoordinator()
        results = coordinator.submit(job_list)
    elif args.coordinator_type == "Sbatch":
        print("Sbatch run start =====================")
        coordinator = SbatchCoordinator()
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
    parser.add_argument('--coordinator-type', default="ProcessPool",
                        choices=["ThreadPool", "Sequential", "Sbatch"],
                        help='Run commands in sequential manner. Default: parallel using pool')
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
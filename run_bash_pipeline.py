import argparse
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

from sleep_bash_runner import SleepBashRunner, SleepBashRunner1, SleepBashRunner2
from coordinator import ProcessPoolCoordinator, SequentialCoordinator


def run_pipeline(p_id, runner):
    for i in range(3):
        runner.run("{}-{}".format(p_id, i))
    return "{} finished".format(p_id)


def main(args):
    sleep_runner = SleepBashRunner()
    sleep_runner1 = SleepBashRunner1()
    sleep_runner2 = SleepBashRunner2()
    # run_pipeline("2", sleep_runner)
        # Executorオブジェクトを作成
    job_list = [ # job-name, runner, args, depends_on
        ["task1", sleep_runner1, "task1", None],
        ["task1-1", sleep_runner1, "task1-1", ["task1"]],
        ["task1-2", sleep_runner1, "task1-2", ["task1"]],
        ["task2", sleep_runner2, "task2", ["task1-1", "task1-2"]],
        ["task2-1", sleep_runner2, "task2-1", ["task2"]],
        ["task2-2", sleep_runner2, "task2-2", ["task2"]],
        ["task3", sleep_runner1, "task3", None],
    ]
    # TODO: Output of submit() should be same type for Sequential and PoolParallel.
    if args.sequential_run:
        print("Sequential run start =====================")
        coordinator = SequentialCoordinator()
        results = coordinator.submit(job_list)
    else:
        print("Parallel run start =====================")
        coordinator = ProcessPoolCoordinator(4)
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
    parser.add_argument('--sequential-run', action='store_true',
                        help='Run commands in sequential manner. Default: parallel using pool')
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
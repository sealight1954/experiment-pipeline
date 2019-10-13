import argparse
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

from sleep_bash_executor import SleepBashExecutor, SleepBashExecutor1, SleepBashExecutor2
from coordinator import Coordinator

def run_pipeline(p_id, executor):
    for i in range(3):
        executor.run("{}-{}".format(p_id, i))
    return "{} finished".format(p_id)

def main(args):
    sleep_executor = SleepBashExecutor()
    sleep_executor1 = SleepBashExecutor1()
    sleep_executor2 = SleepBashExecutor2()
    # run_pipeline("2", sleep_executor)
        # Executorオブジェクトを作成
    job_list = [ # job-name, executor, args, depends_on
        ["task1", sleep_executor1, "task1", None],
        ["task1-1", sleep_executor1, "task1-1", ["task1"]],
        ["task1-2", sleep_executor1, "task1-2", ["task1"]],
        ["task2", sleep_executor2, "task2", ["task1-1", "task1-2"]],
        ["task2-1", sleep_executor2, "task2-1", ["task2"]],
        ["task2-2", sleep_executor2, "task2-2", ["task2"]],
        ["task3", sleep_executor1, "task3", None],
    ]
    coordinator = Coordinator(4)
    futures = coordinator.submit(job_list)
    # Note: submit job already started.

    # 各futureの完了を待ち、結果を取得。
    # as_completed()は、与えられたfuturesの要素を完了順にたどるイテレータを返す。
    # 完了したタスクが無い場合は、ひとつ完了するまでブロックされる。
    for future in as_completed(futures):
        print(future.result()) # digest()の戻り値が表示される。

    # すべてのタスクの完了を待ち、後始末をする。
    # 完了していないタスクがあればブロックされる。
    # (上でas_completedをすべてイテレートしているので、実際にはこの時点で完了していないタスクは無いはず。)


def parse_args():
    parser = argparse.ArgumentParser()
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
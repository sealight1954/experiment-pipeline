import argparse
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

from sleep_bash_executor import SleepBashExecutor, SleepBashExecutor1, SleepBashExecutor2

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
    executor = ProcessPoolExecutor(max_workers=4)
    job_list = [ # job-name, executor, args, depends_on
        ["task1", sleep_executor1, "task1", None],
        ["task1-1", sleep_executor1, "task1-1", ["task1"]],
        ["task1-2", sleep_executor1, "task1-2", ["task1"]],
        ["task2", sleep_executor2, "task2", ["task1-1", "task1-2"]],
        ["task2-1", sleep_executor2, "task2-1", ["task2"]],
        ["task2-2", sleep_executor2, "task2-2", ["task2"]],
        ["task3", sleep_executor1, "task3", None],
    ]
    future_dict = {}
    # Executorオブジェクトにタスクをsubmitし、同数だけfutureオブジェクトを得る。
    # タスクの実行は、submit()を呼び出した瞬間から開始される。
    # ユーザーはこれを渡す
    # futures = [executor.submit(run_pipeline,t, sleep_executor) for t in range(3)]
    idx = 0
    submit_flags = [False] * len(job_list)
    while True:
        # print ("idx: {} started".format(idx))
        job_name, cmd_executor, cmd_args, job_dependency = job_list[idx]
        # print(job_list[idx])
        # print(job_name, cmd_executor, cmd_args, job_dependency)
        if submit_flags[idx]:
            idx = (idx + 1) % len(job_list)
            continue
        if job_dependency is None:
            future_dict[job_name] = executor.submit(cmd_executor.run, cmd_args)
            submit_flags[idx] = True
            print("submit because no dependency")
        else:
            ok_to_run = True
            for dependent_job_name in job_dependency:
                future_item = future_dict.get(dependent_job_name)
                if future_item is None or not future_item.done():
                    ok_to_run = False
                    break
            if ok_to_run:
                future_dict[job_name] = executor.submit(cmd_executor.run, cmd_args)
                submit_flags[idx] = True
                print("submit with dependency met: {}".format(job_dependency))
        if np.all(submit_flags):
            print("submit finished")
            break
        idx = (idx + 1) % len(job_list)
        time.sleep(0.5)
    
    futures = future_dict.values()
    # Note: submit job already started.

    # 各futureの完了を待ち、結果を取得。
    # as_completed()は、与えられたfuturesの要素を完了順にたどるイテレータを返す。
    # 完了したタスクが無い場合は、ひとつ完了するまでブロックされる。
    for future in as_completed(futures):
        print(future.result()) # digest()の戻り値が表示される。

    # すべてのタスクの完了を待ち、後始末をする。
    # 完了していないタスクがあればブロックされる。
    # (上でas_completedをすべてイテレートしているので、実際にはこの時点で完了していないタスクは無いはず。)
    executor.shutdown()


def parse_args():
    parser = argparse.ArgumentParser()
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
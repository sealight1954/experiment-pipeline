import argparse
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
# See: https://github.com/microsoft/ptvsd/issues/1056
import multiprocessing
multiprocessing.set_start_method('spawn', True)
from sleep_runner import SleepRunner1

def run_pipeline(p_id, executor):
    for i in range(3):
        executor.run("{}-{}".format(p_id, i))
    return "{} finished".format(p_id)


def main(args):
    sleep_runner = SleepRunner1()
    # run_pipeline("2", sleep_runner)
        # Executorオブジェクトを作成
    executor = ProcessPoolExecutor(max_workers=4)

    # Executorオブジェクトにタスクをsubmitし、同数だけfutureオブジェクトを得る。
    # タスクの実行は、submit()を呼び出した瞬間から開始される。
    # ユーザーはこれを渡す
    futures = [executor.submit(sleep_runner.run) for t in range(3)]
    time.sleep(5)
    # Note: submit job already started.
    print("Submit finished")

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
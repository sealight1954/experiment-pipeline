import concurrent.futures
import multiprocessing
multiprocessing.set_start_method('spawn', True)
import subprocess
import hashlib
"""
https://gist.github.com/tag1216/40b75346fd4ffdbfba22a55905094b0e#file-01_thread-py
https://blog.imind.jp/entry/2019/02/17/012210 
https://github.com/joblib/joblib/issues/864 ... multiprocessingのおまじない
https://takuya-1st.hatenablog.jp/entry/2016/04/11/044313 ... subprocessの仕様
"""

def digest(t): # 適当にCPU資源を消費するための関数
    hash = hashlib.sha256()
    for i in range(t*1000000):
        hash.update('hogehoge'.encode('utf-8'))
    return hash.hexdigest()

if __name__=='__main__':

    task_list = [1,1,1,2,2,3]
    cmd = ["sbatch", "submit.sh"]
    proc = subprocess.Popen(cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    res = proc.communicate()
    print(res)
    # Executorオブジェクトを作成
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=4)

    # Executorオブジェクトにタスクをsubmitし、同数だけfutureオブジェクトを得る。
    # タスクの実行は、submit()を呼び出した瞬間から開始される。
    futures = [executor.submit(digest,t) for t in task_list]

    # 各futureの完了を待ち、結果を取得。
    # as_completed()は、与えられたfuturesの要素を完了順にたどるイテレータを返す。
    # 完了したタスクが無い場合は、ひとつ完了するまでブロックされる。
    for future in concurrent.futures.as_completed(futures):
        print(future.result()) # digest()の戻り値が表示される。

    # すべてのタスクの完了を待ち、後始末をする。
    # 完了していないタスクがあればブロックされる。
    # (上でas_completedをすべてイテレートしているので、実際にはこの時点で完了していないタスクは無いはず。)
    executor.shutdown()
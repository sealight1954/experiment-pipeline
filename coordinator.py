import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
# See: https://github.com/microsoft/ptvsd/issues/1056
import multiprocessing
multiprocessing.set_start_method('spawn', True)

import numpy as np


class SequentialCoordinator:
    def __init__(self, log_dir="./results"):
        self.log_dir = log_dir

    def submit(self, job_list, dry_run=False):
        results = []
        for _, make_runner, cmd_kwargs, _ in job_list:
            cmd_runner = make_runner()
            cmd_kwargs["dry_run"] = dry_run
            results.append(cmd_runner(**cmd_kwargs))
        return results


class PoolCoordinator:
    def __init__(self, log_dir="./results", max_workers=4, coordinator_type="ProcessPool"):
        if coordinator_type == "ProcessPool":
            self.executor = ProcessPoolExecutor(max_workers=max_workers)
        elif coordinator_type == "ThreadPool":
            self.executor = ThreadPoolExecutor(max_workers=max_workers)
        else:
            print("Invalid coordinator_type: {}".format(coordinator_type))
            exit(1)
        self.future_list = []
        self.log_dir = log_dir

    # def _submit_with_args(self, make_runner, **kwargs):
    #     cmd_runner = make_runner()
    #     cmd_runner(**kwargs)

    def submit(self, job_list, dry_run=False):
        """
        Submit jobs to executor.
        Note that if there is dependency, it waits the 
        """
        # Executorオブジェクトにタスクをsubmitし、同数だけfutureオブジェクトを得る。
        # タスクの実行は、submit()を呼び出した瞬間から開始される。
        # ユーザーはこれを渡す
        future_dict = {}

        idx = 0
        submit_flags = [False] * len(job_list)
        while True:
            # print ("idx: {} started".format(idx))
            job_name, make_runner, cmd_kwargs, job_dependency = job_list[idx]
            # print(job_list[idx])
            # print(job_name, cmd_runner, cmd_args, job_dependency)
            if submit_flags[idx]:
                idx = (idx + 1) % len(job_list)
                continue
            if job_dependency is None:
                # cmd_runner = make_runner()
                cmd_kwargs["dry_run"] = dry_run
                # TODO: log file will be like following.
                # future_dict[job_name] = self.executor.submit(self.construct_and_run, make_runner, **cmd_kwargs, 
                # log_file="results/out_{job_name}.txt", err_file="results/err_{job_name}.txt")
                future_dict[job_name] = self.executor.submit(self.construct_and_run, make_runner, **cmd_kwargs)
                # future_dict[job_name] = self.executor.submit(cmd_runner, **cmd_kwargs)
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
                    # cmd_runner = make_runner()
                    cmd_kwargs["dry_run"] = dry_run
                    future_dict[job_name] = self.executor.submit(self.construct_and_run, make_runner, **cmd_kwargs)
                    # future_dict[job_name] = self.executor.submit(cmd_runner, **cmd_kwargs)
                    submit_flags[idx] = True
                    print("submit with dependency met: {}".format(job_dependency))
            if np.all(submit_flags):
                print("submit finished")
                break
            idx = (idx + 1) % len(job_list)
            time.sleep(0.5)  # TODO: may not be needed
        
        futures = list(future_dict.values())
        # 各futureの完了を待ち、結果を取得。
        # as_completed()は、与えられたfuturesの要素を完了順にたどるイテレータを返す。
        # 完了したタスクが無い場合は、ひとつ完了するまでブロックされる。
        results = []
        for idx, future in enumerate(as_completed(futures)):
            # TODO: Want to describe associated jobs to see order of finish, requires future_list.
            # job_name = [job_list[i] for i in range(len(job_list)) if future == futures[i]
            results.append(future.result())
            # print("[{}]: Results:{}".format(idx, future.result()))
        self.executor.shutdown()
        return results
        # return futures

    @staticmethod
    def construct_and_run(make_runner, **cmd_kwargs):
        cmd_runner = make_runner()
        return cmd_runner(**cmd_kwargs)
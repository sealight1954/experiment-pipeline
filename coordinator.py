import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np


class Coordinator:
    def __init__(self, max_workers=4):
        self.executor = ProcessPoolExecutor(max_workers=max_workers)
        self.future_list = []

    def submit(self, job_list):
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
            job_name, cmd_executor, cmd_args, job_dependency = job_list[idx]
            # print(job_list[idx])
            # print(job_name, cmd_executor, cmd_args, job_dependency)
            if submit_flags[idx]:
                idx = (idx + 1) % len(job_list)
                continue
            if job_dependency is None:
                future_dict[job_name] = self.executor.submit(cmd_executor.run, cmd_args)
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
                    future_dict[job_name] = self.executor.submit(cmd_executor.run, cmd_args)
                    submit_flags[idx] = True
                    print("submit with dependency met: {}".format(job_dependency))
            if np.all(submit_flags):
                print("submit finished")
                break
            idx = (idx + 1) % len(job_list)
            time.sleep(0.5)  # TODO: may not be needed
        
        futures = list(future_dict.values())
        self.future_list += futures
        # Note: submit job already started.
        return self.future_list
        # return futures
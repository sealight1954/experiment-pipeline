import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
# See: https://github.com/microsoft/ptvsd/issues/1056
import multiprocessing
multiprocessing.set_start_method('spawn', True)

import numpy as np


def run_with_args(make_runner, num_args, cmd_args):
    cmd_runner = make_runner()
    if num_args == 0:
        return cmd_runner.run()
    elif num_args == 1:
        return cmd_runner.run(cmd_args)
    else:
        return cmd_runner.run(*cmd_args)


class SequentialCoordinator:
    def __init__(self, log_dir="./results"):
        self.log_dir = log_dir

    def submit(self, job_list):
        results = []
        for job_name, make_runner, num_args, cmd_args, job_dependency in job_list:
            # cmd_runner = make_runner()
            # if num_args == 0:
            #     results.append(cmd_runner.run())
            # elif num_args == 1:
            #     results.append(cmd_runner.run(cmd_args))
            # else:
            #     results.append(cmd_runner.run(*cmd_args))
            results.append(run_with_args(make_runner, num_args, cmd_args))
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

    def _submit_with_args(self, make_runner, num_args, cmd_args):
        cmd_runner = make_runner()
        if num_args == 0:
            return self.executor.submit(cmd_runner.run)
        elif num_args == 1:
            return self.executor.submit(cmd_runner.run, cmd_args)
        else:
            return self.executor.submit(cmd_runner.run, *cmd_args)

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
            job_name, make_runner, num_args, cmd_args, job_dependency = job_list[idx]
            # print(job_list[idx])
            # print(job_name, cmd_runner, cmd_args, job_dependency)
            if submit_flags[idx]:
                idx = (idx + 1) % len(job_list)
                continue
            if job_dependency is None:
                future_dict[job_name] = self._submit_with_args(make_runner, num_args, cmd_args)
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
                    future_dict[job_name] = self._submit_with_args(make_runner, num_args, cmd_args)
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
import time
import os
import datetime
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
# See: https://github.com/microsoft/ptvsd/issues/1056
import multiprocessing
multiprocessing.set_start_method('spawn', True)

import numpy as np

from base_runner import run_cmd_and_print


def run_with_args(make_runner, num_args, cmd_args):
    cmd_runner = make_runner()
    if num_args == 0:
        return cmd_runner.run()
    elif num_args == 1:
        return cmd_runner.run(cmd_args)
    else:
        return cmd_runner.run(*cmd_args)

def dry_run_with_args(make_runner, num_args, cmd_args):
    cmd_runner = make_runner()
    if num_args == 0:
        return cmd_runner.run()
    elif num_args == 1:
        return cmd_runner.run(cmd_args)
    else:
        return cmd_runner.run(*cmd_args)

sbatch_base_str = """#!/bin/bash
#SBATCH --output={log_dir}/res_{job_name}_%j.txt
#SBATCH --error={log_dir}/err_{job_name}_%j.txt
#
#SBATCH --ntasks=1
#SBATCH --time=10:00
#SBATCH --mem-per-cpu=100
srun {command}
"""


class SbatchCoordinator:
    def __init__(self, log_dir="./results"):
        self.log_dir = log_dir

    def submit(self, job_list, dry_run=False):
        results = []
        job_id_dict = {}
        if dry_run:
            for job_name, make_runner, cmd_kwargs, job_dependency in job_list:
                job_id_dict[job_name] = "dummy"

        for job_name, make_runner, cmd_kwargs, job_dependency in job_list:
            
            now = datetime.datetime.now()
            tmp_str = now.strftime('%Y%m%d%H%M%S-{}.sh')
            tmp_dir = os.path.join(self.log_dir, "tmp")
            os.makedirs(tmp_dir, exist_ok=True)
            tmp_sbatch_path = os.path.join(tmp_dir, tmp_str.format(job_name))
            cmd_runner = make_runner()
            cmd_kwargs["dry_run"] = True
            command = cmd_runner(**cmd_kwargs)
            # command = " ".join(cmd_kwargs)
            with open(tmp_sbatch_path, 'w') as f:
                f.write(sbatch_base_str.format(log_dir=self.log_dir, job_name=job_name, command=command))
            if job_dependency is None:
                dependency_option = ""
            else:
                job_id_lst = [job_id_dict[job_name] for job_name in job_dependency]
                dependency_option = "--dependency=afterok:{} ".format(":".join(job_id_lst))
                
            cmd_to_run = "sbatch --parsable {dependency}--job-name={job_name} {filename}".format(
                dependency=dependency_option, job_name=job_name, filename=tmp_sbatch_path)
            # TODO: Add options for dependency
            if dry_run:
                print(cmd_to_run)
            else:
                job_id_dict[job_name] = run_cmd_and_print(cmd_to_run.split(" "), isReturnJobid=True)

            results.append(job_id_dict[job_name])
        return results


import time
import os
import datetime

import numpy as np

from base_runner import run_cmd_and_print

sbatch_base_str = """#!/bin/bash
#SBATCH --output={log_dir}/out_%j_{job_name}.txt
#SBATCH --error={log_dir}/err_%j_{job_name}.txt
#
#SBATCH --ntasks=1
#SBATCH --time=10:00
#SBATCH --mem-per-cpu=100
srun {command}
"""

def get_stdout_file(log_dir, job_name, job_id):
    """
    """
    # Note: This is duplicate but is needed because job_id is acquired after submitting sbatch.
    return "{log_dir}/out_{job_id}_{job_name}.txt".format(log_dir=log_dir, job_name=job_name, job_id=job_id)


def get_stderr_file(log_dir, job_name, job_id):
    return "{log_dir}/err_{job_id}_{job_name}.txt".format(log_dir=log_dir, job_name=job_name, job_id=job_id)


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
            tmp_str = now.strftime('%Y%m%d-%H%M%S-%f-{}.sh')
            tmp_dir = os.path.join(self.log_dir, "tmp")
            os.makedirs(tmp_dir, exist_ok=True)
            tmp_sbatch_path = os.path.join(tmp_dir, tmp_str.format(job_name))
            cmd_runner = make_runner()
            cmd_kwargs["dry_run"] = True
            actual_command = cmd_runner(**cmd_kwargs)
            # command = " ".join(cmd_kwargs)
            with open(tmp_sbatch_path, 'w') as f:
                f.write(sbatch_base_str.format(log_dir=self.log_dir, job_name=job_name, command=actual_command))
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
            print("Sbatch submit. Results [{}] will be stored in {}".format(actual_command, get_stdout_file(self.log_dir, job_name, job_id_dict[job_name])))
        return results


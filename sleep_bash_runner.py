from job_script.job_sleep import run_job_sleep
from base_bash_runner import BaseBashRunner


def get_sleep_cmd(id, n):
    command = ["python", "job_script/job_sleep.py"]
    command += ["--id", "{}_cmd".format(id)]
    command += ["--n", "{}".format(n)]
    return command

# TODO: Delete after debug.
# class SleepBashRunner0(BaseBashRunner):
#     def __init__(self):
#         base_command_args = ["python", "job_script/job_sleep.py"]
#         super(SleepBashRunner0, self).__init__(base_command_args)
    
#     def run(self):
#         return super().run()

class SleepBashRunner1(BaseBashRunner):
    def __init__(self):
        base_command_args = ["python", "job_script/job_sleep.py"]
        # base_command_args = []
        super(SleepBashRunner1, self).__init__(base_command_args)
    
    def run(self, id=0):
        args = ["--id", "{}_1".format(id)]
        return super().run(args)
    
    def dry_run(self, id=0):
        args = ["--id", "{}_1".format(id)]
        return super().dry_run(args)

class SleepBashRunner2(BaseBashRunner):
    def __init__(self):
        base_command_args = ["python", "job_script/job_sleep.py"]
        # base_command_args = []
        super(SleepBashRunner2, self).__init__(base_command_args)
    
    def run(self, id=0, n=5):
        args = ["--id", "{}_2".format(id)]
        args += ["--n", "{}".format(n)]
        return super().run(args)

    def dry_run(self, id=0, n=5):
        args = ["--id", "{}_2".format(id)]
        args += ["--n", "{}".format(n)]
        return super().dry_run(args)
from job_script.job_sleep import run_job_sleep
from base_bash_executor import BaseBashRunner

class SleepBashRunner(BaseBashRunner):
    def __init__(self):
        base_command_args = ["python", "job_script/job_sleep.py"]
        super(SleepBashRunner, self).__init__(base_command_args)
    
    def run(self, id):
        args = ["--id", id]
        return super().run(args)

class SleepBashRunner1(BaseBashRunner):
    def __init__(self):
        base_command_args = ["python", "job_script/job_sleep.py"]
        # base_command_args = []
        super(SleepBashRunner1, self).__init__(base_command_args)
    
    def run(self, id):
        args = ["--id", "{}_1".format(id)]
        return super().run(args)


class SleepBashRunner2(BaseBashRunner):
    def __init__(self):
        base_command_args = ["python", "job_script/job_sleep.py"]
        # base_command_args = []
        super(SleepBashRunner2, self).__init__(base_command_args)
    
    def run(self, id):
        args = ["--id", "{}_2".format(id)]
        return super().run(args)
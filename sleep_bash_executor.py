from job_script.job_sleep import run_job_sleep
from base_bash_executor import BaseBashExecutor

class SleepBashExecutor(BaseBashExecutor):
    def __init__(self):
        base_command_args = ["python", "job_script/job_sleep.py"]
        super(SleepBashExecutor, self).__init__(base_command_args)
    
    def run(self, id):
        args = ["--id", id]
        return super().run(args)

class SleepBashExecutor1(BaseBashExecutor):
    def __init__(self):
        base_command_args = ["python", "job_script/job_sleep.py"]
        # base_command_args = []
        super(SleepBashExecutor1, self).__init__(base_command_args)
    
    def run(self, id):
        args = ["--id", "{}_1".format(id)]
        return super().run(args)


class SleepBashExecutor2(BaseBashExecutor):
    def __init__(self):
        base_command_args = ["python", "job_script/job_sleep.py"]
        # base_command_args = []
        super(SleepBashExecutor2, self).__init__(base_command_args)
    
    def run(self, id):
        args = ["--id", "{}_2".format(id)]
        return super().run(args)
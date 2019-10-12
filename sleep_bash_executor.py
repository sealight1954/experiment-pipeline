from job_script.job_sleep import run_job_sleep
from base_bash_executor import BaseBashExecutor

class SleepBashExecutor(BaseBashExecutor):
    def __init__(self, base_command):
        super(SleepBashExecutor, self).__init__(base_command)
    
    def run(self, id):
        args = ["--id", id]
        return super().run(args)

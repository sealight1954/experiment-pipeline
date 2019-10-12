from job_script.job_sleep import run_job_sleep
from base_executor import BaseExecutor

class SleepExecutor(BaseExecutor):
    def __init__(self):
        self.i = 1
    
    def run(self, id):
        run_job_sleep(n=5, id=id)
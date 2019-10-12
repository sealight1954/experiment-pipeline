from job_script import job_sleep
from base_executor import BaseExecutor

class SleepExecutor(BaseExecutor):
    def __init__(self):
        return 0
    
    def run(self, id):
        job_sleep(n=5, id=id)
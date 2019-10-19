from job_script.job_sleep import run_job_sleep
from base_runner import BaseRunner

class SleepRunner(BaseRunner):
    def __init__(self):
        self.i = 1
    
    def run(self, id):
        run_job_sleep(n=5, id=id)


class SleepRunner1(BaseRunner):
    def __init__(self):
        self.i = 1
    
    def run(self, id):
        run_job_sleep(n=5, id="{}_1_func".format(id))

class SleepRunner2(BaseRunner):
    def __init__(self):
        self.i = 1
    
    def run(self, id, n):
        run_job_sleep(n=n, id="{}_2_func".format(id))
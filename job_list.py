from typing import overload

class Job(list):

    def __init__(self, job_name: str, make_runner, cmd_kwargs: dict, job_dependency):
        assert callable(make_runner), "make_runner must be a callable constructor of function."
        # tmp_func = make_runner()
        # assert callable(tmp_func), "function made by make_runner() must be a callable function."
        assert job_dependency is None or isinstance(job_dependency, list), "job_dependency need to be either None or list of job_names."
        super().__init__(
            [job_name, make_runner, cmd_kwargs, job_dependency]
        )

class JobList(list):
    def __init__(self, job_list):
        super().__init__()
        for job in job_list:
            self.append(Job(*job))
    
    def append(self, job):
        super().append(Job(*job))
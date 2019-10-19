from abc import abstractmethod, ABCMeta
import subprocess
import datetime
import os


def run_cmd_and_print(cmd, isReturnJobid=False, log_f=None, err_f=None):
    print("run command start: {}".format(" ".join(cmd)))
    if log_f is None:
        log_f = subprocess.PIPE
    if err_f is None:
        err_f = subprocess.PIPE
    comp_proc = subprocess.run(cmd, stdout=log_f, stderr=err_f)
    print(comp_proc.args, comp_proc.returncode)
    assert comp_proc.returncode == 1, "Error occured in: {}".format(" ".join(comp_proc.args))
    print("stdout: {}".format(comp_proc.stdout))
    print("stderr: {}".format(comp_proc.stderr))
    if isReturnJobid:
        # return comp_proc.stdout.rstrip().decode("utf-8") 
        return str(int(comp_proc.stdout))


class BaseRunner(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        NotImplementedError()
    
    @abstractmethod
    def __call__(self):
        NotImplementedError()


class BaseBashRunner(BaseRunner):
    def __init__(self, cmd_lst, log_file=None, err_file=None):
        self.base_cmd_args = cmd_lst
        now = datetime.datetime.now()
        time_str = now.strftime('%Y%m%d-%H%M%S-%f')
        if log_file is None:
            log_file = os.path.join('results', "{}.log".format(time_str))
        if err_file is None:
            err_file = os.path.join('results', "{}.err".format(time_str))
            
        self.log_file = log_file
        self.err_file = err_file
        self.log_f = open(self.log_file, 'w+')
        self.err_f = open(self.err_file, 'w+')


    def __call__(self, **kwargs):
        """
        subclass can call this method as
        runner.run(param1=param1, param2=param2) ...
        """
        # print(self.base_cmd_args, kwargs)
        dry_run = kwargs.pop('dry_run', False)
        cmd_args_to_run = self.base_cmd_args
        for key, value in kwargs.items():
            cmd_args_to_run += ["--{}".format(key), str(value)]
        if dry_run:
            print(" ".join(cmd_args_to_run))
            return " ".join(cmd_args_to_run)
        else:
            return run_cmd_and_print(cmd_args_to_run, log_f=self.log_f, err_f=self.err_f)


    
    def debug_f_print(self):
        self.log_f.write("test run: {}".format(" ".join(self.base_cmd_args)))
        self.log_f.flush()

# TODO: really need?
class BaseFuncRunner(BaseRunner):
    def __init__(self, run_func):
        self.run_func = run_func

    def __call__(self, **kwargs):
        dry_run = kwargs.pop("dry_run", False)
        if dry_run:
            print("Function: {}, Arguments: {}".format(self.run_func.__name__, kwargs))
        else:
            self.run_func(**kwargs)
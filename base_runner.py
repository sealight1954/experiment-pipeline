from abc import abstractmethod, ABCMeta
import subprocess


class BaseRunner(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        NotImplementedError()
    
    @abstractmethod
    def __call__(self):
        NotImplementedError()


def run_cmd_and_print(cmd, isReturnJobid=False):
    comp_proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(comp_proc.args, comp_proc.returncode)
    print("stdout: {}".format(comp_proc.stdout))
    print("stderr: {}".format(comp_proc.stderr))
    if isReturnJobid:
        # return comp_proc.stdout.rstrip().decode("utf-8") 
        return int(comp_proc.stdout)


class BaseBashRunner(BaseRunner):
    def __init__(self, cmd_lst):
        self.base_cmd_args = cmd_lst

    def __call__(self, **kwargs):
        """
        subclass can call this method as
        runner.run(param1=param1, param2=param2) ...
        """
        print(self.base_cmd_args, kwargs)
        cmd_args_to_run = self.base_cmd_args
        print(kwargs)
        for key, value in kwargs.items():
            cmd_args_to_run += ["--{}".format(key), str(value)]

        run_cmd_and_print(cmd_args_to_run)

    def dry_run(self, *args):

        if args is None:
            commands = " ".join(self.base_cmd_args)
        else:
            commands = " ".join(self.base_cmd_args + args)
        print(commands)
        return commands


# TODO: really need?
class BaseFuncRunner(BaseRunner):
    def __init__(self, run_func):
        self.run_func = run_func

    def __call__(self, **kwargs):
        self.run_func(**kwargs)
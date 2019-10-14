import subprocess

from base_runner import BaseRunner


def run_cmd_and_print(cmd, isReturnJobid=False):
    comp_proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(comp_proc.args, comp_proc.returncode)
    print("stdout: {}".format(comp_proc.stdout))
    print("stderr: {}".format(comp_proc.stderr))
    if isReturnJobid:
        return int(comp_proc.stdout)


class BaseBashRunner(BaseRunner):
    def __init__(self, cmd_lst):
        self.base_commands = cmd_lst

    def run(self, args):
        run_cmd_and_print(self.base_commands + args)
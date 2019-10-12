import subprocess
from utils import run_cmd_and_print

from base_executor import BaseExecutor
class BaseBashExecutor(BaseExecutor):
    def __init__(self, cmds):
        self.base_commands = cmds

    def run(self, args):
        run_cmd_and_print(self.base_commands + args)
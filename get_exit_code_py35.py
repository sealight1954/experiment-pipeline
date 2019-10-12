# python 3.5以上なら、https://docs.python.org/ja/3/library/subprocess.htmlの方法が使える
import subprocess

from utils import cmd_run_and_print

cmd = ["bash", "exit_1.sh"]
cmd_run_and_print(cmd)
# 1
cmd = ["sbatch", "submit.sh"]
cmd_run_and_print(cmd)
cmd = ["sbatch", "--parsable", "submit.sh"]
return_code = cmd_run_and_print(cmd, isReturnJobid=True)
print("return_code of func: {}".format(return_code))
cmd = ["srun", "hostname", "&"]
return_code = cmd_run_and_print(cmd, isReturnJobid=True)
print("return_code of func: {}".format(return_code))

# python 3.5以上なら、https://docs.python.org/ja/3/library/subprocess.htmlの方法が使える
import subprocess

from base_bash_executor import run_cmd_and_print

cmd = ["bash", "exit_1.sh"]
run_cmd_and_print(cmd)
# 1
cmd = ["sbatch", "submit.sh"]
run_cmd_and_print(cmd)
cmd = ["sbatch", "--parsable", "submit.sh"]
return_code = run_cmd_and_print(cmd, isReturnJobid=True)
print("return_code of func: {}".format(return_code))
cmd = ["srun", "hostname", "&"]
return_code = run_cmd_and_print(cmd, isReturnJobid=True)
print("return_code of func: {}".format(return_code))

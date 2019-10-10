# python 3.5以上なら、https://docs.python.org/ja/3/library/subprocess.htmlの方法が使える
import subprocess

def cmd_run_and_print(cmd):
    comp_proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(comp_proc.args, comp_proc.returncode)
    print("stdout: {}".format(comp_proc.stdout))
    print("stderr: {}".format(comp_proc.stderr))

cmd = ["bash", "exit_1.sh"]
cmd_run_and_print(cmd)
# 1
cmd = ["sbatch", "submit.sh"]
cmd_run_and_print(cmd)
cmd = ["sbatch", "--parsable", "submit.sh"]
cmd_run_and_print(cmd)
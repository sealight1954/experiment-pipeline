import os
import sys
import subprocess
import time

# 下記のコマンドでもいけるが、python 3.5以上なら、https://docs.python.org/ja/3/library/subprocess.htmlの方法が使える
cmd = ['sbatch','submit.sh', '--parsable']
# cmd = ['sbatch','submit.sh', '--parsable']
#  /home/semitsu/anaconda3/envs/slurm/bin/python /home/semitsu/workspace/debug_srun/return_code_popen.py
# RETURN CODE 0
# cmd = ['bash','exit_1.sh']
# >>> 1
# cmd = ['echo','hello']
# >>> 0
p = subprocess.Popen(cmd,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
try:
    # Filter stdout
    for line in iter(p.stdout.readline, ''):
        sys.stdout.flush()
        # Print status
        print(">>> " + line.rstrip())
        sys.stdout.flush()
except:
    sys.stdout.flush()

# Wait until process terminates (without using p.wait())
while p.poll() is None:
    # Process hasn't exited yet, let's wait some
    time.sleep(0.5)

# Get return code from process
return_code = p.returncode

print ('RETURN CODE', return_code)

# Exit with return code from process
sys.exit(return_code)
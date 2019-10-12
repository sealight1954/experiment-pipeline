import time
import argparse


def run_job_sleep(n=5, id=0):
    print("[{}]: start, sleep {}".format(id, n))
    time.sleep(n)
    print("[{}]: end.".format(id))
    return

def main(args):
    run_job_sleep(args.n, args.id)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", default=5, type=int,
        help="time to sleep")
    parser.add_argument("--id", default=0, type=int,
        help="id to identify job.")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main(parse_args())
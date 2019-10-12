import time
import argparse

def job_sleep(n=5, id=0):
    print("[{}]: start, sleep {}".format(id, n))
    time.sleep(n)
    print("[{}]: end.")

def main(args):
    job_sleep(args.n, args.id)

def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("--n", default=5, type=int,
        help="time to sleep")
    args.add_argument("--id", default=0, type=int,
        help="id to identify job.")

if __name__ == "__main__":
    main(parse_args())
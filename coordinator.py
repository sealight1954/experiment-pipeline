import argparse

from sleep_executor import SleepExecutor

def run_pipeline(p_id, run_func):
    for i in range(5):
        run_func.run("{}-{}".format(p_id, i))


def main(args):
    sleep_executor = SleepExecutor()
    sleep_executor.run("1")
    run_pipeline("2", sleep_executor)


def parse_args():
    parser = argparse.ArgumentParser()
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
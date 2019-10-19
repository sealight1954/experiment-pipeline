def func(**kwargs):
    print(kwargs)

def func2(a=2, key=5):
    print(a, key)


if __name__ == "__main__":
    func(**{"key": 3})
    func(**{})
    func()
    func2(**{"key": 7, "b": 8})
    for key, value in {'id': 'task2-1', 'n': 4}.items():
        print(key, value)
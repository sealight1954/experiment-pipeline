import datetime

class SomeClass():
    def __init__(self):
        now = datetime.datetime.now()
        self.time_str = now.strftime('%Y%m%d-%H%M%S-%f')
        print(self.time_str)


    def func(self, message):
        print("{}".format(message))
        print(self.time_str)


if __name__ == "__main__":
    obj1 = SomeClass()
    obj2 = SomeClass()
    obj1.func("obj1")
    obj2.func("obj2")
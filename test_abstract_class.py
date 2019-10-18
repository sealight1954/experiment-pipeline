from abc import ABCMeta, abstractmethod

class Parent(metaclass=ABCMeta):
    def master_func(self):
        self._slave_func()
    
    @abstractmethod
    def _slave_func(self):
        NotImplementedError()

class Child(Parent):
    def func(self):
        self.master_func()
    
    def _slave_func(self):
        print("slave func defined in Child, called by Parent")


if __name__ == "__main__":
    child = Child()
    child.func()
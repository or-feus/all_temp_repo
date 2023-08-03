from abc import ABCMeta, ABC, abstractmethod


class Parent(metaclass=ABCMeta):

    def __init__(self, x):
        self.x = x

    @abstractmethod
    def say(self):
        pass


class Child(Parent):

    def __init__(self, x):
        self.x = x

    def say(self):
        return "good"


x = Parent(10)
print(x)

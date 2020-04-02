from abc import ABC, abstractmethod


# Abstract class will be used by different platforms like gitlab.py file
class UserPlatform(ABC):

    @abstractmethod
    def addUser(self):
        pass

    @abstractmethod
    def removeUser(self):
        pass

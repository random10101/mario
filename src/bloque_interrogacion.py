

from random import randint

class BloqueInterrogación:
    def __init__(self):
        self.__x = randint(100, 256)
        self.__y = randint(56, 156)
        self.__vx = 0

    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y


    def update(self):
        pass
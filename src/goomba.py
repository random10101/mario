import random
import pyxel

class Goomba:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__vx = 1

        self.draw = (49, 2)
        self.width = 14
        self.height = 13

    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y

    def update(self):
        self.movement()

    def movement(self):
        if self.__x < 0 or self.__x > 240: 
            self.__vx = -self.__vx
        self.__x += self.__vx
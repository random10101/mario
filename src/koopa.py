import random

class KoopaTroopa:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__vx = 1

        self.draw = (17, 0)
        self.width = 14
        self.height = 15


    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y

    def update(self):
        self.Mover()

    def Mover(self):
        if self.__x < 0 or self.__x > 240: #En verdad sería si colisiona con algun objeto, pero bueno, lo he hecho para probar
            self.__vx = -self.__vx
        self.__x += self.__vx
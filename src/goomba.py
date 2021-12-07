import random

class Goomba:
    def __init__(self):
        self.__x = random.randint(150, 254)
        self.__y = 50
        self.__vx = 3
        self.__vy = 5


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
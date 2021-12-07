import pyxel
from . import BloqueInterrogación



class Mario:
    def __init__(self):
        self.__is_alive = True
        self.__x = 32
        self.__y = 200
        self.__vx = 0
        self.__vy = 0

    @property
    def x(self):
        return self.__x
    
    @property
    def vx(self):
        return self.__vx
    
    @property
    def y(self):
        return self.__y

    def update(self):
        self.move()
        self.jump()

    def move(self):
        # Intervalo válido x: (0, pyxel.height/2)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.__vx = max(self.__vx-1, -8)
            self.__x = max(self.__x+self.__vx, 0)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.__vx = min(self.__vx+1, 8)
            self.__x = min(self.__x+self.__vx, pyxel.height/2)
        else:
            self.__vx = 0
    
    def jump(self):
        # Intervalo válido y: (0, 200)
        if pyxel.btn(pyxel.KEY_SPACE):
            self.__vy = max(self.__vy-2, -8)
        elif self.__y >= 200:
            self.__vy = 0
        else: 
            self.__vy = min(self.__vy + 1, 8)
        self.__y = min(self.__y+self.__vy, 200) 
    
    def Chocar(self, objeto: BloqueInterrogación):
        if objeto.x >= self.__x and objeto.x + 8 <= self.__x:
            self.__vx = 0

    
import pyxel


class Estrella:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__vx = 3
        self.__vy = 5

        self.draw = (16, 43)
        self.width = 16
        self.height = 16


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

        # if pyxel.frame_count % 2 == 0: #Más o menos funciona que salte y rebote, pero creo que haria falta hacer las colisiones
        #     self.__y += 48
        # else:
        #     self.__y -= 48 
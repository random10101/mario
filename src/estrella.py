import pyxel


class Estrella:
    def __init__(self):
        self.__x = 100
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

        if pyxel.frame_count % 2 == 0: #Más o menos funciona que salte y rebote, pero creo que haria falta hacer las colisiones
            self.__y += 48
        else:
            self.__y -= 48 
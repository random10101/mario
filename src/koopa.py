import random

class KoopaTroopa:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y - 15
        self.__vx = 1
        self.wall_left = False
        self.wall_right = False

        self.draw = (17, 0)
        self.width = 14
        self.height = 15

        self.movement_range = (self.__x-self.width*2, self.__x+self.width*2)

    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y

    def reset_collisions(self):
        self.wall_left = False
        self.wall_right = False

    def touch_right(self, x):
        # Evento de choque por la derecha
        self.__x = x - self.width
        self.wall_right = True

    def touch_left(self, x):
        # Evento de choque por la izquierda
        self.__x = x - self.width
        self.wall_left = True

    def update(self, mario):
        if mario.x > 32:
            if mario.vx > 0 and not mario.wall_right[0]: 
                # Mario se mueve hacia la derecha y no hay un objeto a su derecha
                self.__x -= mario.vx
                # Mover el rango de movimiento cuando Mario avanza
                self.movement_range = tuple(x-mario.vx for x in self.movement_range)
            elif mario.vx < 0 and not mario.wall_left[0]: 
                # Mario se mueve a la izquierda y no hay un objeto a su izquierda
                self.__x -= mario.vx
                # Actualizar el rango de movimiento cuando Mario retrocede
                self.movement_range = tuple(x-mario.vx for x in self.movement_range)

        # Cambiar la dirección del movimiento si se sale del rango de movimiento o colisiona con un objeto
        if self.__x < self.movement_range[0] or self.__x > self.movement_range[-1] or (self.__vx > 0 and self.wall_right) or (self.__vx < 0 and self.wall_left): 
            self.__vx = -self.__vx
        self.__x += self.__vx

        self.reset_collisions()
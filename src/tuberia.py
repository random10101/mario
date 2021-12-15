import pyxel
import random

class Tuberia:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.draw = (79, 178)

        self.width = 32
        self.height = 47

    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
        
    def mario_collisions(self, mario):
        # mario choca por su derecha
        if (self.__x <= mario.x+mario.width <= self.__x+8) and ((self.__y <= mario.y+mario.height <= self.__y+self.height) or (self.__y < mario.y < self.__y+self.height)):
            mario.touch_right(self.__x)

        # mario choca por su izquierda
        if (self.__x+self.width-8 <= mario.x <= self.__x+self.width) and ((self.__y <= mario.y+mario.height <= self.__y+self.height) or (self.__y < mario.y < self.__y+self.height)):
            mario.touch_left(self.__x+self.width+mario.width)

        # mario choca por abajo
        if ((self.__x <= mario.x <= self.__x+self.width) or (self.__x <= mario.x+mario.width <= self.__x+self.width)) and (self.__y-16 <= mario.y+mario.height <= self.__y):
            mario.touch_bottom(self.__y)
        else:
            # resetear la distancia al suelo de referencia para que mario pueda caer
            mario.reset_distance_to_floor()

    def enemies_collisions(self, enemies):
        for enemy in enemies:
            # Enemigo choca por su derecha
            if (self.__x <= enemy.x+enemy.width <= self.__x+8) and ((self.__y <= enemy.y+enemy.height <= self.__y+self.height) or (self.__y < enemy.y < self.__y+self.height)):
                enemy.touch_right(self.__x)

            # Enemigo choca por su izquierda
            if (self.__x+self.width-8 <= enemy.x <= self.__x+self.width) and ((self.__y <= enemy.y+enemy.height <= self.__y+self.height) or (self.__y < enemy.y < self.__y+self.height)):
                enemy.touch_left(self.__x+self.width+enemy.width)

    def mario_movement(self, mario):
        if mario.vx > 0 and not mario.wall_right[0]: 
            # mario se mueve hacia la derecha y no hay un objeto a su derecha
            self.__x -= mario.vx
        elif mario.vx < 0 and not mario.wall_left[0]: 
            # mario se mueve a la izquierda y no hay un objeto a su izquierda
            self.__x -= mario.vx

    def update(self, mario, is_closest, *args):
        if is_closest: # Calcular colisiones solo en el objeto más cercano
            self.mario_collisions(mario)

        if args[0]: # Iterable de enemigos en el mapa
            self.enemies_collisions(args[0])

        if mario.x >= 128:
            # Actualizar el movimiento de la tubería con respecto a Mario
            self.mario_movement(mario)  
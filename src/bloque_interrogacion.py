import random

class BloqueInterrogación:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

        self.draw = (177, 27)
        self.width = 16
        self.height = 16

        self.hidden = True
        self.show = False
        self.mistery_object_name = self.generate_object()

    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y

    def generate_object(self):
        # Generar objeto aleatorio entre monedas, flores y setas
        all_objects = ['flor', 'seta', 'moneda']
        return random.choice(all_objects)

    def show_object(self):
        # Crear un contador para asegurar que el objeto especial solo se crea una vez
        if self.hidden:
            self.show = True
            self.hidden = False

    def update(self, mario, is_closest):
        self.show = False
        # comprobar colisiones solo con el bloque más cerana a mario
        if is_closest:
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
                # resetear la distancia al suelo de referencia para que pueda caer al suelo
                mario.reset_distance_to_floor()

            # mario choca por arriba
            if ((self.__x <= mario.x <= self.__x+self.width) or (self.__x <= mario.x+mario.width <= self.__x+self.width)) and (self.__y <= mario.y <= self.__y+self.height):
                self.show_object()
                mario.touch_top(self.__y+self.height)
                self.draw = (145, 27)

        if mario.x >= 128:
            if mario.vx > 0 and not mario.wall_right[0]: 
                # mario se mueve hacia la derecha y no hay un objeto a su derecha
                self.__x -= mario.vx
            elif mario.vx < 0 and not mario.wall_left[0]: 
                # mario se mueve a la izquierda y no hay un objeto a su izquierda
                self.__x -= mario.vx
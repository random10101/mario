class Tuberia:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.draw = (79, 178)

        self.width = 32
        self.height = 47

    def update(self, mario, is_closest):
        # comprobar colisiones colo con la tubería más cerana a mario
        if is_closest:
            # mario choca por su derecha
            if (self.x <= mario.x+mario.width <= self.x+8) and ((self.y <= mario.y+mario.height <= self.y+self.height) or (self.y < mario.y < self.y+self.height)):
                mario.touch_right(self.x)

            # mario choca por su izquierda
            if (self.x+self.width-8 <= mario.x <= self.x+self.width) and ((self.y <= mario.y+mario.height <= self.y+self.height) or (self.y < mario.y < self.y+self.height)):
                mario.touch_left(self.x+self.width+mario.width)

            # mario choca por abajo
            if ((self.x <= mario.x <= self.x+self.width) or (self.x <= mario.x+mario.width <= self.x+self.width)) and (self.y-16 <= mario.y+mario.height <= self.y):
                mario.touch_bottom(self.y)
            else:
                # resetear la distancia al suelo de referencia para que pueda caer al suelo
                mario.reset_distance_to_floor()

        if mario.x > 32:
            if mario.vx > 0 and not mario.wall_right[0]: 
                # mario se mueve hacia la derecha y no hay un objeto a su derecha
                self.x -= mario.vx
            elif mario.vx < 0 and not mario.wall_left[0]: 
                # mario se mueve a la izquierda y no hay un objeto a su izquierda
                self.x -= mario.vx
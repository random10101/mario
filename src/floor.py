import pyxel

class Floor:
    def __init__(self, x, y):
        self.height = 16
        self.width = 16
        self.x = x
        self.y = y
        
        self.latest_x = None
        self.draw = (0, 227)

    def update(self, mario):
        # Actualizar posición del suelo
        if mario.x >= 128:
            if mario.vx > 0 and not mario.wall_right[0]: # mario se mueve hacia adelante
                self.x -= mario.vx
            elif mario.vx < 0 and not mario.wall_left[0]: # mario se mueve hacia atrás
                self.x -= mario.vx
        
        # Regenerar los bloques de suelo
        if self.x < -pyxel.width: 
            self.x = self.latest_x + 16
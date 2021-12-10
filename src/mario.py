import pyxel
from . import BloqueInterrogación



class Mario:
    def __init__(self):
        self.__is_alive = True
        self.__x = 32
        self.__y = 200
        self.__vx = 0
        self.__vy = 0
        self.height = 16
        self.width = 16

        self.jumping = False
        self.double_jumping = False
        self.distance_to_floor = 200
        self.reset_collisions()

    @property
    def x(self):
        return self.__x
    
    @property
    def vx(self):
        return self.__vx
    
    @property
    def y(self):
        return self.__y

    def reset_collisions(self):
        # Resetear el sistema de colisiones
        self.wall_top = (False, 0)
        self.wall_bottom = (False, 0)
        self.wall_left = (False, 0)
        self.wall_right = (False, 0)

    def reset_distance_to_floor(self):
        self.distance_to_floor = 200

    def update(self):
        self.reset_collisions()
        self.move()
        self.jump()

    def move(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.__vx = max(self.__vx-1, -4) 
            self.__x = max(self.__x+self.__vx, 0)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.__vx = min(self.__vx+1, 4) 
            self.__x = min(self.__x+self.__vx, pyxel.height/2)
        else:
            self.__vx = 0
    
    def jump(self):
        if pyxel.btn(pyxel.KEY_SPACE) and not self.double_jumping:
            self.__vy = max(self.__vy-6, -12)
            if self.jumping:
                self.double_jumping = True
            else:
                self.jumping = True

        elif self.__y >= self.distance_to_floor:
            self.__vy = 0
            if self.double_jumping:
                self.double_jumping = False
            else:
                self.jumping = False

        else: 
            self.__vy = min(self.__vy + 1, 8)
        self.__y = min(self.__y+self.__vy, self.distance_to_floor) 
    
    def touch_bottom(self, y):
        # Evento de choque por abajo
        self.__y = min(self.y, y+self.height)
        self.wall_bottom = (True, y)
        self.distance_to_floor = y - 16

    def touch_right(self, x):
        # Evento de choque por la derecha
        self.__x = x - self.width
        self.wall_right = (True, x)

    def touch_left(self, x):
        # Evento de choque por la izquierda
        self.__x = x - self.width
        self.wall_left = (True, x)

    def touch_top(self):
        # Evento de choque por arriba
        pass 
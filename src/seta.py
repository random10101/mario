from src.mario import Mario


class Champiñon:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y - 15
        self.__vx = 3
        self.__is_active = True

        self.draw = (0, 45)
        self.width = 14
        self.height = 15

    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y

    def touch(self, mario: Mario):
        # Evento de interacción con Mario
        # Primero se comprueba si están en el mismo espacio en la coordenada x y luego en el mismo espacio en la coordenada y
        if (self.__x <= mario.x <= self.__x+self.width or self.__x <= mario.x+mario.width <= self.__x+self.width) and (self.__y <= mario.y <= self.__y+self.width or  self.__y <= mario.y+mario.height <= self.__y+self.width):
            return True
        else:
            return False

    def update(self, mario: Mario, is_closest):
        if self.__x < 0:
            self.__vx = -self.__vx
        elif self.__x > 256 - self.width:
            self.__vx = -self.__vx
        self.__x += self.__vx
        
        
        # mario colisiona con la seta más cercana
        # if is_closest and self.__is_active:
        if self.touch(mario):
            mario.supermario = True
                
        

        if mario.x >= 128:
            if mario.vx > 0 and not mario.wall_right[0]: 
                # mario se mueve hacia la derecha y no hay un objeto a su derecha
                self.__x -= mario.vx
            elif mario.vx < 0 and not mario.wall_left[0]: 
                # mario se mueve a la izquierda y no hay un objeto a su izquierda
                self.__x -= mario.vx
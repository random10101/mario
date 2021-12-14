class Moneda:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y - 13

        self.draw = (2, 29)
        self.width = 9
        self.height = 13

    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y

    def touch(self, mario):
        # handle mario interaction
        pass

    def update(self, mario, is_closest):
        # Evento de interacción con Mario
        self.touch(mario)

        if mario.x > 32:
            if mario.vx > 0 and not mario.wall_right[0]: 
                # mario se mueve hacia la derecha y no hay un objeto a su derecha
                self.__x -= mario.vx
            elif mario.vx < 0 and not mario.wall_left[0]: 
                # mario se mueve a la izquierda y no hay un objeto a su izquierda
                self.__x -= mario.vx
class FlorDeFuego:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y - 14

        self.draw = (55, 47)
        self.width = 14
        self.height = 14
         

    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y

    def touch(self, mario):
        # Evento de interacción con Mario
        pass

    def update(self, mario, is_closest):
        # mario colisiona con la flor
        self.touch(mario)

        if mario.x >= 128:
            if mario.vx > 0 and not mario.wall_right[0]: 
                # mario se mueve hacia la derecha y no hay un objeto a su derecha
                self.__x -= mario.vx
            elif mario.vx < 0 and not mario.wall_left[0]: 
                # mario se mueve a la izquierda y no hay un objeto a su izquierda
                self.__x -= mario.vx
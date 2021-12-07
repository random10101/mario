import pyxel
import src

class App:
    def __init__(self):
        self.score = None
        self.timer = None

        self.clouds = [(-10, 50), (40, 75)]

        self.mario = src.Mario()

        self.Koopa = src.KoopaTroopa()
        self.__bloques_interrogacion = self.CrearBloquesInterrogacion(4)
        self.Estrella = src.Estrella()

        self.CrearBloquesInterrogacion(4)
        pyxel.init(256, 256)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.mario.update()
        self.Koopa.update()
        self.Estrella.update()


    def CrearBloquesInterrogacion(self, num_bloques):
        bloquesInterrogacion = []
        for i in range(num_bloques):
            bloquesInterrogacion.append(src.BloqueInterrogación())
        return bloquesInterrogacion


    def draw(self):
        pyxel.load("assets/mario.pyxres")
        pyxel.cls(12)

        # Pintar suelo
        for i in range(16):
            for j in range(3):
                pyxel.blt(16 * i, 216 + 16 * j, 0, 0, 227, 16, 16)
        
        
        # Pintar nubes
        offset = (pyxel.frame_count // 16) % 160
        for i in range(3):
            for x, y in self.clouds:
                pyxel.blt(x + i * 160 - offset, y, 0, 139, 46, 63, 16)


        # Pintar escalera de bloques lisos
        pyxel.blt(144, 152, 0, 0, 62, 16, 16)

        for i in range(2):
            pyxel.blt(128 + 16 * i, 168, 0, 0, 62, 16, 16)

        for i in range(3):
            pyxel.blt(112 + 16 * i, 184, 0, 0, 62, 16, 16)
        
        for i in range(4):
            pyxel.blt(96 + 16 * i, 200, 0, 0, 62, 16, 16)


        # Pintar bloques de interrogación
        for item in self.__bloques_interrogacion:    
            pyxel.blt(item.x, item.y, 0, 177, 27, 16, 16)

        # Pintar tuberia
        pyxel.blt(32, 169, 0, 79, 178, 32, 47, 12)

        # Pintar "Koopa", que no es un koopa, pero para hacer pruebas va a ser un koopa
        pyxel.blt(self.Koopa.x, self.Koopa.y, 0, 177, 27, 16, 16, 12)

        # Pintar estrella
        pyxel.blt(self.Estrella.x, self.Estrella.y, 0, 16, 43, 16, 16, 12)
        

        # Pintar Mario
        if self.mario.vx > 0:
            if pyxel.frame_count % 8 <= 4 and self.mario.vx > 1:
                pyxel.blt(self.mario.x, self.mario.y, 0, 18, 99, 16, 15, 12)
            else:
                pyxel.blt(self.mario.x, self.mario.y, 0, 0, 98, 16, 16, 12)
        elif self.mario.vx < 0:
            if pyxel.frame_count % 8 <= 4 and self.mario.vx < -1:
                pyxel.blt(self.mario.x, self.mario.y, 0, 18, 99, -16, 15, 12)
            else:
                pyxel.blt(self.mario.x, self.mario.y, 0, 0, 98, -16, 16, 12)
        else:
            pyxel.blt(self.mario.x, self.mario.y, 0, 0, 98, 16, 16, 12)


App()
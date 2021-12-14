import pyxel
import random
import src


class App:
    def __init__(self):
        self.score = 0
        self.timer = src.Timer()
        self.coins = 0

        self.clouds = [(-10, 50), (40, 75)]

        self.mario = src.Mario()

        # Generar nivel
        self.floors = self.create_floors()
        self.blocks_row = self.generate_blocks()
        self.pipes = self.create_pipes()

        # Objetos
        self.coins_objects = []
        self.mistery_objects = []

        # Generar enemigos
        self.goombas = self.create_goombas()
        self.koopas = self.create_koopas()
        self.stars = self.create_stars()

        pyxel.init(256, 256)
        pyxel.run(self.update, self.draw)

    # Generar bloques
    def generate_blocks(self, pixel_start=128):
        # Crear filas de 3-5 blockes a una altura fija
        n_row = random.randint(3, 5)
        dispatch = [src.BloqueRompible, src.BloqueMonedas, src.BloqueInterrogación, src.BloqueLiso]

        blocks = []
        for i in range(n_row):
            block = random.choice(dispatch)(16*i+pixel_start, 150)
            blocks.append(block)

        latest_block_x = blocks[-1].x + blocks[-1].width
        if random.randint(0, 1): # Generar segundo nivel de bloques
            for i in range(1, n_row-2):
                block = random.choice(dispatch)(16*i+latest_block_x, 102)
                blocks.append(block) 

        return blocks

    # Generar enemigos
    def generate_enemies(self):
        # # Comprobar que no hay más de 4 enemigos activos
        # weights = [0.75, 0.25]
        # enemy = random.choices(enemies, weights)
        pass


    def latest_floor(self):
        return max(self.floors, key=lambda obj: obj.x)

    def create_floors(self):
        # Crear 144 suelos: (-pyxel.width, 2*pyxel.width)
        floors = []
        for i in range(-16, 32):
            for j in range(3):
                floor = src.Floor(16*i, 216+16*j)
                floors.append(floor)
        return floors

    def create_pipes(self):
        pipes = [src.Tuberia(268, 169)]
        return pipes

    def create_goombas(self):
        goombas = [src.Goomba(240, 203), 
                   src.Goomba(240*2, 200)]
        return goombas

    def create_koopas(self):
        koopas = [src.KoopaTroopa(140, 201), 
                  src.KoopaTroopa(140*2, 200)]
        return koopas

    def create_stars(self):
        stars = [src.Estrella(140, 155), 
                  src.Estrella(140*2, 155)]
        return stars

    def is_closest_object_to_mario(self, item):
        all_objects = self.pipes + self.blocks_row + self.mistery_objects
        return min(all_objects, key=lambda obj: abs(obj.x-self.mario.x)).x == item.x

    def is_closest_block(self, block):
        return min(self.blocks_row, key=lambda obj: abs(obj.x-self.mario.x)) == block

    def update(self):
        self.timer.update()

        self.mario.update()
        

        # Actualizar tuberias
        for pipe in self.pipes:
            is_closest = self.is_closest_object_to_mario(pipe)
            pipe.update(self.mario, is_closest)

        # Actualizar bloques
        for block in self.blocks_row:
            is_closest_block = self.is_closest_object_to_mario(block)
            block.update(self.mario, is_closest_block)

            # Actualizar objetos de bloques interrogación
            if hasattr(block, 'mistery_object_name') and block.show:
                objs = {'flor':src.FlorDeFuego, 'seta':src.Champiñon, 'moneda':src.Moneda}
                mistery_object_name = block.mistery_object_name
                block_object = objs[mistery_object_name](block.x, block.y)
                if not block_object in self.mistery_objects:
                    self.mistery_objects.append(block_object)

        # Generar una fila de bloques al principio del mapa
        if self.blocks_row[-1].x < -pyxel.width:
            self.blocks_row = self.generate_blocks(256)
        
        # Actualizar suelos
        latest_floor = self.latest_floor()
        for item in self.floors:
            item.latest_x = latest_floor.x
            item.update(self.mario)

        # Actualizar goombas
        for goomba in self.goombas:
            goomba.update()

        # Actualizar koopas
        for koopa in self.koopas:
            koopa.update()

        # Actualizar estrellas
        for star in self.stars:
            star.update()

        # Actualizar objetos especiales
        for item in self.mistery_objects:
            is_closest = self.is_closest_object_to_mario(block)
            item.update(self.mario, is_closest)

    def draw_score(self):
            # Pintar puntuación
            s = "MARIO \n{:>5}".format(self.score)
            pyxel.text(5, 4, s, 1)
            pyxel.text(4, 4, s, 7)

            # Pintar contador monedas
            s = "MONEDAS \n{:>7}".format(self.coins)
            pyxel.text(90, 4, s, 1)
            pyxel.text(89, 4, s, 7)

            # Pintar timer
            s = "TIME \n{:>4}".format(self.timer.t)
            pyxel.text(45, 4, s, 1)
            pyxel.text(44, 4, s, 7)

    def draw(self):
        pyxel.load("assets/mario.pyxres")
        pyxel.cls(12)
        
        # Pintar suelo
        for item in self.floors:
            pyxel.blt(item.x, item.y, 0, *item.draw, 16, 16)
        
        # Pintar filas de bloques
        for block in self.blocks_row:
            pyxel.blt(block.x, block.y, 0, *block.draw, block.width, block.height, 12)

        # Pintar objectos especiales
        for item in self.mistery_objects:
            pyxel.blt(item.x, item.y, 0, *item.draw, item.width, item.height, 12)

        # Pintar nubes
        offset = (pyxel.frame_count // 16) % 160
        for i in range(3):
            for x, y in self.clouds:
                pyxel.blt(x + i * 160 - offset, y, 0, 139, 46, 63, 16)

        # Pintar escalera de bloques lisos
        # pyxel.blt(144, 152, 0, 0, 62, 16, 16)

        # for i in range(2):
        #     pyxel.blt(128 + 16 * i, 168, 0, 0, 62, 16, 16)

        # for i in range(3):
        #     pyxel.blt(112 + 16 * i, 184, 0, 0, 62, 16, 16)
        
        # for i in range(4):
        #     pyxel.blt(96 + 16 * i, 200, 0, 0, 62, 16, 16)


        # Pintar tuberias
        offset = (pyxel.frame_count // 16) % 160
        for pipe in self.pipes:
            pyxel.blt(pipe.x, pipe.y, 0, *pipe.draw, 32, 47, 12)

        # Pintar goombas
        for goomba in self.goombas:
            pyxel.blt(goomba.x, goomba.y, 1, *goomba.draw, goomba.width, goomba.height)

        # Pintar koopas
        for koopa in self.koopas:
            pyxel.blt(koopa.x, koopa.y, 1, *koopa.draw, koopa.width, koopa.height)

        # Pintar estrellas
        for star in self.stars:
            pyxel.blt(star.x, star.y, 0, *star.draw, star.width, star.height, 12)
        

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

        self.draw_score()
        
        

App()
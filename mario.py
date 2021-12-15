import pyxel
import time
import random
import src


class App:
    def __init__(self):
        self.end_is_showing = False
        self.games = 3
        self.__reset()
        self.mario = src.Mario()

        pyxel.init(256, 256)
        pyxel.run(self.update, self.draw)

    def __reset(self):
        self.end = False
        self.score = 0
        self.timer = src.Timer()
        self.coins = 0
        self.distance_done = 0      

        self.clouds = [(-10, 50), (40, 75)]
        self.mountains = [(25, 183), (215, 183)]

        # Generar nivel
        self.floors = self.create_floors()
        self.blocks_row = self.generate_blocks()
        self.pipes = self.create_pipes()
        
        # Objetos
        self.coins_objects = []
        self.mistery_objects = []
        self.enemies = []

    def empty_x_positions(self):
        return [p.x for p in self.blocks_row]

    # Generar tuberías
    def create_pipes(self):
        valid_positions = self.empty_x_positions()
        # Generar tubería después de la fila bloques
        n = random.randint(45, 90)
        pipes = [src.Tuberia(valid_positions[-1]+n, 169)]
        return pipes

    # Generar bloques
    def generate_blocks(self, pixel_start=128):
        # Crear filas de 3-5 bloques a una altura fija
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
    def random_number_list(self, start, end, length):
        randomlist = []
        while len(randomlist) < length:
            n = random.randint(start, end)
            if n not in randomlist:
                randomlist.append(n)
        return randomlist

    def generate_random_coordinates(self, length):
        random_ints = self.random_number_list(0, 8, length)

        coordinates = []
        for n in random_ints:
            x = pyxel.width + (16*n)
            y = 216 # Altura del suelo
            coordinates.append((x, y))
        return coordinates


    def generate_enemies(self):
        if len(self.enemies) < 4:
            src_enemies = [src.Goomba, src.KoopaTroopa]
            weights = [0.75, 0.25]
            k = 4 - len(self.enemies)
            new_enemies = random.choices(src_enemies, weights, k=k)
            # Crear una lista de coordenadas aleatorias 
            random_coordinates = self.generate_random_coordinates(len(new_enemies))
            
            # Asignar a cada objeto unas coordenadas y crear una instancia
            for enemy_class, coordinates in zip(new_enemies, random_coordinates):
                new_enemy = enemy_class(*coordinates)
                self.enemies.append(new_enemy)

    def latest_floor(self):
        # Devuelve el suelo con la coordenada x mayor
        return max(self.floors, key=lambda obj: obj.x)

    def create_floors(self):
        # Crear 144 suelos: (-pyxel.width, 2*pyxel.width)
        floors = []
        for i in range(-16, 32):
            for j in range(3):
                floor = src.Floor(16*i, 216+16*j)
                floors.append(floor)
        return floors

    def is_closest_object_to_mario(self, item):
        all_objects = self.pipes + self.blocks_row + self.mistery_objects
        return min(all_objects, key=lambda obj: abs(obj.x-self.mario.x)).x == item.x

    def is_closest_block(self, block):
        return min(self.blocks_row, key=lambda obj: abs(obj.x-self.mario.x)) == block

    def update(self):
        self.timer.update()

        if self.timer.t < 0:
            pyxel.quit()

        if not self.mario.is_alive:
            self.games -= 1
            self.__reset()
        self.mario.update()
        
        if self.games == 0:
            pyxel.quit()

        # Actualizar número de pixeles recorridos por Mario
        if self.mario.vx > 0:
            self.distance_done += self.mario.vx

        # Generar fin de la partida
        if self.distance_done > 5000 and self.timer.t > 100:
            self.end = True
        
        # Actualizar enemigos
        for enemy in self.enemies:
            # Desactivar enemigos si se encuentran fuera del mapa
            enemy.update(self.mario)
        # Regenerar enemigos una vez inactivos
        dead_enemies = [enemy for enemy in self.enemies if not enemy.is_alive]
        self.score += 10 * len(dead_enemies)
        self.enemies = [enemy for enemy in self.enemies if enemy.x > -64 and enemy.is_alive]
        self.generate_enemies()


        # Actualizar tuberias
        for pipe in self.pipes:
            is_closest = self.is_closest_object_to_mario(pipe)
            pipe.update(self.mario, is_closest, self.enemies)

        # Actualizar bloques
        for block in self.blocks_row:
            is_closest_block = self.is_closest_object_to_mario(block)
            block.update(self.mario, is_closest_block)

            # Actualizar objetos de bloques interrogación
            if hasattr(block, 'mistery_object_name') and block.show:
                objs = {'seta':src.Champiñon, 'moneda':src.Moneda}
                mistery_object_name = block.mistery_object_name
                block_object = objs[mistery_object_name](block.x, block.y)
                if not block_object in self.mistery_objects:
                    self.mistery_objects.append(block_object)
                if mistery_object_name == "moneda" and block.show:
                    self.score += 10
                    self.coins += 1
                    block.hidden = True
                    block.show = False

        # Generar una fila de bloques al principio del mapa
        if self.blocks_row[-1].x < -pyxel.width:
            self.blocks_row = self.generate_blocks(256)
            self.pipes = self.create_pipes()
        
        # Actualizar suelos
        latest_floor = self.latest_floor()
        for item in self.floors:
            item.latest_x = latest_floor.x
            item.update(self.mario)

        # Actualizar objetos especiales
        for item in self.mistery_objects:
            print(type(item),)
            is_closest = self.is_closest_object_to_mario(block)
            item.update(self.mario, is_closest)

    def draw_score(self):
        # Pintar puntuación
        s = "MARIO \n{:>5}".format(self.score)
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)

        # Pintar contador monedas
        pyxel.blt(88, 5, 0, 81, 16, 5, 8, 12)
        s = "x {:>2}".format(self.coins)
        pyxel.text(96, 7, s, 1)
        pyxel.text(95, 7, s, 7)

        # Pintar timer
        s = "TIME \n{:>4}".format(self.timer.t)
        pyxel.text(45, 4, s, 1)
        pyxel.text(44, 4, s, 7)

        # Pintar vidas
        pyxel.blt(150, 4, 0, 18, 99, 16, 15, 12)
        v = "x {:>2}".format(self.games)
        pyxel.text(171, 10, v, 1)
        pyxel.text(170, 10, v, 7)

    def generate_ending(self):
        pyxel.cls(12)

        # Pintar mensaje final de partida
        s = "FIN DE LA PARTIDA"
        pyxel.text(121-len(s), 100, s, 1)
        pyxel.text(120-len(s), 100, s, 7)
        self.end_is_showing = True

    def draw(self):
        pyxel.load("assets/mario.pyxres")
        pyxel.cls(12)

        if self.end:
            if self.end_is_showing:
                time.sleep(2)
                pyxel.quit()
            else:
                self.generate_ending()
        else:
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
                    pyxel.blt(x + i * 160 - offset, y, 0, 109, 138, 50, 21, 12)
                    
            # Pintar montañas
            offset = (pyxel.frame_count // 32) % 160
            for x, y in self.mountains:
                pyxel.blt(x + 160 - offset, y, 0, 0, 193, 74, 33, 12)

            # Pintar tuberias
            offset = (pyxel.frame_count // 16) % 160
            for pipe in self.pipes:
                pyxel.blt(pipe.x, pipe.y, 0, *pipe.draw, 32, 47, 12)

            # Pintar enemgos
            for enemy in self.enemies:
                pyxel.blt(enemy.x, enemy.y, 1, *enemy.draw, enemy.width, enemy.height)

            # Pintar Mario
            if not self.mario.jumping:
                # Comprobar si mario ha cogido una seta o no
                if not self.mario.supermario:
                
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

                elif self.mario.supermario:

                    if self.mario.vx > 0:
                        if pyxel.frame_count % 8 <= 2 and self.mario.vx > 1:
                            pyxel.blt(self.mario.x, self.mario.y, 0, 73, 83, 16, 31, 12)
                        elif pyxel.frame_count % 8 <= 4 and self.mario.vx > 1:
                            pyxel.blt(self.mario.x, self.mario.y, 0, 88, 82, 16, 31, 12)
                        elif pyxel.frame_count % 8 <= 6 and self.mario.vx > 1:
                            pyxel.blt(self.mario.x, self.mario.y, 0, 106, 84, 16, 31, 12)
                        else:
                            pyxel.blt(self.mario.x, self.mario.y, 0, 54, 82, 16, 32, 12)
                    elif self.mario.vx < 0:
                        if pyxel.frame_count % 8 <= 4 and self.mario.vx < -1:
                            pyxel.blt(self.mario.x, self.mario.y, 0, 73, 83, -16, 31, 12)
                        else:
                            pyxel.blt(self.mario.x, self.mario.y, 0, 54, 82, -16, 32, 12)
                    else:
                        pyxel.blt(self.mario.x, self.mario.y, 0, 54, 82, 16, 32, 12)

            else:
                if not self.mario.supermario:
                    if self.mario.vx >= 0:
                        pyxel.blt(self.mario.x, self.mario.y, 0, 1, 79, 16, 16, 12)
                    else:
                        pyxel.blt(self.mario.x, self.mario.y, 0, 1, 79, -16, 16, 12)
                elif self.mario.supermario:
                    if self.mario.vx >= 0:
                        pyxel.blt(self.mario.x, self.mario.y, 0, 147, 80, 16, 32, 12)
                    else:
                        pyxel.blt(self.mario.x, self.mario.y, 0, 147, 80, -16, 32, 12)                

            self.draw_score()
        
        

App()
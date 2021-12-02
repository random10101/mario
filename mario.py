import pyxel
import src


class App:
    def __init__(self):
        self.score = None
        self.timer = None

        pyxel.init(256, 256)
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pass

App()
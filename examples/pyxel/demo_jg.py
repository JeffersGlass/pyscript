import pyxel

class App:
    def __init__(self):
        pyxel.load('assets/sprite.png')
        pyxel.init(128,128)
        pyxel.run(self.update, self.draw)

    def update(self):
        ...

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 0, 8, 8, 9)
        

App()

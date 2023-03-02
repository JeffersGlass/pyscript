import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="PyScript Fun Demo")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        for index, y in enumerate(range(10, 100, 8)):
            pyxel.text(40, y, "Hello, PyScript Fun!!", int((pyxel.frame_count + index )/ 8) % 15 + 1)

App()
import pyxel
import js
from pyscript import window, document

js.document = document

class Screen():
    def __init__(self, width, height):
        self.width = window.screen.width
        self.height = window.screen.height

js.screen = Screen(400, 400)

class App():
    def __init__(self):
        pyxel.init(256, 256)

    def update(self):
        pass

    def draw(self):
        pass

print("LOADING APP")

App()
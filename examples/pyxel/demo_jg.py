import pyxel
import js
from dataclasses import dataclass

class Frame():
    def __init__(self, u, v, w, h):
        self.u = u
        self.v = v
        self.w = w
        self.h = h
    
    @classmethod
    def fromFrame(cls, frame, **kwargs):
        return cls(frame.u, frame.v, frame.w, frame.h)

class Person():
    def __init__(self, x = 40, y = 100, speed = 3):
        self.x = x
        self.dx = 0
        self.y = y
        self.dy = 0
        self.speed = speed

        self.width = 16
        self.height = 24


        self.directionIndex = 1
        self.Image = pyxel.image(0)
        self.frameIndex = 0
        self.frames = {
            "standing":
            [
                Frame(u=0, v=32, w=16, h=16),
            ],
            "walking":
            [
                Frame(u=0, v=48, w=16, h=24),
                Frame(u=16, v=48, w=16, h=24),
                Frame(u=32, v=48, w=16, h=24),
                Frame(u=48, v=48, w=16, h=24),
            ]
        }
        self.walking = False
        self.walkChange = -1

    def update(self):
        self.dx = 0
        self.dy = 0
        nowWalking = False
        if pyxel.btn(pyxel.KEY_SHIFT):
            currentSpeed = self.speed * 2
        else:
            currentSpeed = self.speed
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.dx = -currentSpeed
            self.directionIndex = 0
            nowWalking = True
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.dx = currentSpeed
            self.directionIndex = 1
            nowWalking = True
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.dy = -currentSpeed
            nowWalking = True
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.dy = currentSpeed
            nowWalking = True

        if nowWalking != self.walking:
            self.walkChange = pyxel.frame_count
        self.walking = nowWalking
        
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        if not self.walking:
            currentFrame = Frame.fromFrame(self.frames["standing"][0])
        else:
            ellapsed = int((pyxel.frame_count - self.walkChange) / 2) % 4
            currentFrame = Frame.fromFrame(self.frames["walking"][ellapsed])
        if self.directionIndex == 0:
            currentFrame.w *= -1
        pyxel.blt(
            x = self.x,
            y = self.y - currentFrame.h,
            img = self.Image,
            u = currentFrame.u,
            v = currentFrame.v,
            w = currentFrame.w,
            h = currentFrame.h, 
            colkey = 0)   
        

@dataclass
class Camera():
    x: int
    y: int

    def update(self, person: Person, buffer = 30):
        if person.x - buffer < self.x:
            self.x = person.x - buffer
        elif person.x + person.width > self.x + pyxel.width - buffer:
            self.x = person.x + person.width - pyxel.width + buffer

        if person.y - person.height - buffer < self.y:
            self.y = person.y - person.height - buffer
        elif person.y > self.y + pyxel.height - buffer:
            self.y = person.y - pyxel.height + buffer




class App:
    def __init__(self):
        pyxel.init(256, 256)
        pyxel.image(0).load(0, 0, 'assets/spritesheet.png')

        self.jeff = Person()
        self.camera = Camera(0, 0)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.jeff.update()
        self.camera.update(self.jeff)
        pyxel.camera(self.camera.x, self.camera.y)

    def draw(self):
        pyxel.cls(13)    
        nextY = 0 
        for obj in globals():
            doc = globals()[obj].__doc__
            if doc is None: doc = ''
            doc = doc.strip()
            numLines = len(doc.split("\n"))

            pyxel.rect(-5, nextY - 4, 5 * 80, numLines * 8 + 8, 7)
            pyxel.text(0, nextY, obj, 1)
            pyxel.text(80, nextY, doc, 1)
            nextY += 8 * numLines + 12
    
        self.jeff.draw()            

App()

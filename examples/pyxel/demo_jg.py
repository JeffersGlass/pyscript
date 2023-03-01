import pyxel
import js
from dataclasses import dataclass
import os
import math

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
        self.running = False
        self.walkChange = -1

    def update(self):
        self.dx = 0
        self.dy = 0
        nowWalking = False
        if pyxel.btn(pyxel.KEY_SHIFT):
            self.running = True
            currentSpeed = self.speed * 2
        else:
            self.running = False
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
        if self.running:
            pyxel.circ(
                x = self.x + self.width/2,
                y = self.y - 8,
                r = 10,
                col = 12
            )
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

class FileTree():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.color = 1
        
    def draw(self):
        line = 0
        for root, dirs, files in os.walk("."):
            path = root.split(os.sep)
            pyxel.text(self.x, line * 10, str((len(path) - 1) * '---' + os.path.basename(root)), self.color)
            line += 1
            #print((len(path) - 1) * '---', os.path.basename(root))
            for file in files:
                pyxel.text(self.x, line * 10, str((len(path) * '---' + file)), self.color)
                #print(len(path) * '---', file)
                line +=1

@dataclass
class JSInfo():
    name: str
    attributes: str



class App:
    def __init__(self):
        pyxel.init(256, 256)
        pyxel.image(0).load(0, 0, 'assets/spritesheet.png')

        self.jeff = Person()
        self.camera = Camera(0, 0)
        self.files = FileTree()

        jsNames = dir(js)
        self.jsDocs = [
            JSInfo(
                name = name,
                attributes = ', '.join(attrib for attrib in dir(getattr(js, name)) if attrib[:2] != '__')
            ) for name in jsNames]        
        self.maxDoc = max(len(info.attributes) for info in self.jsDocs)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.jeff.update()
        self.camera.update(self.jeff)
        pyxel.camera(self.camera.x, self.camera.y)

    def draw(self):
        pyxel.cls(13)    
        #sself.drawGlobals()
        self.drawJS()
        
        #pyxel.cls(7)    
        #self.files.draw()

        self.jeff.draw()    

    def drawGlobals(self):
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

    def drawJS(self):
        lineHeight = 20
        firstDraw = max(int(self.camera.y / lineHeight), 0)
        #pyxel.text(self.camera.x, self.camera.y, str(firstDraw), 1)
        lastDraw = min(int((self.camera.y + pyxel.height + lineHeight) / lineHeight), len(self.jsDocs))
        for index, js_item in enumerate(self.jsDocs[firstDraw:lastDraw]):
            name_len = len(js_item.name)
            pyxel.rect(5 * name_len + 10, ((index + firstDraw) * lineHeight) - 4, self.maxDoc * 5, 16, 15)
            pyxel.text(5 * name_len + 15, ((index + firstDraw) * lineHeight), js_item.attributes, 1)
            pyxel.rect(max(self.camera.x + 5, -5), ((index + firstDraw) * lineHeight) - 4, 4 * len(js_item.name) + 10, 16, 7)
            pyxel.text(max(self.camera.x + 10, 0), ((index + firstDraw) * lineHeight), js_item.name, 2)
            pyxel.rect(self.camera.x, self.camera.y, 5, pyxel.height, 13)

App()

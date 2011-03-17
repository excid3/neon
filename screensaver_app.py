import pyglet
from neon import NeonApp

class ScreensaverApp(NeonApp):

    def on_init(self):
        # Initialize a text widget to move around
        self.text = pyglet.text.Label("Screensaver", color=(255,0,0,255), anchor_x="center", anchor_y="center")
        self.text.x = self.x
        self.text.y = self.y +self.h
        self.widgets.append(self.text)
        self.direction = 0
        
    def on_draw(self):
        
        move = 1

        if self.direction == 0: #up/right
            self.text.x += move
            self.text.y += move
            
            if self.text.x >= self.x+self.w:
                self.direction = 3
            
            if self.text.y >= self.y+self.h:
                self.direction = 1

        elif self.direction == 1: #down/right
            self.text.x += move
            self.text.y -= move
            
            if self.text.x >= self.x+self.w:
                self.direction = 2
            
            if self.text.y < self.y:
                self.direction = 0
            
        elif self.direction == 2: #down/left
            self.text.x -= move
            self.text.y -= move

            if self.text.x < self.x:
                self.direction = 1
            
            if self.text.y < self.y:
                self.direction = 3
            
        elif self.direction == 3: #up/left
            self.text.x -= move
            self.text.y += move
            
            if self.text.x < self.x:
                self.direction = 0
            
            if self.text.y >= self.y+self.h:
                self.direction = 2
        
        self.text.draw()


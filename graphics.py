#!/usr/bin/env python

import platform
import pyglet
import random

import node

SCREEN_X, SCREEN_Y = 0, 1024

window = pyglet.window.Window(fullscreen=True)
# Used for configuring the location of the screen rendering
pyglet.gl.glTranslatef(SCREEN_X, -SCREEN_Y, 0)


class NeonApp:
    def __init__(self, title="Untitled Window", size=(800, 600), location=(0,0)):
        self.title = pyglet.text.Label(title, font_name="Arial", font_size=16, anchor_x="left", anchor_y="top")
        self.w, self.h = size
        self.set_location(*location)
        self.dt = 0
   
        running_apps.append(self)
        
        self.text = pyglet.text.Label("Screensaver", color=(255,0,0,255), anchor_x="center", anchor_y="center")
        self.text.x = self.x
        self.text.y = self.y +self.h
        self.direction = 0
        
    def update(self, dt):
        self.dt = dt
        
    def draw_updates(self):
        
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

    def set_location(self, x, y):
        self.x = x
        self.y = y

        
    def _draw(self):
        # Draw the window title
        draw_polygon((
            self.x, self.y+self.h,
            self.x, self.y+self.h+24,
            self.x+self.w, self.y+self.h+24,
            self.x+self.w, self.y+self.h),
            colors=(0.1, 0.1, 0.1)
        )
        self.title.x = self.x+4
        self.title.y = self.y+self.h+24
        self.title.draw()
        
        # Draw the window itself
        draw_polygon((
            self.x, self.y,
            self.x, self.y+self.h,
            self.x+self.w, self.y+self.h,
            self.x+self.w, self.y)
        )

        self.draw_updates()
        

def draw_polygon(dimensions=(), format="v2i", amount=4, colors=(1.0,1.0,1.0)):
    pyglet.gl.glColor3f(*colors)
    pyglet.graphics.draw(amount, pyglet.gl.GL_POLYGON,
        (format, dimensions)
    )


def update(dt):
    for app in running_apps:
        app.update(dt)

@window.event
def on_draw():
    window.clear()
    
    # Draw backgrounds
    for i in [0, 1280]:
        background.x = SCREEN_X + i
        background.y = SCREEN_Y
        background.draw()

    # Draw applications    
    for app in running_apps:
        app._draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    global focused_app
    for app in reversed(running_apps):
        if app.x <= x <= app.x+app.w and \
           app.y+app.h <= y <= app.y+app.h+24:
           focused_app = app

@window.event
def on_mouse_release(x, y, button, modifiers):
    global focused_app
    focused_app = None

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global focused_app
    if focused_app:
        focused_app.set_location(focused_app.x+dx, focused_app.y+dy)



running_apps = []
focused_app = None


pyglet.resource.path = ["/home/user/Wallpaper/"]
pyglet.resource.reindex()
background = pyglet.sprite.Sprite(img=pyglet.resource.image("%s.png" % platform.node()))
pyglet.clock.schedule_interval(update, 1/120.0)

    
NeonApp("Window Title")
NeonApp("Second Window Title", (600, 200), (1600, 400))
node.start_server(pyglet.app.run)

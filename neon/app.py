import pyglet

import neon


def draw_polygon(dimensions=(), format="v2i", amount=4, colors=(1.0,1.0,1.0)):
    pyglet.gl.glColor3f(*colors)
    pyglet.graphics.draw(amount, pyglet.gl.GL_POLYGON,
        (format, dimensions)
    )


class NeonApp:
    def __init__(self, parent, title="Untitled Window", size=(800, 600), location=(0,0)):
        self.parent = parent
        self.title = pyglet.text.Label(title, font_name="Arial", font_size=16, anchor_x="left", anchor_y="top")
        self.w, self.h = size
        self.set_location(*location)
        self.dt = 0
   
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

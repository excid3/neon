import platform
import pyglet

import neon

class NeonApp:
    def __init__(self, parent, title="Untitled Window", size=(800, 600), location=(0,0)):
        self.parent = parent
        self.title = pyglet.text.Label(title, font_name="Arial", font_size=16, anchor_x="left", anchor_y="top")
        self.title_text = title
        self.w, self.h = size
        self.set_location(*location)
        self.dt = 0
        self.widgets = []
        
        self.network_draw('%s: new: {"size":%s, "location":%s }' % \
                          (self.title_text,
                           str(size),
                           str(location))
                         )
        
        if hasattr(self, "on_init"):
            self.on_init()

    def update(self, dt):
        self.dt = dt

    def set_location(self, x, y):
        self.x = x
        self.y = y

        
    def _draw(self):
        # Draw the window title
        self.draw_polygon((
            self.x, self.y+self.h,
            self.x, self.y+self.h+24,
            self.x+self.w, self.y+self.h+24,
            self.x+self.w, self.y+self.h),
            color=(0.1, 0.1, 0.1)
        )
        self.title.x = self.x+4
        self.title.y = self.y+self.h+24
        self.title.draw()
        
        # Draw the window itself
        self.draw_polygon((
            self.x, self.y,
            self.x, self.y+self.h,
            self.x+self.w, self.y+self.h,
            self.x+self.w, self.y)
        )

    def draw_polygon(self, points, format="v2i", amount=4, color=(1.0,1.0,1.0)):
        self.draw_object(pyglet.gl.GL_POLYGON, points, format, amount, color)

    def draw_line(self, points, format="v2i", amount=2, color=(1.0, 1.0, 1.0)):
        self.draw_object(pyglet.gl.GL_LINES, points, format, amount, color)
        
    def draw_object(self, shape, points, format, amount, color):
        pyglet.gl.glColor3f(*color)
        pyglet.graphics.draw(amount, shape,
            (format, points)
        )
        #self.network_draw('%s: draw_object: {"shape":%s, "points":%s, "format":%s, "amount":%i, "color":%s}' % \
        #                  (self.title_text,
        #                   shape,
        #                   str(points),
        #                   '"%s"' % format,
        #                   amount,
        #                   str(color))
        #                 )
        
    def network_draw(self, message):
        for host in self.parent.nodes.keys():
            if host != platform.node()+".local":
                neon.network.send_network_data(message, (host, 9999))
        

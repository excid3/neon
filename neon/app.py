import platform
import pyglet

import neon


class NeonApp:
    """
    The Neon App is a base class that provides functionality for other apps
    to inherit and override
    """

    def __init__(self, parent, title="Untitled Window", size=(800, 600), location=(0,0)):
        """Initialize the window"""

        #self.parent = parent

        #FIXME: Creating a pyglet lable here crashes for some reason when a network
        # node creates a fake app...
        self.title = None #pyglet.text.Label(title, font_name="Arial", font_size=16, anchor_x="left", anchor_y="top")
        self.title_text = title
        self.w, self.h = size
        self.set_location(*location)
        self.dt = 0
        self.widgets = []

        if hasattr(self, "on_init"):
            self.on_init()

    def update(self, dt):
        self.dt = dt

    def set_location(self, x, y):
        """Set the window location"""
        self.x = x
        self.y = y

    def _draw(self):
        """Internal draw command"""

        # Draw the window title
        self.draw_polygon((
            self.x, self.y+self.h,
            self.x, self.y+self.h+24,
            self.x+self.w, self.y+self.h+24,
            self.x+self.w, self.y+self.h),
            color=(0.1, 0.1, 0.1),
            broadcast=False # This is drawn remotely with the fake app
        )
        #self.title.x = self.x+4
        #self.title.y = self.y+self.h+24
        #self.title.draw()

        # Draw the window itself
        self.draw_polygon((
            self.x, self.y,
            self.x, self.y+self.h,
            self.x+self.w, self.y+self.h,
            self.x+self.w, self.y),
            broadcast=False# This is drawn remotely with the fake app
        )

    def draw_polygon(self, points, format="v2i", amount=4, color=(1.0,1.0,1.0), broadcast=True):
        """Helper command for drawing that will broadcast to the other machines
        in the cluster by default. This keeps every machine's graphics in
        sync"""
        self.draw_object(pyglet.gl.GL_POLYGON, points, format, amount, color, broadcast)

    def draw_line(self, points, format="v2i", amount=2, color=(1.0, 1.0, 1.0), broadcast=True):
        """Helper command for drawing that will broadcast to the other machines
        in the cluster by default. This keeps every machine's graphics in
        sync"""
        self.draw_object(pyglet.gl.GL_LINES, points, format, amount, color, broadcast)

    def draw_object(self, shape, points, format, amount, color, broadcast=True):
        """Helper command for drawing that will broadcast to the other machines
        in the cluster by default. This keeps every machine's graphics in
        sync"""
        pyglet.gl.glColor3f(*color)
        pyglet.graphics.draw(amount, shape,
            (format, points)
        )
        if broadcast and self.__class__ != NeonApp: #TODO: Make these FakeApp for cloned apps
            neon.NODE.network_cmd('%s: draw_object: {"shape":%s, "points":%s, "format":"%s", "amount":%i, "color":%s}' % \
                          (self.title_text,
                           shape,
                           str(points),
                           format,
                           amount,
                           str(color))
                         )

    def send_app_config(self):
        """Used if a remote machine doesn't have a local copy of this
        application"""
        if self.__class__ == neon.app.NeonApp: #TODO: Make these FakeApp for cloned apps
            return

        print "sending config"
        neon.NODE.network_cmd('%s: __init__: {"title":"%s", "size":%s, "location":%s}' % \
                          (self.title_text,
                           self.title_text,
                           str((self.w, self.h)),
                           str((self.x, self.y)))
                         )

#!/usr/bin/env python

import platform
import pyglet
import threading

import neon
from app import NeonApp
from network import ThreadedUDPServer, UDPHandler


class RenderNode(UDPHandler):
    def __init__(self, location, size):
        self.x, self.y = location
        self.w, self.h = size
        
        self.running_apps = {}
        self.focused_app = None

        self.window = pyglet.window.Window(fullscreen=True)

        # Used for configuring the location of the screen rendering
        pyglet.gl.glTranslatef(self.x, -self.y, 0)
        
        pyglet.clock.schedule_interval(self.update, 1/120.0)
        
        self.set_callbacks()

    def update(self, dt):
        for app in self.running_apps.values():
            app.update(dt)

    def new_app(self, title="Untitled Window", size=(800, 600), location=(0,0)):
        self.running_apps[title] = NeonApp(self, title, size, location)
    
    def start_server(self):
        
        HOST, PORT = "", 9999
        server = ThreadedUDPServer((HOST, PORT), self) # Issue here, we can't access the queue variable
        server_thread = threading.Thread(target=server.serve_forever)
        
        server_thread.setDaemon(True)
        server_thread.start()
        
        try:
            pyglet.app.run()
        finally:
            print "\nShutting down"
            server.shutdown()
        
        
    def set_callbacks(self):
        pyglet.resource.path = ["/home/user/Wallpaper/"]
        pyglet.resource.reindex()
        self.background = pyglet.sprite.Sprite(img=pyglet.resource.image("%s.png" % platform.node()))

        self.window.set_handlers("on_draw", self.on_draw,
                                 "on_mouse_press", self.on_mouse_press,
                                 "on_mouse_release", self.on_mouse_release,
                                 "on_mouse_drag", self.on_mouse_drag)
        

    # Initialize window callbacks
    def on_draw(self):
        self.window.clear()
        
        # Draw backgrounds
        for i in [0, 1280]:
            self.background.x = self.x + i
            self.background.y = self.y
            self.background.draw()

        # Draw applications    
        for app in self.running_apps.values():
            app._draw()

        # Network shapes
        print self.queue
        for item in self.queue:
            # network items
            title, shape, args = item.split(":")
            
            print self.running_apps[title]

        self.queue = []



    def on_mouse_press(self, x, y, button, modifiers):

        for app in reversed(self.running_apps.values()):
            if app.x <= x <= app.x+app.w and \
               app.y+app.h <= y <= app.y+app.h+24:
               self.focused_app = app


    def on_mouse_release(self, x, y, button, modifiers):
        self.focused_app = None


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):

        if self.focused_app:
            self.focused_app.set_location(self.focused_app.x+dx, self.focused_app.y+dy)

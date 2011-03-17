#!/usr/bin/env python

import platform
import pyglet
import threading

import neon
import network
from app import NeonApp

HOST, PORT = "", 9999


class RenderNode:
    def __init__(self, nodes):
        self.nodes = nodes
        
        name = platform.node() + ".local"
    
        self.x, self.y = nodes[name]["location"]
        self.w, self.h = nodes[name]["size"]
        
        self.running_apps = []
        self.focused_app = None


        # Used for configuring the location of the screen rendering
        self.window = pyglet.window.Window(fullscreen=True)
        pyglet.gl.glTranslatef(self.x, -self.y, 0)
        
        pyglet.clock.schedule_interval(self.update, 1/120.0)
        self.set_callbacks()


    def update(self, dt):
        for name, app in self.running_apps:
            app.update(dt)

    def new_app(self, title="Untitled Window", size=(800, 600), location=(0,0), app_type=NeonApp):
        self.running_apps.append((title, app_type(self, title, size, location)))
    
    
    def start_server(self):
        
        server = network.ThreadedUDPServer((HOST, PORT), network.UDPHandler) # Issue here, we can't access the queue variable
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
        for name, app in self.running_apps:
            app._draw() # Draw the window

            if hasattr(app, "on_draw"): 
                app.on_draw() # Draw custom content

            # Network shapes
            if name in network.queue:
                for command, args in network.queue[name]:

                    # Can we run this command on the application?
                    if hasattr(app, command):

                        if 'points' in args:
                            pts = []
                            for x,y in zip(args["points"][::2], args["points"][1::2]):
                                pts.append(x+app.x)
                                pts.append(y+app.y)
                            args["points"] = pts
                        
                        getattr(app, command)(**args)
    
        network.queue.clear()
            

    def on_mouse_press(self, x, y, button, modifiers):

        for name, app in reversed(self.running_apps):

            # Find the app that is currently being focused
            if app.x <= x <= app.x+app.w and \
                app.y+app.h <= y <= app.y+app.h+24:
                self.focused_app = app

                # Move item to end of list, this way it's draw on top
                self.running_apps.remove((name, app))
                self.running_apps.append((name, app))
                
               
    def on_mouse_release(self, x, y, button, modifiers):
        self.focused_app = None


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):

        # If an app is focused, let's drag it and the widgets inside of it
        if self.focused_app:
        
            self.focused_app.set_location(self.focused_app.x + dx, self.focused_app.y + dy)
            
            for widget in self.focused_app.widgets:
                widget.x = widget.x + dx
                widget.y = widget.y + dy

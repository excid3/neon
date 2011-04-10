#!/usr/bin/env python

"""
Neon Graphics Library

"""

import platform
import pyglet
import threading

import neon
import network
from app import NeonApp


HOST, PORT = "", 9999
NODE = None


# This is the core Neon class. It must be instanciated on each node of the
# cluster. It's intention is to keep track of the window location, size, and
# events.

class RenderNode:
    def __init__(self, nodes):
        self.nodes = nodes

        # This won't apply to all networks, but for ubuntu, the .local is
        # required in order to do local network traffic
        name = platform.node() + ".local"

        # Set the location and size of our node
        self.x, self.y = nodes[name]["location"]
        self.w, self.h = nodes[name]["size"]

        # Initialize some variables for later
        self.running_apps = []
        self.focused_app = None


        # Configure the location of the screen rendering with OpenGL. We just
        # simply translate the location so that each node only displays the
        # graphics it is supposed to.
        self.window = pyglet.window.Window(fullscreen=True)
        pyglet.gl.glTranslatef(-self.x, -self.y, 0)

        # Set the update interval and callbacks
        pyglet.clock.schedule_interval(self.update, 1/120.0)
        self.set_callbacks()

        # This is used to keep track of the running RenderNode on each machine
        # so that we can accept and send out network commands through it alone.
        global NODE
        NODE = self


    def update(self, dt):
        """Placeholder function for in the future calling the update function
        so that apps can use this to update their logic"""
        #for name, app in self.running_apps:
        #    app.update(dt)
        pass

    def new_app(self, title="Untitled Window", size=(800, 600), location=(0,0), app_type=NeonApp):
        """Instanciate a new app for this RenderNode"""
        print "Adding %s" % title
        self.running_apps.append((title, app_type(self, title, size, location)))

    def start_server(self):
        """The RenderNode main loop. Starts the UDP server thread and pyglet"""
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
        """Sets some handlers, loads the wallpaper, etc."""
        pyglet.resource.path = ["/home/user/Wallpaper/"]
        pyglet.resource.reindex()
        self.background = pyglet.sprite.Sprite(img=pyglet.resource.image("%s.png" % platform.node()))

        self.window.set_handlers("on_draw", self.on_draw,
                                 "on_mouse_press", self.on_mouse_press,
                                 "on_mouse_release", self.on_mouse_release,
                                 "on_mouse_drag", self.on_mouse_drag)


    def on_draw(self):
        """The main draw look for pyglet"""

        # Cache a copy of network objects so we don't receive anything while we
        # are executing this
        network_objects = network.queue.copy()
        network.queue.clear()

        # Clear the window
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
            if name in network_objects:
                for command, args in network_objects[name]:

                    # Can we run this command on the application?
                    if command != '__init__' and hasattr(app, command):
                        getattr(app, command)(**args)
                    else:
                        print "Unknown command for %s: %s" % (name, command)

                # Delete the network commands we've used
                del network_objects[name]

        # If there is anything left in the queue, we must not have the app running here
        for key, value in network_objects.items():
            created = False

            # Create a new window based upon that info
            for command, args in value:
                if command == '__init__':
                    print "Creating local copy of %s" % args["title"]
                    self.new_app(**args)
                    created = True
                    break

            if not created:
                print "Unknown app: %s, requesting config" % key
                self.network_cmd("%s: send_app_config: {}" % key)

    def network_cmd(self, message):
        """Sends a command to all the hosts in the cluster"""
        for host in self.nodes.keys():
            if host != platform.node()+".local":
                neon.network.send_network_data(message, (host, 9999))

    def on_mouse_press(self, x, y, button, modifiers):
        """Called every time a mouse button is pressed"""
        for name, app in reversed(self.running_apps):

            # Find the app that is currently being focused
            if app.x <= x + self.x <= app.x+app.w and \
                app.y+app.h <= y + self.y <= app.y+app.h+24:
                self.focused_app = [name, app]

                # Move item to end of list, this way it's draw on top
                self.running_apps.remove((name, app))
                self.running_apps.append((name, app))

    def on_mouse_release(self, x, y, button, modifiers):
        """Called every time a mouse button is released. This is used for the
        end of dragging to unfocus the app that was selected while dragging."""
        self.focused_app = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Called every time the mouse is dragged"""

        # If an app is focused, let's drag it and the widgets inside of it
        if self.focused_app:
            new_x, new_y = self.focused_app[1].x + dx, self.focused_app[1].y + dy
            self.focused_app[1].set_location(new_x, new_y)
            self.network_cmd('%s: set_location: {"x":%i, "y":%i}' % (self.focused_app[0], new_x, new_y))

            for widget in self.focused_app[1].widgets:
                widget.x = widget.x + dx
                widget.y = widget.y + dy

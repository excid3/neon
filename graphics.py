#!/usr/bin/env python
#
# This is an example script for configuring and running an app across a cluster
#
# A RenderNode is a machine on the network that will render graphics. Apps can
# be applied to a render node, where Neon will instanciate and execute the app.
#
# Here we have cluster-3 launch the application across the network after setup
# of the RenderNodes. When we are ready, we call start_server and Neon will
# launch the graphics and UPD threads.

import platform

from neon import RenderNode
from apps import GraphApp, ScreensaverApp

nodes = { 
          "cluster-1.local": { "location": (0, 2048),    "size": (2560, 1024) },
          "cluster-2.local": { "location": (2560, 2048), "size": (2560, 1024) },
          "cluster-3.local": { "location": (0, 1024),    "size": (2560, 1024) },
          "cluster-4.local": { "location": (2560, 1024), "size": (2560, 1024) },
          "cluster-5.local": { "location": (0, 0),    "size": (2560, 1024) },
          "cluster-6.local": { "location": (2560, 0), "size": (2560, 1024) },
        }

r = RenderNode(nodes)

if platform.node() == "cluster-3":
    r.new_app("Network Graph", (3500,1700), (100, 1050), app_type=GraphApp)
    #r.new_app("Screensaver Example", (600, 1200), (1600, 400), app_type=ScreensaverApp)

r.start_server()

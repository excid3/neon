#!/usr/bin/env python

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

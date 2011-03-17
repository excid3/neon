#!/usr/bin/env python

from neon import RenderNode

from graph_app import GraphApp

nodes = { 
          "cluster-1.local": { "location": (0, 0),    "size": (2560, 1025) },
          #"cluster-2.local": { "location": (2560, 2048), "size": (2560, 1025) },
          "cluster-3.local": { "location": (0, 0),    "size": (2560, 1025) },
          #"cluster-4.local": { "location": (2560, 1024), "size": (2560, 1025) },
          "cluster-5.local": { "location": (0, 0),    "size": (2560, 1025) },
          #"cluster-6.local": { "location": (2560, 0), "size": (2560, 1025) },
        }

r = RenderNode(nodes)

import platform
if platform.node() == "cluster-3":
    r.new_app("Window Title", app_type=GraphApp)
    r.new_app("Second Window Title", (600, 200), (1600, 400))

r.start_server()

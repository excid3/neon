#!/usr/bin/env python

from neon import RenderNode

location = (0, 0) # x, y
size = (2560, 1024) # width, height

r = RenderNode(location, size)

r.new_app("Window Title")
r.new_app("Second Window Title", (600, 200), (1600, 400))

r.start_server()

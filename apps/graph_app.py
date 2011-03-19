import random
from neon import NeonApp

class GraphApp(NeonApp):

    def on_init(self):
        self.graphs = [400, 1000, 600, 900, 800, 1200]
        self.colors = [(0.1, 0.8, 0.1),
                       (0.8, 0.1, 0.1),
                       (0.8, 0.8, 0.1),
                       (0.8, 0.8, 0.8),
                       (0.1, 0.8, 0.8),
                       (0.1, 0.1, 0.8)]

    def on_draw(self):
        # Add a little change to each
        for i in range(0, len(self.graphs)):
            v = self.graphs[i] + random.randint(-10, 10)
            if v < 0: v = 0
            elif v > self.h: v = self.h
            self.graphs[i] = v

        
        # GRAPH!
        for i, v in enumerate(self.graphs):
        
            self.draw_polygon((
                self.x + 525*i + 200, self.y,
                self.x + 525*i + 200, self.y + v,
                self.x + 525*i + 600, self.y + v,
                self.x + 525*i + 600, self.y),
                color=self.colors[i]
            )


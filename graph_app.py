from neon import NeonApp

class GraphApp(NeonApp):
    def on_init(self):
        self.nodes = "OHAI"

#    def on_draw(self):
#        print self.title_text

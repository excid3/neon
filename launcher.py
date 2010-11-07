# Neon Launcher

import ConfigParser
import logging
import subprocess
import sys


PROPERTIES = ["height", "width"]


class Launcher:
    """Neon application launcher"""
    
    def __init__(self, app, config)
         self.app = app
         self.nodes = {}
         self.config = self.parse_config(config)

    def parse_config(self, config):
        """Parses the configuration file"""

        #logging.info("Loading config: %s" % config)
        parser = ConfigParser.ConfigParser()
        parser.read(config)
        count = parser.get("Nodes", "node_count")

        nodes = {}
        errors = False
        for n in range(1, int(count) + 1):
             
            try:
                name = parser.get("Nodes", "node%i" % n)
                nodes[name] = {}

                for prop in PROPERTIES:
                    nodes[name][prop] = parser.get(name, prop)

            except ConfigParser.NoSectionError, e:
                print "Configuration Error: %s" % e
                errors = True

        if errors:
            sys.exit(1)

        print "Config loaded successfully"
        for node, props in nodes.items():
            print node, props

        self.nodes = nodes


    def start(self):
        for node, props in self.nodes.items():
            print subprocess.call(["ssh", "-x", node, "ls"])


def main():
    app, config = get_args()
    nlauncher = Launcher(app, config)
    nlauncher.start()


def get_args():
    """Verifies and returns arguments"""

    if len(sys.argv) != 3:
        print "USAGE: launcher.py app config\n" \
              "    app - path to the application\n" \
              "    config - path to config file"
        sys.exit(1)

    return sys.argv[1], sys.argv[2]


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()

from grader import Grader

import json
import sys
import os

class Main:
    def __init__(self, settings_file, timeouts_file=None) -> None:
        with open(settings_file, 'r') as f:
            self.settings = json.load(f)
        if timeouts_file:
            with open(timeouts_file, 'r') as f:
                self.timeouts = json.load(f)
        self.grader = Grader(self.settings, self.timeouts)

    def ready(self):
        self.grader.init_submissions()

if __name__ == '__main__':
    config_dir = sys.argv[1]
    main = Main(os.path.join(config_dir, 'settings.json'), os.path.join(config_dir, 'timeouts.json'))
    main.ready()
    
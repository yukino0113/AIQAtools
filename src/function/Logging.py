import os
from datetime import datetime

class Logging:

    def __init__(self):
        self.path = os.path.join(os.getcwd(), 'log.txt')

    def clear_log(self):
        open(self.path, 'w').close()

    def log(self, function, message):
        time = datetime.now().strftime("%H:%M:%S")
        with open(self.path, 'a') as f:
            f.write(f'[{time} {function}] {message}\n')

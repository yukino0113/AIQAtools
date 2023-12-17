import os
from datetime import datetime


class Logging:

    def __init__(self):
        self.log_path = os.path.join(os.getcwd(), 'log.txt')

    def clear_log(self):
        open(self.log_path, 'w').close()

    def log(self, function, message):
        time = datetime.now().strftime("%H:%M:%S")
        with open(self.log_path, 'a') as f:
            f.write(f'[{time} {function}] {message}\n')

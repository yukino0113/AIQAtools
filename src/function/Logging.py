from datetime import datetime


class Logging:

    @staticmethod
    def get_time():
        return datetime.now().strftime("%H:%M:%S")

    def clear_log(self):
        open(self.log_path, 'w').close()

    def log(self, function, message):
        time = datetime.now().strftime("%H:%M:%S")
        with open(self.log_path, 'a') as f:
            f.write(f'[{time} {function}] {message}\n')

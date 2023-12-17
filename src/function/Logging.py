from datetime import datetime


class Logging:

    @staticmethod
    def get_time():
        return datetime.now().strftime("%H:%M:%S")

    def log(self, function, message, log_path):
        with open(log_path, 'a+', encoding='utf-8') as f:
            f.write(f'[{self.get_time()}] [{function}] {message}\n')

    def log_end(self, log_path):
        with open(log_path, 'a+', encoding='utf-8') as f:
            f.write(f'[{self.get_time()}] [Test End] [準備輸出摘要]\n')
            for _ in range(3):
                f.write(f'[{self.get_time()}] [] \n')


    def log_summary(self, issue, quantity, log_path):
        with open(log_path, 'a+', encoding='utf-8') as f:
            f.write(f'[{self.get_time()}] [Summary] {issue}: {quantity}\n')


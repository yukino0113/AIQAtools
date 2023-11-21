import os

from icecream import ic


class SaveFile:

    def __init__(self, path, style):
        self.resultPath = os.path.join(path, 'result')
        self.style = style
        self.init_create_result_folder()
        self.init_create_style_folder(style)
        self.create_from_template()
        self.issueTable = {}

    def init_create_result_folder(self):
        if not os.path.exists(self.resultPath):
            os.mkdir(self.resultPath)

    def init_create_style_folder(self, style):
        if not os.path.exists(os.path.join(self.resultPath, style)):
            os.mkdir(os.path.join(self.resultPath, style))

    @staticmethod
    def _get_issue_template():
        with open(f'{os.path.dirname(os.path.realpath(__file__))}\\..\\..\\issue_list.txt',
                  'r', encoding='utf-8') as f:
            return f.read().split('\n')

    def create_from_template(self):
        os.chdir(os.path.join(self.resultPath, self.style))
        for name in self._get_issue_template():
            if not os.path.exists(name):
                os.mkdir(name)

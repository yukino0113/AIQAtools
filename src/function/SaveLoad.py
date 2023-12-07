import os
import shutil

from icecream import ic


class SaveLoad:

    def __init__(self, path):
        self.resultPath = os.path.join(os.path.dirname(path), 'result')
        self.style = None
        self._check_and_create_result_folder()

        """
        issue structure:
        self.issue = {
            issue_name: issue_folder_name,
            issue_name: issue_folder_name
        }
        """
        self.issue = self._get_issue_template()

    def _check_and_create_result_folder(self):
        if not os.path.exists(self.resultPath):
            os.mkdir(self.resultPath)

    def _check_and_create_style_folder(self, style):
        self._check_and_create_result_folder()
        if not os.path.exists(os.path.join(self.resultPath, style)):
            os.mkdir(os.path.join(self.resultPath, style))

    def _check_and_create_issue_folder(self):
        self._check_and_create_style_folder(self.style)
        os.chdir(os.path.join(self.resultPath, self.style))
        for name in self.issue.keys():
            if not os.path.exists(os.path.join(self.resultPath, self.style, self.issue[name])):
                os.mkdir(self.issue[name])
                if name not in ['正常', '已完成照片備存']:
                    open(
                        os.path.join(name, f'{os.path.join(self.resultPath, self.style, self.issue[name])}/對應圖片的問題描述.txt'),
                        'w', encoding='utf-8').close()

    @staticmethod
    def _get_issue_template():
        issue = {}
        with open(f'{os.path.dirname(os.path.realpath(__file__))}/../../issue_list.txt', 'r', encoding='utf-8') as f:
            for line in f.read().split('\n'):
                if ':' in line and not line.startswith('#'):
                    temp = line.split(':')
                    issue[temp[0]] = temp[1]
            issue['正常'] = '正常'
            issue['已完成照片備存'] = '已完成照片備存'
            return issue

    def get_delete_list(self, style: str, issue: list, image: str):
        self.style = style
        self._check_and_create_issue_folder()

        exist_list = [x for x in self.issue.keys()
                      if os.path.basename(image)
                      in os.listdir(os.path.join(self.resultPath, self.style, self.issue[x]))]
        return [x for x in exist_list if x not in issue]

    def save(self, style: str, issue: list, image: str):
        self.style = style
        file_name = os.path.basename(image)

        for issue_item in issue:
            issue_path = os.path.join(self.resultPath, self.style, self.issue[issue_item])
            if file_name not in os.listdir(issue_path):
                shutil.copy(image, issue_path)
        for del_issue in self.get_delete_list(self.style, issue, image):
            del_path = os.path.join(self.resultPath, self.style, self.issue[del_issue], file_name)
            os.remove(del_path)

        shutil.copy(image, os.path.join(self.resultPath, self.style, '已完成照片備存'))

    def load(self, image: str):
        issue_list = []
        for key in list(self.issue.keys()):
            if os.path.basename(image) in os.listdir(os.path.join(self.resultPath, self.style, self.issue[key])):
                issue_list.append(key)
        return issue_list

import os
import shutil

from src.function.Logging import Logging as LOG

from icecream import ic


class SaveLoad:

    def __init__(self, path):
        self.resultPath = os.path.join(os.path.dirname(path), 'result')
        self.style = None
        self._check_and_create_result_folder()
        self.log = LOG()

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
            self.log.log('Create result folder', f'Create result folder at: {self.resultPath}')

    def _check_and_create_style_folder(self, style):
        self._check_and_create_result_folder()
        if not os.path.exists(style_path := os.path.join(self.resultPath, style)):
            os.mkdir(style_path)
            self.log.log('Create style folder', f'Create style folder at: {style_path}')

    def _check_and_create_issue_folder(self):
        self._check_and_create_style_folder(self.style)
        os.chdir(os.path.join(self.resultPath, self.style))
        for name in self.issue.keys():
            if not os.path.exists(issue_path := os.path.join(self.resultPath, self.style, self.issue[name])):
                os.mkdir(self.issue[name])
                self.log.log('Create issue folder', f'Create issue folder at: {issue_path}')
                if name not in ['正常', '已完成照片備存']:
                    open(os.path.join(name, f'{issue_path}/對應圖片的問題描述.txt'), 'w', encoding='utf-8').close()
                    self.log.log('Create issue desc file', "Create issue desc file at ")

    def _get_issue_template(self):
        issue = {}
        with open(f'{os.path.dirname(os.path.realpath(__file__))}/../../issue_list.txt', 'r', encoding='utf-8') as f:
            for line in f.read().split('\n'):
                if ':' in line and not line.startswith('#'):
                    temp = line.split(':')
                    issue[temp[0]] = temp[1]
            issue['正常'] = '正常'
            issue['已完成照片備存'] = '已完成照片備存'
            self.log.log('Load issue txt', f'Issue template loaded from '
                                           f'{os.path.dirname(os.path.realpath(__file__))}/../../issue_list.txt')
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
                self.log.log('Save image', f'Saved {file_name} to {issue_item}')

        for del_issue in self.get_delete_list(self.style, issue, image):
            del_path = os.path.join(self.resultPath, self.style, self.issue[del_issue], file_name)
            os.remove(del_path)
            self.log.log('Delete image', f'Delete {file_name} from {del_issue}')

        shutil.copy(image, os.path.join(self.resultPath, self.style, '已完成照片備存'))
        self.log.log('Save image', f'Saved {file_name} to 已完成照片備存')

    def load(self, image: str):
        issue_list = []
        for key in list(self.issue.keys()):
            if os.path.basename(image) in os.listdir(os.path.join(self.resultPath, self.style, self.issue[key])):
                issue_list.append(key)
        self.log.log('Load image', f'Loaded {os.path.basename(image)} from {issue_list}')
        return issue_list

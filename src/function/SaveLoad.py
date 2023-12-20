import os
import shutil

from src.function.Logging import Logging


class SaveLoad(Logging):

    def __init__(self, path):
        super().__init__()
        self.resultPath = os.path.join(os.path.dirname(path), 'result')
        self.log_path = os.path.join(self.resultPath, 'log.txt')
        self.style = None
        self._check_and_create_result_folder()
        self.clear_logs()

        """
        issue structure:
        self.issue = {
            issue_name: issue_folder_name,
            issue_name: issue_folder_name
        }
        """
        self.issue = self._get_issue_template()

    def clear_logs(self):
        open(os.path.join(f'{self.resultPath}/log.txt'), 'w+', encoding='utf-8').close()

    def _check_and_create_result_folder(self):
        if not os.path.exists(self.resultPath):
            os.mkdir(self.resultPath)
            self.log_message('Create result folder', f'Create result folder at: {self.resultPath}', self.log_path)

    def _check_and_create_style_folder(self, style):
        self._check_and_create_result_folder()
        if not os.path.exists(style_path := os.path.join(self.resultPath, style)):
            os.mkdir(style_path)
            self.log_message('Create style folder', f'Create style folder at: {style_path}', self.log_path)

    def _check_and_create_issue_folder(self):
        self._check_and_create_style_folder(self.style)
        os.chdir(os.path.join(self.resultPath, self.style))
        for name in self.issue.keys():
            if not os.path.exists(issue_path := os.path.join(self.resultPath, self.style, self.issue[name])):
                os.mkdir(self.issue[name])
                self.log_message('Create issue folder', f'Create issue folder at: {issue_path}', self.log_path)
                if name not in ['正常', '已完成照片備存']:
                    open(os.path.join(name, f'{issue_path}/對應圖片的問題描述.txt'), 'w', encoding='utf-8').close()
                    self.log_message('Create issue desc file', "Create issue desc file at ", self.log_path)

    def _get_issue_template(self):
        issue = {}
        with open(f'{os.path.dirname(os.path.realpath(__file__))}/../../issue_list.txt', 'r', encoding='utf-8') as f:
            for line in f.read().split('\n'):
                if ':' in line and not line.startswith('#'):
                    temp = line.split(':')
                    issue[temp[0]] = temp[1]
            issue['正常'] = '正常'
            issue['已完成照片備存'] = '已完成照片備存'
            self.log_message('Load issue txt', f'Issue template loaded from '
                                               f'{os.path.dirname(os.path.realpath(__file__))}/../../issue_list.txt',
                             self.log_path)
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
                self.log_message('Save image', f'Saved {file_name} to {issue_item}', self.log_path)

        for del_issue in self.get_delete_list(self.style, issue, image):
            if del_issue == '已完成照片備存':
                continue
            del_path = os.path.join(self.resultPath, self.style, self.issue[del_issue], file_name)
            os.remove(del_path)
            self.log_message('Delete image', f'Delete {file_name} from {del_issue}', self.log_path)

        shutil.copy(image, os.path.join(self.resultPath, self.style, '已完成照片備存'))
        self.log_message('Backup image', f'Saved {file_name} to 已完成照片備存', self.log_path)

    def load(self, image: str):
        issue_list = []
        for key in list(self.issue.keys()):
            if os.path.basename(image) in os.listdir(os.path.join(self.resultPath, self.style, self.issue[key])):
                issue_list.append(key)
        self.log_message('Load image', f'Loaded {os.path.basename(image)} from {issue_list}', self.log_path)
        return issue_list

    def log_final_summary(self):

        self.log_end(self.log_path)

        image_sum = len(os.listdir(os.path.join(self.resultPath, self.style, '已完成照片備存')))

        logs = {}
        issue_count_list = []
        for key in self.issue.keys():
            if key not in ['正常', '已完成照片備存']:
                logs[key] = {}
                item_count = [item for item in os.listdir(os.path.join(self.resultPath, self.style, self.issue[key]))
                              if not item.endswith('.txt')]
                logs[key]['quan'] = len(item_count)
                issue_count_list += item_count

        self.log_summary('張數', image_sum, self.log_path)
        self.log_summary('整體', len(set(issue_count_list)), self.log_path)

        for issue in logs.keys():
            if issue not in ['正常', '已完成照片備存']:
                self.log_summary(issue, logs[issue]['quan'], self.log_path)

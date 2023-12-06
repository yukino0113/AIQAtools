import os
import shutil

from icecream import ic


class SaveLoad:

    def __init__(self, path):
        self.resultPath = os.path.join(path, 'result')
        self.style = None
        self._check_and_create_result_folder()

        self.issueFolder = {
            '身形太壯、怪異肌肉': '1_(男)身形太壯怪異肌肉',
            '胸部過大不自然': '2_(女)胸部過大不自然',
            '胸部形狀位置怪異': '3_(女)胸部形狀位置怪異',
            '頭髮沒切乾淨突出': '4_(女)頭髮沒切乾淨突出',
            '臉切壞': '5_臉切壞',
            '膚色斷差': '6_膚色斷差',
            '手指': '7_手趾',
            '頭身比不符': '8_頭身比不符(QA)',
            '背景怪異': '9_背景怪異(QA)',
            '頭髮(色)髮型改變': '10_頭髮(色)髮型改變(QA)',
            '裸露': '11_裸露',
            '性別錯亂': '12_性別錯亂',
            '衣服剪裁': '13_衣服剪裁',
            '風格不符': '14_風格不符',
            '骨架異常': '骨架異常',
            '其他': 'XX_其他',
            '正常': '正常'
        }

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
        for name in self._get_issue_template():
            if not os.path.exists(name):
                os.mkdir(name)
                if name != '正常':
                    open(os.path.join(name, f'{os.path.join(self.resultPath, self.style, name)}\對應圖片的問題描述.txt'), 'w', encoding='utf-8').close()
        os.mkdir('已完成照片備存')

    @staticmethod
    def _get_issue_template():
        with open(f'{os.path.dirname(os.path.realpath(__file__))}/../../issue_list.txt', 'r', encoding='utf-8') as f:
            return f.read().split('\n')

    def get_delete_list(self, style: str, issue: list, image: str):
        self.style = style
        self._check_and_create_issue_folder()

        exist_list = [x for x in self.issueFolder.keys()
                      if os.path.basename(image)
                      in os.listdir(os.path.join(self.resultPath, self.style, self.issueFolder[x]))]
        return [x for x in exist_list if x not in issue]

    def save(self, style: str, issue: list, image: str):
        self.style = style
        file_name = os.path.basename(image)

        for issue_item in issue:
            issue_path = os.path.join(self.resultPath, self.style, self.issueFolder[issue_item])
            if file_name not in os.listdir(issue_path):
                shutil.copy(image, issue_path)
        for del_issue in self.get_delete_list(self.style, issue, image):
            del_path = os.path.join(self.resultPath, self.style, self.issueFolder[del_issue], file_name)
            os.remove(del_path)

        shutil.copy(image, os.path.join(self.resultPath, self.style, '已完成照片備存'))

    def load(self, image: str):
        issue_list = []
        for key in list(self.issueFolder.keys()):
            if os.path.basename(image) in os.listdir(os.path.join(self.resultPath, self.style, self.issueFolder[key])):
                issue_list.append(key)
        return issue_list

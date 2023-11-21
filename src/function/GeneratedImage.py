import os

from icecream import ic


class GeneratedImage:
    def __init__(self, path):
        self.path = path
        self.imagePathDic = ic(self.get_generated_path())
        self.styleOrder = 0
        self.ImageOrder = 0
        self.currentStyle = list(self.imagePathDic.keys())[self.styleOrder]
        self.currentImage = list(self.imagePathDic[self.currentStyle].keys())[self.ImageOrder]
        self.test = 0

    def get_generated_path(self) -> dict:
        image_dict = {}
        for style_folder in [x for x in os.listdir(self.path)
                             if (os.path.isdir(os.path.join(self.path, x)) and 'Design' in x)]:
            image_dict[style_folder] = {}
            for source_folder in style_folder:
                path = os.path.join(self.path, style_folder)
                source_folder = ic(x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x)))
                for folder in source_folder:
                    os.chdir(os.path.join(path, folder))
                    for file in os.listdir(os.path.join(path, folder)):
                        image_dict[style_folder][file.split('.jpg')[0]] = os.path.join(path, folder, file)
        return image_dict

    def next(self):
        if self.ImageOrder < len(list(self.imagePathDic[self.currentStyle].keys())):
            self.ImageOrder += 1

    def previous(self):
        if self.ImageOrder > 0:
            self.ImageOrder -= 1


GeneratedImage("C:\\Users\\jethro_wang\\Desktop")
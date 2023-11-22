import os

from icecream import ic


class GeneratedImage:
    def __init__(self, path):
        self.path = path
        self.imageMaxCount = 0
        self.imagePathDic = self._get_path()
        self.ImageOrder = 0

        if self.imagePathDic:
            self._refresh_current_style_and_image()

    def _refresh_current_style_and_image(self):
        self.currentStyle = list(self.imagePathDic.keys())[self.ImageOrder // 80]
        self.currentImage = list(self.imagePathDic[self.currentStyle].keys())[self.ImageOrder % 80]

    def _get_path(self) -> dict:
        image_dict = {}
        for styleFolder in [x for x in os.listdir(self.path)
                            if (os.path.isdir(os.path.join(self.path, x)) and 'Design' in x)]:
            image_dict[styleFolder] = {}
            for source_folder in styleFolder:
                path = os.path.join(self.path, styleFolder)
                source_folder = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
                for folder in source_folder:
                    os.chdir(os.path.join(path, folder))
                    for file in os.listdir(os.path.join(path, folder)):
                        image_dict[styleFolder][file.split('.jpg')[0]] = os.path.join(path, folder, file)
            self.imageMaxCount += len(list(image_dict[styleFolder].keys()))
        return image_dict

    def next(self):
        if self.ImageOrder < self.imageMaxCount - 1:
            self.ImageOrder += 1
            self._refresh_current_style_and_image()
        else:
            # todo: error handling
            pass

    def previous(self):
        if self.ImageOrder > 0:
            self.ImageOrder -= 1
            self._refresh_current_style_and_image()
        else:
            # todo: error handling
            pass

    def get_current_image_path(self) -> str:
        return self.imagePathDic[self.currentStyle][self.currentImage]

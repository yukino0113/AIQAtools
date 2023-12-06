import os
from icecream import ic

class ReferenceImage:

    def __init__(self, path):
        self.imagePathList = self._get_path(path)

    @staticmethod
    def _get_path(path) -> dict:

        image = {}

        # get image from folder
        for file in os.listdir(path):
            if file.endswith('.png') or file.endswith('.jpg'):
                image[os.path.basename(file).split('.')[0]] = os.path.join(path, file)

        return ic(image)

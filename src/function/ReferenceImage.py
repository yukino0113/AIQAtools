import os
from ..function.Logging import Logging
from icecream import ic


class ReferenceImage:

    def __init__(self, path):
        self.imagePathList = self._get_path(path)
        self.log = Logging()

    def _get_path(self, path) -> dict:

        image = {}

        # get image from folder
        for file in os.listdir(path):
            if file.endswith('.png') or file.endswith('.jpg'):
                image[os.path.basename(file).split('.')[0]] = os.path.join(path, file)
        self.log.log('Load Reference Image', f'Loaded reference image from {path}')
        return image

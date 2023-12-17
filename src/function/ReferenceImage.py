import os
from ..function.Logging import Logging
from icecream import ic


class ReferenceImage(Logging):

    def __init__(self, path):
        super().__init__()
        self.imagePathList = self._get_path(path)

    def _get_path(self, path) -> dict:

        image = {}

        # get image from folder
        for file in os.listdir(path):
            if file.endswith('.png') or file.endswith('.jpg'):
                image[os.path.basename(file).split('.')[0]] = os.path.join(path, file)
        self.log('Load Reference Image', f'Loaded reference image from {path}')
        return image

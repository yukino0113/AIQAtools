import os
from ..function.Logging import Logging
from icecream import ic


class ReferenceImage(Logging):

    def __init__(self, path, log_path):
        self.log_path = os.path.join(os.path.dirname(log_path), 'result', 'log.txt')
        self.imagePathList = self._get_path(path)

    def _get_path(self, path) -> dict:

        image = {}

        # get image from folder
        for file in os.listdir(path):
            if file.endswith('.png') or file.endswith('.jpg'):
                image[os.path.basename(file).split('.')[0]] = os.path.join(path, file)
        self.log_message('Load Reference Image', f'Loaded reference image from {path}', self.log_path)
        return image

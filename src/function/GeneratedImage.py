import os
from .Logging import Logging


class GeneratedImage(Logging):

    def __init__(self, path):
        self.path = path
        self.log_path = os.path.join(os.path.dirname(path), 'result', 'log.txt')
        self.imagePathList = self._get_path()

        self.currentImageIndex = 0

        self.currentStyle = os.path.basename(path)
        self.currentImage = self.imagePathList[self.currentImageIndex]

    def _get_path(self) -> list:
        """
        Source folder structure:
        - Style folder (self.path)
        -- Source folder
        --- Image file

        styleImageList Structure: [str, str, str, ...]
        """

        image_lst = []

        # get image from folder
        for file in os.listdir(self.path):
            if file.endswith('.png') or file.endswith('.jpg'):
                image_lst.append(os.path.join(self.path, file))

        # get image from child folder
        source_folder_list = [x for x in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, x))]
        for source_folder in source_folder_list:
            source_folder_path = os.path.join(self.path, source_folder)

            for file in os.listdir(source_folder_path):
                if file.endswith('.png') or file.endswith('.jpg'):
                    image_lst.append(os.path.join(source_folder_path, file))

        self.log_message('Load Generated Image', f'Loaded generated image from {self.path}', self.log_path)
        return image_lst

    def next(self):
        if self.currentImageIndex < len(self.imagePathList) - 1:
            self.currentImageIndex += 1
            self.currentImage = self.imagePathList[self.currentImageIndex]

    def previous(self):
        if self.currentImageIndex > 0:
            self.currentImageIndex -= 1
            self.currentImage = self.imagePathList[self.currentImageIndex]


import os

from icecream import ic


class GeneratedImage:

    def __init__(self, path):
        self.path = path
        self.imagePathList = self._get_path()

        self.currentImageIndex = 0

        self.currentStyle = None
        self.currentImage = self.imagePathList[self.currentImageIndex]

    def _get_path(self) -> list:
        """
        Source folder structure:

        - Style folder (self.path)
        -- Source folder
        --- Image file

        styleImageDict Structure:
        {
            style: {
                image_path: [str, str, str, ...]
            }
        }
        :return: image_dict: dict
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

        return ic(image_lst)

    def next(self):
        if self.currentImageIndex < len(self.imagePathList) - 1:
            self.currentImageIndex += 1
            self.currentImage = self.imagePathList[self.currentImageIndex]

    def previous(self):
        if self.currentImageIndex > 0:
            self.currentImageIndex -= 1
            self.currentImage = self.imagePathList[self.currentImageIndex]


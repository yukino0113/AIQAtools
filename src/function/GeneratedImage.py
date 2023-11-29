import os

from icecream import ic


class GeneratedImage:
    def __init__(self, path):
        self.path = path
        self.imagePathDic = self._get_path()

        self.currentImageIndex = 0
        self.currentStyleIndex = 0

        if self.imagePathDic:
            self._refresh_current_style_and_image()

    def _refresh_current_style_and_image(self):
        self.currentStyle = list(self.imagePathDic.keys())[self.currentStyleIndex]
        self.currentImage = self.imagePathDic[self.currentStyle][self.currentImageIndex]

    def _get_path(self) -> dict:
        """
        Source folder structure:

        - Path folder (self.path)
        -- Style folder
        --- Source folder
        ---- Image file

        styleImageDict Structure:
        {
            style: {
                image_path: [str, str, str, ...]
            }
        }
        :return: image_dict: dict
        """

        image_dict = {}

        # If x in the result path is a folder and file name contains 'Design'
        style_folder_list = \
            [styleFolderName for styleFolderName in os.listdir(self.path)
             if (os.path.isdir(os.path.join(self.path, styleFolderName)) and 'Design' in styleFolderName)]

        for styleFolder in style_folder_list:
            image_dict[styleFolder] = []

            for source_folder in styleFolder:
                style_path = os.path.join(self.path, styleFolder)
                # Get all the folder in the style folder
                source_folder = [x for x in os.listdir(style_path) if os.path.isdir(os.path.join(style_path, x))]

                for folder in source_folder:
                    # todo: need this?
                    os.chdir(os.path.join(style_path, folder))

                    for file in os.listdir(os.path.join(style_path, folder)):
                        image_dict[styleFolder].append(os.path.join(style_path, folder, file))

            if len(image_dict[styleFolder]) == 0:
                del image_dict[styleFolder]

        return image_dict

    def next(self):
        if self.currentImageIndex < len(self.imagePathDic[self.currentStyle]) - 1:
            self.currentImageIndex += 1
            self._refresh_current_style_and_image()
        else:
            self.currentStyleIndex += 1
            self.currentImageIndex = 0

    def previous(self):
        if self.currentImageIndex > 0:
            self.currentImageIndex -= 1
        else:
            if self.currentStyleIndex > 0:
                self.currentStyleIndex -= 1
                self.currentImageIndex = len(self.imagePathDic[self.currentStyle]) - 1
        self._refresh_current_style_and_image()

    def get_current_image_path(self) -> str:
        return self.imagePathDic[self.currentStyle][self.currentImageIndex]

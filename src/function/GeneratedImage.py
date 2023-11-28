import os

from icecream import ic


class GeneratedImage:
    def __init__(self, path):
        self.path = path
        self.imagePathDic = self._get_path()

        self.currentStyle = None
        self.currentImage = None

        if self.imagePathDic:
            # self._refresh_current_style_and_image()
            pass


    def _refresh_current_style_and_image(self):
        # todo: need to change logic for image order
        self.currentStyle = list(self.imagePathDic.keys())[self.ImageOrder // 80]
        self.currentImage = list(self.imagePathDic[self.currentStyle].keys())[self.ImageOrder % 80]

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
                quantity: int,
                image_path: [str, str, str, ...]
            }
        }

        :return: image_dict: dict
        """

        def _clean_empty_style_folder(image_path_dict: dict) -> dict:
            for style in image_path_dict.keys():
                if image_path_dict[style]['quantity'] == 0:
                    image_path_dict.pop(style)
            return image_path_dict

        image_dict = {}

        # If x in the result path is a folder and file name contains 'Design'
        style_folder_list = \
            [styleFolderName for styleFolderName in os.listdir(self.path)
             if (os.path.isdir(os.path.join(self.path, styleFolderName)) and 'Design' in styleFolderName)]

        for styleFolder in style_folder_list:
            image_dict[styleFolder] = {}

            for source_folder in styleFolder:
                style_path = os.path.join(self.path, styleFolder)
                # Get all the folder in the style folder
                source_folder = [x for x in os.listdir(style_path) if os.path.isdir(os.path.join(style_path, x))]

                for folder in source_folder:
                    # todo: need this?
                    os.chdir(os.path.join(style_path, folder))

                    image_dict[styleFolder]['image_path'] = []

                    for file in os.listdir(os.path.join(style_path, folder)):
                        image_dict[styleFolder]['image_path'].append(os.path.join(style_path, folder, file))

            image_dict[styleFolder]['quantity'] = len(list(image_dict[styleFolder]['image_path'].keys()))

        return ic(_clean_empty_style_folder(image_dict))

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

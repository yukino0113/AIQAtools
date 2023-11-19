import configparser
from os import listdir
from os.path import isfile, join

from icecream import ic


class TestImage:

    def __init__(self):
        self.path = self.__get_path()
        self.__get_image()

    @staticmethod
    def __get_path() -> str:
        config = configparser.ConfigParser()
        config.read('../config.ini')
        return config['fileIO']['input_path']

    def __get_image_path_list(self) -> list:
        ic([x for x in listdir(self.path) if not isfile(join(self.path, x))])
        pass

TestImage()



import configparser
from icecream import ic

cf = configparser.ConfigParser()
cf.read('config.ini', encoding='utf-8')

ic(cf['option']['options'])
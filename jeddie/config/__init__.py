import json
import os

from exceptions.exceptions import MissingConfigException

CONFIG_PATH = os.getenv('CONFIG_PATH')
if not CONFIG_PATH:
    raise MissingConfigException('Please set the CONFIG_PATH environment variable to the json config file.')


class ConfigLoader:
    def __init__(self):
        self._load_config()

    def _load_config(self):
        file = open(CONFIG_PATH, "r")
        raw_config = json.load(file)
        for key, value in raw_config.items():
            setattr(self, key, value)


config = ConfigLoader()

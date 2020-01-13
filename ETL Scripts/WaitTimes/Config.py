# Config file object

from json import loads


class Config:
    # Config file locations
    __db_path__ = "config/dbconnections.json"

    def __init__(self):
        self.db_info = self.__load_db_info__()

    def __load_db_info__(self):
        with open(self.__db_path__) as file:
            return loads(file.read())

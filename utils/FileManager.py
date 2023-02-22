import json
from PIL import Image
import imagehash


class FileManager:
    @staticmethod
    def get_data_from_json_file(file='configurations/db_access_configuration.json') -> dict:
        """
        readying test_data_from_file from json file
        :return: test_data_from_file from json file
        """

        with open(file, 'r', encoding='utf-8') as config:
            return json.load(config)

    @staticmethod
    def hash_it(path):
        img = Image.open(path)
        image_one_hash = imagehash.whash(img)
        print(image_one_hash)

import json
from project.resources.constains.constants import Constants


class ManageTestData(object):
    test_data = ""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ManageTestData, cls).__new__(cls)
            with open(Constants.TEST_DATA_FILE_NAME) as test_data_file:
                cls.test_data = json.load(test_data_file)
        return cls.instance

    @classmethod
    def get_param(cls, name):
        return cls.test_data[name]

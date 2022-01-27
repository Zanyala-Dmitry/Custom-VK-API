import logging
from project.resources.constains.constants import Constants


class Logger:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logger, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def initialization():
        logging.basicConfig(filename=Constants.LOG_FILE_NAME,
                            format='%(asctime)s %(levelname)s:%(message)s',
                            level=logging.INFO)

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def error(message):
        logging.error(message)

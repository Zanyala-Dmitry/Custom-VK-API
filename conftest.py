import pytest
from framework.driver.browser import Browser
from utils.logger_ import Logger

logger = Logger()
logger.initialization()


@pytest.fixture(scope="function")
def before_after_test():
    Browser.maximize()
    yield
    Browser.quit()

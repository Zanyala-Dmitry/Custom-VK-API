from framework.driver.browser import Browser
from project.resources.constains.constants import Constants

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException


class FormStateProvider:

    def __init__(self, element):
        self.element = element

    def wait_for_displayed(self):
        try:
            WebDriverWait(
                Browser.get_driver(), Constants.TIMEOUT_SECONDS).until(
                ec.presence_of_element_located(
                    self.element.locator))
            return True
        except TimeoutException:
            return False

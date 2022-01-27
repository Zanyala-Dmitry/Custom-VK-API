from selenium.webdriver.common.by import By

from utils.logger_ import Logger
from framework.driver.browser import Browser
from project.resources.constains.constants import Constants
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException


class BaseElement:
    locator = None

    def __init__(self, locator, name):
        if isinstance(locator, tuple):
            self.locator = locator
        else:
            self.locator = (By.XPATH if "/" in locator else By.ID, locator)
        self.name = name

    def _find_element(self):
        Logger().info(f"Search element: {self.name}")
        try:
            element = WebDriverWait(
                Browser.get_driver(), Constants.TIMEOUT_SECONDS).\
                until(ec.presence_of_element_located(self.locator))
        except TimeoutException:
            element = None
            Logger().error("Can't find element")
        return element

    def _find_elements(self):
        Logger().info(f"Search elements: {self.name}")
        try:
            elements_list = WebDriverWait(
                Browser.get_driver(), Constants.TIMEOUT_SECONDS).\
                until(ec.presence_of_all_elements_located(self.locator))
        except TimeoutException:
            elements_list = list()
            Logger().error("Can't find elements")
        return elements_list

    def click(self):
        Logger().info(f"Click on element: {self.name}")
        element = self._find_element()
        if element is not None:
            element.click()

    def get_attribute(self, attribute):
        Logger().info(f"Getting attribute element: {self.name}")
        element = self._find_element()
        if element is not None:
            return element.get_attribute(attribute)
        else:
            Logger().error("Can't find elements")
            return None

    def get_text(self):
        element = self._find_element()
        return element.text

    def get_size(self, measurement):
        return self._find_element().size[measurement]

    def get_screenshot(self):
        return self._find_element().screenshot_as_png

    def is_displayed(self):
        try:
            WebDriverWait(
                Browser.get_driver(), Constants.TIMEOUT_SECONDS). \
                until(
                ec.visibility_of_element_located(self.locator))
            return True
        except TimeoutException:
            return False

    def is_exist(self):
        try:
            WebDriverWait(
                Browser.get_driver(), Constants.TIMEOUT_SECONDS).until(
                ec.presence_of_element_located(self.locator))
            return True
        except TimeoutException:
            return False

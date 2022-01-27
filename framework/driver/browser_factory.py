from project.resources.constains.test_settings import TestSettings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class BrowserFactory:
    @staticmethod
    def make_driver():
        browser_type = TestSettings.BROWSER
        s = Service(ChromeDriverManager().install())
        web_driver = None
        if browser_type == "chrome":
            web_driver = webdriver.Chrome(service=s)
        if browser_type == "firefox":
            web_driver = webdriver.Firefox(executable_path=GeckoDriverManager().
                                           install())
        return web_driver

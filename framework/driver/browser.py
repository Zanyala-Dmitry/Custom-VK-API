from framework.driver.browser_factory import BrowserFactory
from selenium.webdriver.common.action_chains import ActionChains


class Singleton(type):
    _instances = {}

    def __call__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__()
        return cls._instances[cls]

    def destroy(cls):
        try:
            del Singleton._instances[cls]
        except KeyError:
            pass


class Browser(metaclass=Singleton):
    __driver = None

    def __init__(self):
        Browser.__driver = BrowserFactory.make_driver()

    @classmethod
    def get_driver(cls):
        return cls.__driver

    @classmethod
    def quit(cls):
        cls.get_driver().close()
        cls.destroy()

    @classmethod
    def maximize(cls):
        cls.get_driver().maximize_window()

    @classmethod
    def open_url(cls, url):
        cls.get_driver().get(url)

    @classmethod
    def get_url(cls):
        return cls.get_driver().current_url

    @classmethod
    def switch_to_default_content(cls):
        cls.get_driver().switch_to.default_content()

    @classmethod
    def open_previous_page(cls):
        cls.get_driver().back()

    @classmethod
    def get_screenshot(cls):
        return cls.get_driver().get_screenshot_as_png()

    @classmethod
    def scroll_to_element(cls, element):
        actions = ActionChains(cls.get_driver())
        actions.move_to_element(element).perform()

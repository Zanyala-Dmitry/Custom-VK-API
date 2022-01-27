from framework.element.base_element import BaseElement


class BaseForm(object):
    def __init__(self, selector, name):
        self.type = "Form"
        self.element = BaseElement(selector, "")
        self.name = name

    def is_opened(self):
        return self.element.is_displayed()

from framework.element.base_element import BaseElement


class Button(BaseElement):
    def __init__(self, locator, name):
        self.subtype = "button"
        super().__init__(locator, name)

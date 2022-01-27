from framework.element.base_element import BaseElement


class Label(BaseElement):
    def __init__(self, locator, name):
        self.subtype = "label"
        super().__init__(locator, name)

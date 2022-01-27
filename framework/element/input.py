from framework.element.base_element import BaseElement


class Input(BaseElement):
    def __init__(self, locator, name):
        self.subtype = "input"
        super().__init__(locator, name)

    def type_text(self, message, clear=True):
        element = self._find_element()
        if clear:
            element.clear()
        element.send_keys(message)

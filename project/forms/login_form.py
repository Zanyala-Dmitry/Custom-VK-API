from framework.forms.base_form import BaseForm
from framework.element.input import Input
from framework.element.button import Button


class LoginForm(BaseForm):
    def __init__(self):
        self.type = "Form"
        self._login_text_box = Input("index_email", "Login text box")
        self._password_text_box = Input("index_pass", "Password text box")
        self._login_button = Button("index_login_button", "Login button")

        super().__init__('index_forgot', "Login card")

    def _set_login(self, login):
        self._login_text_box.type_text(login)

    def _set_password(self, password):
        self._password_text_box.type_text(password)

    def _click_login_button(self):
        self._login_button.click()

    def filling_login_page(self, login, password, to_login=True):
        self._set_login(login)
        self._set_password(password)
        if to_login:
            self._click_login_button()

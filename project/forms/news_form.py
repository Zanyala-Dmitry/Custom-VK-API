import re
from framework.forms.base_form import BaseForm
from framework.element.button import Button
from framework.element.label import Label


class NewsForm(BaseForm):
    def __init__(self):
        self.type = "Form"
        self._my_page_button = Button("l_pr", "My page button")
        self._get_label_what_new = Label("submit_post_box",
                                         "User label 'what new'")

        super().__init__("ui_rmenu_news", "News card")

    def click_my_page_button(self):
        self._my_page_button.click()

    def get_user_id(self):
        match = re.search(r'\d+', self._get_label_what_new.
                          get_attribute("data-from-oid"))
        return match[0]

from selenium.webdriver.common.by import By
from framework.driver.browser import Browser
from framework.forms.base_form import BaseForm
from framework.element.label import Label
from framework.element.button import Button
from project.resources.constains.js_constants import JSConstants


class ProfileForm(BaseForm):
    LABEL_DELETED_POST_LOC_TEMPLATE = "//div[@id='post{}_{}'and contains(" \
                                    "@class, 'unshown')]"
    LABEL_USER_NAME_LOC_TEMPLATE = "//div[@id='post{}_{}']//h5/a"
    LABEL_COMMENT_MESSAGE_LOC_TEMPLATE = "//div[@id='post{}_{}']" \
                                         "//div[@class='reply_author']/a"
    LABEL_POST_MESSAGE_LOC_TEMPLATE = "//div[@id='post{}_{}']" \
                                      "//div[contains(@class,'wall_post_text')]"
    LABEL_DOC_TITLE_LOC_TEMPLATE = "//div[@id='wpt{}_{}']" \
                                   "//a[contains(@class,'page_doc_title')]"
    BUTTON_SHOW_COMMENT_LOC_TEMPLATE = "//div[contains(@id,'replies{}_{}')]/a"
    BUTTON_POST_LIKE_LOC_TEMPLATE = "//div[@id='post{}_{}']" \
                                    "//span[contains(@Class,'_like')]"
    LIST_POST_MESSAGE_LOC_TEMPLATE = "//div[text()='{}']"
    LIST_POST_PICTURE_LOC_TEMPLATE = "//div[@id='wpt{}_{}']//a"
    IMAGE_FIELD_POST_PICTURE_LOC_TEMPLATE = "//div[@id='wpt{}_{}']"\
                                            "//div[contains(@class," \
                                            "'page_post_sized_thumbs')]"

    def __init__(self):
        self.type = "Form"
        self._label_name = Label((By.CLASS_NAME, "page_name"), "User name "
                                                               "label")
        self._profile_button = Button("top_profile_link", "User profile button")
        self._logout_button = Button("top_logout_link", "User logout button")
        self._quick_login_button = Button("quick_login_button",
                                          "Quick login button")

        super().__init__("profile", "Profile card")

    def get_user_name(self):
        return self._label_name.get_text()

    def is_post_deleted(self, user_id, post_id):
        return Label(self.LABEL_DELETED_POST_LOC_TEMPLATE.format(user_id,
                                                                 post_id),
                     "Label deleted post").is_exist()

    def get_post_user_name(self, user_id, post_id):
        return Label(self.LABEL_USER_NAME_LOC_TEMPLATE.format(user_id, post_id),
                     "Label user name").get_text()

    def is_message_present(self, message):
        return Label(self.LIST_POST_MESSAGE_LOC_TEMPLATE.format(message),
                     "Post message label").is_displayed()

    def get_comment_user_name(self, user_id, post_id):
        Button(self.BUTTON_SHOW_COMMENT_LOC_TEMPLATE.format(user_id, post_id),
               "Show comments button").click()
        return Label(self.LABEL_COMMENT_MESSAGE_LOC_TEMPLATE.format(user_id,
                                                                    post_id),
                     'Comment author label').get_text()

    def click_like_post_button(self, user_id, post_id):
        Button(self.BUTTON_POST_LIKE_LOC_TEMPLATE.format(user_id, post_id),
               "Post like button").click()

    def get_photo_id(self, user_id, post_id):
        data_photo_id = Label(self.LIST_POST_PICTURE_LOC_TEMPLATE.format(
            user_id, post_id), "Post picture").\
            get_attribute("data-photo-id").split("_")
        return data_photo_id[1]

    def get_doc_name(self, user_id, post_id):
        return Label(self.LABEL_DOC_TITLE_LOC_TEMPLATE.format(user_id, post_id),
                     "Document link").get_text()

    def get_post_message(self, user_id, post_id):
        return Label(self.LABEL_POST_MESSAGE_LOC_TEMPLATE.format(user_id,
                                                                 post_id),
                     "Post message label").get_text()

    def is_quick_login_form_present(self):
        return self._quick_login_button.is_displayed()

    def get_image_screenshot(self, user_id, post_id):
        image_element = Label(self.IMAGE_FIELD_POST_PICTURE_LOC_TEMPLATE.
                              format(user_id, post_id), "Post picture")
        Browser.get_driver().execute_script(JSConstants.SCROLL_TO,
                                            image_element.get_size('height'))
        return image_element.get_screenshot()

    def logout(self):
        self._profile_button.click()
        self._logout_button.click()

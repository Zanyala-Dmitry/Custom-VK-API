import pytest
from utils.manage_test_data import ManageTestData
from utils.random_utils import RandomText
from utils.vk_api_utils import VkApiUtils
from utils.image_functions import ImageFunctions
from project.resources.constains.test_settings import TestSettings
from framework.utils.framework_utils import ConditionalWait
from framework.driver.browser import Browser
from project.forms.profile_form import ProfileForm
from project.forms.login_form import LoginForm
from project.forms.news_form import NewsForm


class TestVKAPI:
    browser = Browser
    test_data = ManageTestData()
    image_functions = ImageFunctions()
    min_randomize_string_length = test_data.get_param(
        "MinRandomizeStringLength")
    max_randomize_string_length = test_data.get_param(
        "MaxRandomizeStringLength")
    conditional_wait = ConditionalWait()
    news_form = NewsForm()
    profile_form = ProfileForm()
    login_form = LoginForm()

    user_1_login = str(test_data.get_param("User_1_login"))
    user_1_password = test_data.get_param("User_1_password")
    user_2_login = test_data.get_param("User_2_login")
    user_2_password = test_data.get_param("User_2_password")
    image_png = test_data.get_param("UploadingPhotoPngPath")
    image_jpg = test_data.get_param("UploadingPhotoJpgPath")

    test_case_data = [(user_1_login, user_1_password, image_png)]

    @pytest.mark.parametrize("user_login, user_password, image_path",
                             test_case_data)
    def test_user_add_photo_and_like(self, user_login, user_password,
                                     image_path, before_after_test):
        Browser().open_url(TestSettings.URL_VK)
        assert self.login_form.is_opened(), \
            "Login card should be displayed"
        self.login_form.filling_login_page(user_login, user_password)

        user_id = self.news_form.get_user_id()
        vk_api_utils = VkApiUtils(user_id, "User_1", image_path)
        assert self.news_form.is_opened(), "News card should be displayed"
        self.news_form.click_my_page_button()

        assert self.profile_form.is_opened(), \
            "Profile card should be displayed"

        message = RandomText.get_randomize_text(
            self.min_randomize_string_length,
            self.max_randomize_string_length)
        post_id = vk_api_utils.create_post(message)
        user_name = self.profile_form.get_user_name()

        assert self.profile_form.get_post_user_name(user_id, post_id) == \
               user_name, "User names should be equals"

        edited_message = RandomText.get_randomize_text(
            self.min_randomize_string_length,
            self.max_randomize_string_length)
        vk_api_utils.post_edit_with_add_media(
            post_id, edited_message, "photo")
        assert self.profile_form.is_message_present(edited_message), \
            "Edited message should be displayed"

        assert self.image_functions.is_images_equals(image_path, user_id,
                                                     post_id,
                                                     self.profile_form),\
            "Photo in UI and send API should be equals"
        comment_message = RandomText.get_randomize_text(
            self.min_randomize_string_length,
            self.max_randomize_string_length)
        vk_api_utils.add_comment(post_id, comment_message)
        assert self.profile_form.get_comment_user_name(user_id, post_id) == \
               user_name, "Comment user name should be equal page user name"
        self.profile_form.click_like_post_button(user_id, post_id)
        assert self.conditional_wait.wait_for(
                lambda: self.is_users_in_list([user_id], vk_api_utils.
                                              get_users_liked_post(user_id,
                                                                   post_id))), \
            "Likes should be from users"
        vk_api_utils.delete_post(post_id)
        assert self.profile_form.is_post_deleted(user_id, post_id), \
            "Post should be deleted"

    test_case_data = [(user_1_login, user_1_password, user_2_login,
                       user_2_password)]

    @pytest.mark.parametrize("user_1_login, user_1_password, user_2_login, "
                             "user_2_password", test_case_data)
    def test_user_first_create_second_like(self, user_1_login, user_1_password,
                                           user_2_login, user_2_password,
                                           before_after_test):
        Browser().open_url(TestSettings.URL_VK)
        assert self.login_form.is_opened(), \
            "Login card should be displayed"
        self.login_form.filling_login_page(user_1_login, user_1_password)

        assert self.news_form.is_opened(), \
            "News card should be displayed"

        user_1_id = self.news_form.get_user_id()
        vk_api_utils_user_1 = VkApiUtils(user_1_id, "User_1", None)

        self.news_form.click_my_page_button()

        assert self.profile_form.is_opened(), \
            "Profile card should be displayed"
        user_1_url = Browser.get_url()

        message = RandomText.get_randomize_text(
            self.min_randomize_string_length,
            self.max_randomize_string_length)
        post_id = vk_api_utils_user_1.create_post(message)
        self.profile_form.click_like_post_button(user_1_id, post_id)
        self.profile_form.logout()

        self.browser.open_url(TestSettings.URL_VK)
        assert self.login_form.is_opened(), \
            "Login card should be displayed"
        self.login_form.filling_login_page(user_2_login, user_2_password)

        news_form = NewsForm()
        assert news_form.is_opened(), "News card should be displayed"
        user_2_id = news_form.get_user_id()
        vk_api_utils_user_2 = VkApiUtils(user_2_id, "User_2", None)

        self.browser.open_url(user_1_url)

        assert self.profile_form.get_post_message(user_1_id, post_id) == \
               message, "Messages should be equals"
        self.profile_form.click_like_post_button(user_1_id, post_id)

        assert self.conditional_wait.wait_for(
            lambda: self.is_users_in_list(
                    [user_1_id, user_2_id], vk_api_utils_user_2.
                    get_users_liked_post(user_1_id, post_id))), \
            "Likes should be from users"

    test_case_data = [(user_1_login, user_1_password)]

    @pytest.mark.parametrize("user_login, user_password", test_case_data)
    def test_user_create_anonymous_control(self, user_login, user_password,
                                           before_after_test):
        Browser().open_url(TestSettings.URL_VK)
        assert self.login_form.is_opened(), \
            "Login card should be displayed"
        self.login_form.filling_login_page(user_login, user_password)

        assert self.news_form.is_opened(), \
            "News card should be displayed"

        user_id = self.news_form.get_user_id()
        vk_api_utils = VkApiUtils(user_id, "User_1", None)

        self.news_form.click_my_page_button()

        assert self.profile_form.is_opened(), \
            "Profile card should be displayed"
        user_url = Browser.get_url()

        message = RandomText.get_randomize_text(
            self.min_randomize_string_length,
            self.max_randomize_string_length)
        post_id = vk_api_utils.create_post(message)
        self.profile_form.logout()

        self.browser.open_url(TestSettings.URL_VK)

        self.browser.open_url(user_url)

        assert self.profile_form.get_post_message(user_id, post_id) == \
               message, "Messages should be equals"
        assert self.profile_form.is_quick_login_form_present(), \
            "Quick login form should be displayed"

    test_case_data = [(user_2_login, user_2_password)]

    @pytest.mark.parametrize("user_login, user_password", test_case_data)
    def test_user_add_text_file_and_like(self, user_login, user_password,
                                         before_after_test):
        Browser().open_url(TestSettings.URL_VK)
        assert self.login_form.is_opened(), \
            "Login card should be displayed"
        self.login_form.filling_login_page(user_login, user_password)

        user_id = self.news_form.get_user_id()
        vk_api_utils = VkApiUtils(user_id, "User_1", None)
        assert self.news_form.is_opened(), "News card should be displayed"
        self.news_form.click_my_page_button()

        assert self.profile_form.is_opened(), \
            "Profile card should be displayed"

        message = RandomText.get_randomize_text(
            self.min_randomize_string_length,
            self.max_randomize_string_length)
        post_id = vk_api_utils.create_post(message)
        user_name = self.profile_form.get_user_name()

        edited_message = RandomText.get_randomize_text(
            self.min_randomize_string_length,
            self.max_randomize_string_length)
        vk_api_utils.post_edit_with_add_media(
            post_id, edited_message, "doc")
        assert self.profile_form.is_message_present(edited_message), \
            "Edited message should be displayed"

        assert ManageTestData.get_param("UploadingDocName") == \
               self.profile_form.get_doc_name(user_id, post_id), \
               "Document names should be equals"
        comment_message = RandomText.get_randomize_text(
            self.min_randomize_string_length,
            self.max_randomize_string_length)
        vk_api_utils.add_comment(post_id, comment_message)
        assert self.profile_form.get_comment_user_name(user_id, post_id) == \
               user_name, "Comment user name should be equal page user name"
        self.profile_form.click_like_post_button(user_id, post_id)
        assert self.conditional_wait.wait_for(
            lambda: self.is_users_in_list(
                    [user_id], vk_api_utils.get_users_liked_post(
                       user_id, post_id))), "Likes should be from users"
        vk_api_utils.delete_post(post_id)
        assert self.profile_form.is_post_deleted(user_id, post_id), \
            "Post should be deleted"

    test_case_data = [(user_2_login, user_2_password, image_png),
                      (user_2_login, user_2_password, image_jpg)]

    @pytest.mark.parametrize("user_login, user_password, image_path",
                             test_case_data)
    def test_user_add_message_and_photo(self, user_login, user_password,
                                        image_path, before_after_test):
        Browser().open_url(TestSettings.URL_VK)
        assert self.login_form.is_opened(), \
            "Login card should be displayed"
        self.login_form.filling_login_page(user_login, user_password)

        user_id = self.news_form.get_user_id()
        vk_api_utils = VkApiUtils(user_id, "User_1", image_path)
        assert self.news_form.is_opened(), "News card should be displayed"
        self.news_form.click_my_page_button()

        assert self.profile_form.is_opened(), \
            "Profile card should be displayed"

        message = RandomText.get_randomize_text(
            self.min_randomize_string_length,
            self.max_randomize_string_length)
        post_id = vk_api_utils.create_post_with_add_media(message, "photo")
        assert self.profile_form.is_message_present(message), \
            "Edited message should be displayed"

        assert self.image_functions.is_images_equals(image_path, user_id,
                                                     post_id,
                                                     self.profile_form), \
            "Photo in UI and send API should be equals"

    @staticmethod
    def is_users_in_list(list_users, list_obj):
        return set(list_users).issubset(list_obj.values)

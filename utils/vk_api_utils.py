from utils.manage_test_data import ManageTestData
from project.resources.constains.test_settings import TestSettings
from utils.api_requests import APIRequest


class VkApiUtils:
    def __init__(self, user_id, user_name, photo_path):
        self.user_id = user_id
        self.user = user_name
        self.uploading_photo_path = photo_path

    _create_post_method = "wall.post"
    _save_uploaded_photo_method = "photos.saveWallPhoto"
    _save_uploaded_doc_method = "docs.save"
    _edit_post_method = "wall.edit"
    _create_comment_method = "wall.createComment"
    _post_info_method = "wall.getById"
    _delete_post_method = "wall.delete"
    _delete_photo_method = "photos.delete"
    _likes_get_list_method = "likes.getList"

    @staticmethod
    def _upload_server_method(content_type):
        return content_type + ".getWallUploadServer"

    @staticmethod
    def _upload_server_url(url):
        return url["response"]["upload_url"]

    def create_post(self, message):
        return self.get_vk(self._create_post_method,
                           message=message)["response"]["post_id"]

    def create_post_with_add_media(self, message, media_type):
        uploaded_media = None
        match media_type:
            case "photo": uploaded_media = self.save_uploaded_photo()
        if media_type is not None:
            post_id = self.get_vk(self._create_post_method, message=message,
                                  attachments=f"{media_type}{self.user_id}"
                                  f"{uploaded_media['response'][0]['id']}")
        else:
            post_id = self.get_vk(self._create_post_method, message=message)

        return post_id["response"]["post_id"]

    def get_upload_server(self, content_type):
        return self.get_vk(self._upload_server_method(content_type),
                           user_id=self.user_id)

    def send_file_on_server(self, content_type, path_file):
        return self.post_vk(self._upload_server_url(self.get_upload_server(
            content_type)), path_file)

    def save_uploaded_photo(self):
        url = self.send_file_on_server('photos', self.uploading_photo_path)
        return self.get_vk(self._save_uploaded_photo_method,
                           user_id=self.user_id, server=f"{url['server']}",
                           photo=f"{url['photo']}", hash=f"{url['hash']}")

    def save_uploaded_doc(self):
        return self.get_vk(self._save_uploaded_doc_method,
                           file=self.send_file_on_server("docs",
                                ManageTestData.get_param("UploadingDocPath")
                                                         )['file'])

    def post_edit_with_add_media(self, post_id, message, media_type):
        uploaded_media = None
        match media_type:
            case "photo":
                uploaded_media = self.save_uploaded_photo()
            case "doc":
                uploaded_media = self.save_uploaded_doc()
        param = 0
        match media_type:
            case "doc": param = 'doc'
        self.get_vk(self._edit_post_method, owner_id=self.user_id,
                    post_id=post_id, message=message,
                    attachments=f"{media_type}{self.user_id}"
                                f"{uploaded_media['response'][param]['id']}")

    def add_comment(self, post_id, message):
        return self.get_vk(self._create_comment_method, owner_id=self.user_id,
                           post_id=post_id, message=message)

    def delete_post(self, post_id):
        self.get_vk(self._delete_post_method, owner_id=self.user_id,
                    post_id=post_id)

    def get_users_liked_post(self, user_id, post_id):
        return (self.get_vk(self._likes_get_list_method, type="post",
                            owner_id=user_id, item_id=post_id)
                ["response"]["items"])

    def get_vk(self, method, **params):
        params["token"] = ManageTestData.get_param(user + "_token")
        params["v"] = TestSettings.VERSION_API
        response = APIRequest.get_api(f"{TestSettings.URI_API_VK}{method}",
                                      params=params)
        self.error_analyse(response)
        return response

    def post_vk(self, url, path_file):
        response = APIRequest.post_file_api(url, path_file)
        self.error_analyse(response)
        return response

    @staticmethod
    def error_analyse(response):
        if "error" in response:
            print("Error")
            raise APIVKRequestException(
                "Receive error in API request. Response: Error code:"
                f"{response['error']['error_code']}. Error message: "
                f"{response['error']['error_msg']}")


class APIVKRequestException(Exception):
    def __init__(self, text):
        self.txt = text

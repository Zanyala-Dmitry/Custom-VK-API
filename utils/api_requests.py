import requests


class APIRequest:
    @staticmethod
    def get_api(url, params=None):
        return requests.get(url, params).json()

    @staticmethod
    def post_file_api(url, path_file, params=None):
        files = {'file': open(path_file, 'rb')}
        return requests.post(url, params, files=files).json()

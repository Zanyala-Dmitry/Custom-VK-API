import cv2


class ImageFunctions:
    @staticmethod
    def get_image_hash(image):

        resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        avg = gray_image.mean()
        ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)

        _hash = ""
        for x in range(8):
            for y in range(8):
                val = threshold_image[x, y]
                _hash = _hash + "1" if val == 255 else _hash + '0'
        return _hash

    @staticmethod
    def get_hashes_difference(hash_1, hash_2):
        k = len(hash_1)
        i = 0
        count = 0
        while i < k:
            if hash_1[i] != hash_2[i]:
                count = count + 1
            i = i + 1
        return count

    def is_images_equals(self, image_file, user_id, post_id, profile_form):
        image_1 = cv2.imread(image_file)
        hash_image_1 = self.get_image_hash(image_1)

        np_arr = np.frombuffer(profile_form.get_image_screenshot(user_id,
                                                                 post_id),
                               np.uint8)
        image_2 = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        hash_image_2 = self.get_image_hash(image_2)

        result = self.get_hashes_difference(hash_image_1, hash_image_2)
        return result < 11

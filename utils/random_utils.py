import random
import string


class RandomText:
    @staticmethod
    def get_randomize_text(min_length, max_length):
        length = random.randint(min_length, max_length)
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.sample(letters_and_digits, length))

import random
import string

import bcrypt


def generate_user_code() -> str:
    """
    Generate user code for new session
    Returns
    -------
    user_code (str): a code with 6 chars
    """
    chars = []
    upper_letters = string.ascii_uppercase
    lower_letters = string.ascii_lowercase
    numbers = list(range(1, 9))
    upper_sample = random.sample(upper_letters, 2)
    lower_sample = random.sample(lower_letters, 2)
    number_sample = random.sample(numbers, 2)

    chars.extend(number_sample)
    chars.extend(lower_sample)
    chars.extend(upper_sample)

    random.shuffle(chars)

    user_code = ''.join([str(char) for char in chars])

    return user_code


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

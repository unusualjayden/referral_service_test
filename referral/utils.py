import string
from random import choice


def generate_fake_sms_code(n=4):
    """Функция генерирующая фейковый смс-код для аутентификации"""
    return ''.join(choice(string.digits) for _ in range(n))

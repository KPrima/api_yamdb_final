import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Нельзя использовать "me" в качестве логина!')
    if not re.match(r'^[\w@.+-_]+\Z', value):
        raise ValidationError(
            'Логин может содержать только буквы, цифры и символы @.+-_'
        )
    return value

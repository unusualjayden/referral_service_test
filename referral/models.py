import string
from random import choice

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель юзера с телефоном и инвайт-кодом"""

    username = models.CharField(max_length=256, null=True)
    phone = models.CharField('phone_number', max_length=15, unique=True)
    invite_code = models.CharField(max_length=6,
                                   default='XXXXXX',
                                   unique=True,
                                   editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    referrer = models.ForeignKey('self',
                                 on_delete=models.CASCADE,
                                 default=None,
                                 null=True)
    USERNAME_FIELD = 'phone'

    def __str__(self):
        return f'ID - {self.id} Phone - {self.phone} Invite code - {self.invite_code} Referrer - {self.referrer_id}'

    def get_formatted_phone_number(self):
        """Метод для получения форматированного телефона"""
        return f'+7{self.phone}'

    def create_invite_code(self, n=6):
        """Метод создающий инвайт-код"""
        invite_code = ''.join(
            choice(string.ascii_uppercase + string.digits) for _ in range(n))
        try:
            CustomUser.objects.get(invite_code=invite_code)
            return self.create_invite_code()
        except CustomUser.DoesNotExist:
            return invite_code

    def save(self, *args, **kwargs):
        self.invite_code = self.create_invite_code()
        super(CustomUser, self).save(*args, **kwargs)

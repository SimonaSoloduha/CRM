import random

from account.auth_backends import User
from django.db import models
from django.utils.translation import gettext_lazy as _


def generate_code():
    random.seed()
    return str(random.randint(10000, 99999))


class Code(models.Model):
    number = models.CharField(max_length=5, blank=True, verbose_name=_('number'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))

    class Meta:
        verbose_name_plural = _('code')
        verbose_name = _('codes')

    def save(self, *args, **kwargs):
        code = generate_code()
        self.number = code
        super().save(*args, **kwargs)

    def __str__(self):
        return self.number

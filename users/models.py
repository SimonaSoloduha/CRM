import random

from account.auth_backends import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from companies.models import Company

STATUS_NOT_HAVE_IN_DB = 'NOT HAVE IN DB'
STATUS_USER_BAN = 'USER BAN'
STATUS_DEVICE_BANNED = 'DEVICE BANNED'
STATUS_RETRY_USER = 'RETRY USER'
STATUS_VIRTUAL_DEVICE = 'VIRTUAL DEVICE'
STATUS_STOP_TIME_ZONE = 'STOP TIME ZONE'
STATUS_STOP_MCHECKER = 'STOP MCHECKER'


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


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
    usser_id = models.CharField(max_length=155, verbose_name=_('usser_id'))
    сompany = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, verbose_name=_('сompany'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))
    STATUS_CHOICES = [
        (STATUS_NOT_HAVE_IN_DB, STATUS_NOT_HAVE_IN_DB),
        (STATUS_USER_BAN, STATUS_USER_BAN),
        (STATUS_DEVICE_BANNED, STATUS_DEVICE_BANNED),
        (STATUS_RETRY_USER, STATUS_RETRY_USER),
        (STATUS_VIRTUAL_DEVICE, STATUS_VIRTUAL_DEVICE),
        (STATUS_STOP_TIME_ZONE, STATUS_STOP_TIME_ZONE),
        (STATUS_STOP_MCHECKER, STATUS_STOP_MCHECKER),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name=_('status'),
        blank=True,
    )

    class Meta:
        verbose_name_plural = _('client')
        verbose_name = _('clients')

    def __str__(self):
        return self.usser_id

from django.db import models
from django.utils.translation import gettext_lazy as _

from countries.models import Country
from users.models import Client, STATUS_NOT_HAVE_IN_DB, STATUS_USER_BAN, STATUS_DEVICE_BANNED, STATUS_RETRY_USER, \
    STATUS_VIRTUAL_DEVICE, STATUS_STOP_TIME_ZONE, STATUS_STOP_MCHECKER


class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    ip = models.CharField(max_length=100, blank=True, verbose_name=_('ip'))
    getz_user = models.CharField(max_length=100, verbose_name=_('getz'))
    getr_user = models.CharField(max_length=255, verbose_name=_('getr'))
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name=_('country'))
    domen = models.CharField(max_length=255, verbose_name=_('domen'))
    packege_id = models.CharField(max_length=255, verbose_name=_('packege_id'))
    usser_id = models.CharField(max_length=255, verbose_name=_('usser_id'))
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, verbose_name=_('client'))
    utm_medium = models.CharField(max_length=255, default='organic', verbose_name=_('utm_medium'))
    user_agent = models.CharField(max_length=255, verbose_name=_('user_agent'))
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
    FILTER_ONE_CHOICES = [
        ('Stop TimeZone', 'Stop TimeZone'),
        ('SUCCESSFUL', 'SUCCESSFUL'),
    ]
    filter_one_time_zone = models.CharField(
        max_length=20,
        choices=FILTER_ONE_CHOICES,
        verbose_name=_('filter_one_time_zone'),
        blank=True,
    )
    FILTER_TWO_CHOICES = [
        ('Stop Mchecker', 'Stop Mchecker'),
        ('SUCCESSFUL', 'SUCCESSFUL'),
    ]
    filter_two_cheker = models.CharField(
        max_length=20,
        choices=FILTER_TWO_CHOICES,
        verbose_name=_('filter_two_cheker'),
        blank=True,
    )
    final = models.BooleanField(default=False, verbose_name=_('final'))

    class Meta:
        verbose_name_plural = _('log')
        verbose_name = _('logs')

    def __str__(self):
        return self.usser_id

from django.db import models
from django.utils.translation import gettext_lazy as _

from countries.models import Country


class Company(models.Model):
    name = models.CharField(max_length=155, verbose_name=_('name'))
    domen = models.CharField(max_length=155, verbose_name=_('domen'))
    url_response = models.CharField(max_length=155, blank=True, verbose_name=_('url_response'))
    notificator = models.CharField(max_length=255, blank=True, verbose_name=_('notificator'))
    countries = models.ManyToManyField(Country, verbose_name=_('countries'), related_name='company')
    active_filter_one_time_zone = models.BooleanField(default=False, verbose_name=_('active_filter_one_time_zone'))
    filter_two_cheker = models.BooleanField(default=False, verbose_name=_('active_filter_one_time_zone'))

    class Meta:
        verbose_name_plural = _('company')
        verbose_name = _('companies')

    def __str__(self):
        return self.name

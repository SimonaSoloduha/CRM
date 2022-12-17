from django.db import models
from django.utils.translation import gettext_lazy as _

from countries.models import Country


class Company(models.Model):
    name = models.CharField(max_length=155, verbose_name=_('name'))
    domen = models.CharField(max_length=155, verbose_name=_('domen'))
    notificator = models.CharField(max_length=155, verbose_name=_('notificator'))
    countries = models.ManyToManyField(Country, verbose_name=_('countries'), related_name='company')

    class Meta:
        verbose_name_plural = _('company')
        verbose_name = _('companies')

    def __str__(self):
        return self.name

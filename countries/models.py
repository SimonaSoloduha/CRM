from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('country'))
    time_zones = models.TextField(verbose_name=_('time_zones'))
    is_active = models.BooleanField(default=True, verbose_name=_('is_active'))

    class Meta:
        verbose_name_plural = _('time_zone')
        verbose_name = _('time_zones')

    def __str__(self):
        return self.name

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    class Meta:
        verbose_name_plural = _('company')
        verbose_name = _('companies')

    def __str__(self):
        return self.name

    def get_logs(self):
        return self.logs.all()

    def get_logs_count(self):
        return self.get_logs().count()

    def get_logs_successful_count(self):
        return self.get_logs().filter(final=True).count()

    def get_logs_successful_filter_1_count(self):
        from logs.models import STATUS_SUCCESSFUL
        return self.get_logs().filter(filter_one_time_zone=STATUS_SUCCESSFUL).count()

    def get_logs_successful_filter_2_count(self):
        from logs.models import STATUS_SUCCESSFUL
        return self.get_logs().filter(filter_two_cheker=STATUS_SUCCESSFUL).count()

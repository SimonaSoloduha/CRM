from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateTimeRangeFilter
from import_export.fields import Field
from django_admin_listfilter_dropdown.filters import (ChoiceDropdownFilter)
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.filters import BooleanFieldListFilter
from logs.models import Log


class LogResource(resources.ModelResource):
    created_at = Field()
    ip = Field(attribute='ip', column_name=_('ip'))
    country = Field(attribute='country', column_name=_('country'))
    getz_user = Field(attribute='getz_user', column_name=_('getz_user'))
    user_agent = Field(attribute='user_agent', column_name=_('user_agent'))
    usser_id = Field(attribute='usser_id', column_name=_('usser_id'))
    status = Field(attribute='status', column_name=_('status'))
    filter_one_time_zone = Field(attribute='filter_one_time_zone', column_name=_('Filter 1'))
    filter_two_cheker = Field(attribute='filter_two_cheker', column_name=_('Filter 2'))
    final = Field(attribute='final', column_name=_('final'))

    class Meta:
        model = Log
        fields = ('get_created_at',
                  'ip',
                  'country',
                  'getz_user',
                  'user_agent',
                  'usser_id',
                  'status',
                  'filter_one_time_zone',
                  'filter_two_cheker',
                  'final')

        def dehydrate_created_at(self, log):
            return f'{log.created_at.strftime("%m/%d/%Y, %H:%M:%S")}'


class FinalFilter(BooleanFieldListFilter):
    template = 'log/filter_log.html'


class LogAdmin(ImportExportModelAdmin):
    list_display = ('get_created_at',
                    'ip',
                    'country',
                    'getz_user',
                    'get_headers',
                    'usser_id',
                    'status',
                    'detail_status',
                    'filter_one_time_zone',
                    'filter_two_cheker',
                    'final')

    change_list_template = "log/change_list_log.html"
    actions = None
    list_per_page = 50
    resource_classes = [LogResource]
    search_fields = ('ip',)
    list_filter = (
        ('created_at', DateTimeRangeFilter),
        ('filter_one_time_zone', ChoiceDropdownFilter),
        ('filter_two_cheker', ChoiceDropdownFilter),
        ('final', FinalFilter),
    )

    def get_rangefilter_created_at_title(self, request, field_path):
        return _('Created: ')

    def get_headers(self, object):
        return f'{object.user_agent.split(" ")[0]}'

    def get_created_at(self, object):
        return f'{object.created_at.strftime("%m/%d/%Y, %H:%M:%S")}'

    get_created_at.short_description = 'Date'
    get_headers.short_description = 'Headers'

    class Media:
        js = ("js/logs/pagination.js",)

    def changelist_view(self, request, extra_context=None):
        try:
            page_param = int(request.GET['e'])
            self.list_per_page = page_param
        except Exception:
            pass
        return super(LogAdmin, self).changelist_view(request, extra_context)


admin.site.register(Log, LogAdmin)

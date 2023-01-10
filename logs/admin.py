from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from logs.models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = ('get_created_at', 'ip', 'country', 'getz_user', 'get_headers',
                    'usser_id', 'status', 'detail_status', 'filter_one_time_zone', 'filter_two_cheker', 'final')
    search_fields = ('ip',)
    # list_filter = ('filter_one_time_zone', 'filter_two_cheker', 'company', ('created_at', DateFieldListFilter))
    actions = None
    list_per_page = 50

    def get_headers(self, object):
        return f'{object.user_agent.split(" ")[0]}'

    def get_created_at(self, object):
        return f'{object.created_at.strftime("%m/%d/%Y, %H:%M:%S")}'

    get_created_at.short_description = 'Date'
    get_headers.short_description = 'Headers'


admin.site.register(Log, LogAdmin)

from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from logs.models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'ip', 'county', 'getz_user', 'get_headers',
                    'usser_id', 'status', 'filter_one_time_zone', 'filter_two_cheker', 'final')
    search_fields = ('ip',)
    list_filter = ('filter_one_time_zone', 'filter_two_cheker', ('created_at', DateFieldListFilter))

    def get_headers(self, object):
        return f'{object.user_agent.split(" ")[0]}'

    get_headers.short_description = 'Headers'


admin.site.register(Log, LogAdmin)

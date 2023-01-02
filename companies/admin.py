from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db import models
from django.forms import TextInput, CheckboxSelectMultiple
from companies.models import Company


def get_percent(count_all, count_true):
    percent = 0
    if count_all and count_true:
        percent = (count_true / count_all) * 100
    return f'{count_true} / {round(percent, 2)}%'


class CompanyAdmin(admin.ModelAdmin):

    @staticmethod
    def count_requests(obj):
        return obj.get_logs_count()

    @staticmethod
    def count_successful_requests(obj):
        return obj.get_logs_successful_count()

    @staticmethod
    def count_successful_filter_1(obj):
        count_all = obj.get_logs_count()
        count_true = obj.get_logs_successful_filter_1_count()
        return get_percent(count_all, count_true)

    @staticmethod
    def count_successful_filter_2(obj):
        count_all = obj.get_logs_count()
        count_true = obj.get_logs_successful_filter_2_count()
        return get_percent(count_all, count_true)

    @staticmethod
    def control_panel(obj):
        return format_html(
            '<a class="fixlink tablelink" href="/admin/companies/company/{}/change/"></a><a class="deletelink tablelink" '
            'href="/admin/companies/company/{}/delete/"></a><a class="duplicatelink tablelink" href="/duplicate/{'
            '}/"></a>', obj.id, obj.id, obj.id)

    list_display = ('name',
                    'domen',
                    'count_requests',
                    'count_successful_requests',
                    'count_successful_filter_1',
                    'count_successful_filter_2',
                    'control_panel')
    change_form_template = "company/change_form_company.html"
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 50})},
        models.ManyToManyField: {'widget': CheckboxSelectMultiple(attrs={'class': 'checkbox-countries'})}
    }

    fieldsets = (
        (_('Info'), {'fields': (tuple([
            'name',
            'domen',
        ]),
        )}
         ),
        (_('Countries'), {'fields': (
            'countries',
        )}
         ),
        (_('Active filters'), {'fields': (tuple([
            'active_filter_one_time_zone',
            'filter_two_cheker',
        ]),
        )}),
    )
    list_display_links = ('name',)
    actions = None
    search_fields = ('name', 'domen',)


admin.site.register(Company, CompanyAdmin)

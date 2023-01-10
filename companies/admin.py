from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db import models
from django.forms import TextInput, CheckboxSelectMultiple
from companies.models import Company
from import_export.admin import ImportExportModelAdmin

from rangefilter.filters import DateRangeFilter
from import_export import resources
from import_export.fields import Field

from companies.utils import get_percent


class CompanyResource(resources.ModelResource):
    name = Field(attribute='name', column_name='Название')
    domen = Field(attribute='domen', column_name='Домен')
    count_requests = Field(column_name='Количество запросов')
    count_successful_requests = Field(column_name='Количество успешных запросов')
    count_successful_filter_1 = Field(column_name='Количество прошедших фильтр 1')
    count_successful_filter_2 = Field(column_name='Количество прошедших фильтр 2')

    class Meta:
        model = Company
        fields = ('name',
                  'domen',
                  'count_requests',
                  'count_successful_requests',
                  'count_successful_filter_1',
                  'count_successful_filter_2',)

    def dehydrate_count_requests(self, company):
        return company.get_logs_count()

    def dehydrate_count_successful_requests(self, company):
        return company.get_logs_successful_count()

    def dehydrate_count_successful_filter_1(self, company):
        count_all = company.get_logs_count()
        count_true = company.get_logs_successful_filter_1_count()
        return get_percent(count_all, count_true)

    def dehydrate_count_successful_filter_2(self, company):
        count_all = company.get_logs_count()
        count_true = company.get_logs_successful_filter_2_count()
        return get_percent(count_all, count_true)


class CompanyAdmin(ImportExportModelAdmin):

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
            '}/"></a><a class="loglink tablelink" href="/admin/logs/log/?company__id__exact={}"></a>',
            obj.id, obj.id, obj.id, obj.id, )

    list_display = ('name',
                    'domen',
                    'count_requests',
                    'count_successful_requests',
                    'count_successful_filter_1',
                    'count_successful_filter_2',
                    'control_panel')
    change_form_template = "company/change_form_company.html"
    change_list_template = "company/change_list_company.html"
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
    list_per_page = 50
    actions = None
    search_fields = ('name', 'domen',)
    list_filter = (
        ('created_at', DateRangeFilter),
    )

    resource_classes = [CompanyResource]

    class Media:
        js = ("js/company/pagination.js",)

    def changelist_view(self, request, extra_context=None):
        try:
            page_param = int(request.GET['e'])
            self.list_per_page = page_param
        except Exception:
            pass
        return super(CompanyAdmin, self).changelist_view(request, extra_context)


admin.site.register(Company, CompanyAdmin)

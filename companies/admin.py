from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db import models
from django.forms import TextInput, CheckboxSelectMultiple
from companies.models import Company


class CompanyAdmin(admin.ModelAdmin):

    def count_appeals(self, obj):
        return f'пока нет обращений'

    def count_passed(self, obj):
        return f'пока нет удачных обращений'

    def count_failed_filter_1(self, obj):
        return f'нет не прошедших фильтр 1'

    def count_failed_filter_2(self, obj):
        return f'нет не прошедших фильтр 2'

    def control_panel(self, obj):
        return format_html(
            '<a class="fixlink tablelink" href="/admin/companies/company/{}/change/"></a><a class="deletelink tablelink" '
            'href="/admin/companies/company/{}/delete/"></a><a class="duplicatelink tablelink" href="/duplicate/{'
            '}/"></a>', obj.id, obj.id, obj.id)

    list_display = ('name', 'domen', 'count_appeals', 'count_passed', 'count_failed_filter_1', 'count_failed_filter_2',
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

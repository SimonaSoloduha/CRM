from django.contrib import admin

from companies.models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'domen', 'notificator')


admin.site.register(Company, CompanyAdmin)

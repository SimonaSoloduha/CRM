from django.contrib import admin

from countries.models import Country


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_zones', 'is_active')


admin.site.register(Country, CountryAdmin)

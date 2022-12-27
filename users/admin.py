from django.contrib import admin

from users.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'usser_id', 'status')
    actions = None

    # def has_add_permission(self, request, obj=None):
    #     return False


admin.site.register(Client, ClientAdmin)

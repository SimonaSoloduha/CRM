"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from django.urls import path, include

from account.models import Account, AccountDeletion, EmailAddress, PasswordExpiry, \
    PasswordHistory, SignupCode

from countries.models import Country

urlpatterns = [
    path('', include('companies.urls')),
    path('', include('users.urls')),
    path('', include('logs.urls')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = 'CRM'
admin.site.site_header = 'CRM'
admin.site.index_title = 'CRM'
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Country)
admin.site.unregister(Account)
admin.site.unregister(AccountDeletion)
admin.site.unregister(EmailAddress)
admin.site.unregister(PasswordExpiry)
admin.site.unregister(PasswordHistory)
admin.site.unregister(SignupCode)
admin.site.unregister(Site)

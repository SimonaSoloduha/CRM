from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from users.views import auth_view, verify_view

urlpatterns = [
    path('admin/login/', auth_view, name='login_view'),
    path('verify/', verify_view, name='verify_view'),
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
]

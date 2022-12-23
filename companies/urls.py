from django.urls import path
from companies.views import add_duplicate

app_name = 'companies'

urlpatterns = [
    path('duplicate/<int:pk>/', add_duplicate, name="add_duplicate"),
]

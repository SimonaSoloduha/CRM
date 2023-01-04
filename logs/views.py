from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from logs.models import Log
from logs.serializers import LogSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, redirect


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class LogViewSet(viewsets.ModelViewSet):
    """
    API для простмотра и добавления логов
    """
    queryset = Log.objects.all().order_by('-created_at')
    serializer_class = LogSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


def check_view(request):
    req_test_url = 'https://shrouded-ravine-59969.herokuapp.com/index_test.php'
    response = redirect(req_test_url)
    print(response)
    return redirect('/admin/companies/company/')

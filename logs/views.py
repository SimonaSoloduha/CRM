from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from logs.models import Log
from logs.serializers import LogSerializer
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'


class LogViewSet(viewsets.ModelViewSet):
    """
    API для простмотра и добавления логов
    """
    queryset = Log.objects.all().order_by('-created_at')
    serializer_class = LogSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

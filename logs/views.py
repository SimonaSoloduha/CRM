from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from logs.models import Log
from logs.serializers import LogSerializer


class LogViewSet(viewsets.ModelViewSet):
    """
    API для простмотра и добавления логов
    """
    queryset = Log.objects.all().order_by('-created_at')
    serializer_class = LogSerializer

    # def list(self, request, *args, **kwargs):
    #     # print('!!!  request', request.headers.get('User-Agent'))
    #     user_agent = request.META.get('HTTP_USER_AGENT')
    #     return super().list(request, *args, **kwargs)

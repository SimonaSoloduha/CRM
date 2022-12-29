from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from logs.models import Log
from logs.serializers import LogSerializer


class LogViewSet(viewsets.ModelViewSet):
    """
    API для простмотра и добавления логов
    """
    queryset = Log.objects.all().order_by('-created_at')
    serializer_class = LogSerializer
    permission_classes = [AllowAny]

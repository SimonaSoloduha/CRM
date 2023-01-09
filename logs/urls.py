from django.urls import include, path
from rest_framework import routers

from logs.views import LogViewSet, LogsUpdateView

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('logs/', LogViewSet.as_view(), name='logs'),
    path('checker/', LogsUpdateView.as_view(), name='checker'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

from django.urls import include, path
from rest_framework import routers

from logs.views import LogViewSet, check

router = routers.DefaultRouter()
router.register(r'logs', LogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('check/', check, name='check'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

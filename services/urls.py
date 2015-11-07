from django.conf.urls import include, url
from rest_framework import routers
from services.views import *

router = routers.DefaultRouter()
router.register(r'tracking', TrackingViewSet, base_name='api-tracking')
router.register(r'history', HistoryViewSet, base_name='api-history')
router.register(r'path', PathViewSet, base_name='api-path')

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
from this import d
from xml.etree.ElementInclude import include
from django.urls import path, include
from .views import UserViewSet, generateFakeUsers
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('users/?', UserViewSet)

urlpatterns = [
    path('ingestfake/', generateFakeUsers),
    path('', include(router.urls)),
]

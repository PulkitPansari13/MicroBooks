from django.urls import path, include
from .views import ContentView, ContentListView, ingestFakeContent
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('books/?', ContentView, basename='books')


urlpatterns = [
    path('ingestfake/', ingestFakeContent),
    path('books/latest', ContentListView.as_view(), kwargs={"list_type":"latest"}),
    path('books/top', ContentListView.as_view(), kwargs={"list_type":"top"}),
    path('', include(router.urls)),
]

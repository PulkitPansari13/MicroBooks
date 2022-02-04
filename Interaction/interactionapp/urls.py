from django.urls import path, include
from .views import LikeView, ReadView, generateFakeInteraction


urlpatterns = [
    path('book/<int:bookid>/like', LikeView.as_view()),
    path('book/<int:bookid>/read', ReadView.as_view()),
]

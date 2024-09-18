from django.urls import path
from photos.views import PhotoView

urlpatterns = [
    path('chapter-1.jpg', PhotoView.as_view()),
]

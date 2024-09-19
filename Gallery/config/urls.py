from django.urls import path
from photos.views import PhotoView
from photos.views import PhotoListView

urlpatterns = [
    path('<str:name>', PhotoView.as_view()),
    path('', PhotoListView.as_view()),
]

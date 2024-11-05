from django.urls import path, include
from hero.views import HeroCreateView, HeroDeleteView, HeroDetailView, HeroListView, HeroUpdateView, SignUpView, DocumentView, PageView
from django.contrib import admin

urlpatterns = [

    # Hero
    path('hero/',                HeroListView.as_view(),    name='hero_list'),
    path('hero/<int:pk>',        HeroDetailView.as_view(),  name='hero_detail'),
    path('hero/add',             HeroCreateView.as_view(),  name='hero_add'),
    path('hero/<int:pk>/',       HeroUpdateView.as_view(),  name='hero_edit'),
    path('hero/<int:pk>/delete', HeroDeleteView.as_view(),  name='hero_delete'),

    # Login/Logout code
    path('accounts/', include('django.contrib.auth.urls')),

    # Admin views for users
    path('admin/', admin.site.urls),
    # path('admin/', include('admin.site.urls')),   Don't do this!

    # User Accounts
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),

    path('doc/<str:doc>', DocumentView.as_view()),
    path('<str:page>.html', PageView.as_view()),
    path('<str:doc>.md', DocumentView.as_view()),
]
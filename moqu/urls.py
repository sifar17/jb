from django.urls import path, include
from . import views

app_name = 'moqu'

urlpatterns = [
    path('moqu/', views.moquHome, name = 'home'),
    path('moqu/about/', views.moquAbout, name = 'about'),
    path('moqu/api/', views.moquApi, name = 'apiAbout'),
    path('moqu/<int:pk>/', views.moquHome, name = 'quotePage'),

    path('moqu/', include('moqu.api.urls', namespace = 'api')),
]
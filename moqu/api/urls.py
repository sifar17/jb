from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Creating Router Object
router = DefaultRouter()

app_name = 'api'

# Register MovieViewSet & QuoteViewSet with Router
router.register('categories', views.CategoryViewSet, basename = 'category')
router.register('movies', views.MovieViewSet, basename = 'movie')
router.register('quotes', views.QuoteViewSet, basename = 'quote')

urlpatterns = [
    path('api-room/', include(router.urls))
]

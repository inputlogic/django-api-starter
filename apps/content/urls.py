from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()


router.register('content', views.ContentViewSet, 'Content')

urlpatterns = [
    path('api/content/', include(router.urls))
]

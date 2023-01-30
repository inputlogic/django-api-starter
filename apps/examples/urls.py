from django.urls import path

from . import views


urlpatterns = [
    path('examples/html-array', views.HTMLArray.as_view(), name='examples-html-array'),
]

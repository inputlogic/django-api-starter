from django.urls import path

from . import views


urlpatterns = [
    path('work', views.WorkList.as_view(), name='work-list'),
    path('work/<int:pk>', views.WorkDetail.as_view(), name='work'),
    path('pages', views.PageList.as_view(), name='page-list'),
    path('pages/<int:pk>', views.PageDetail.as_view(), name='page'),
]

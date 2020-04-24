from django.urls import path

from . import views


urlpatterns = [
    path('posts', views.PostList.as_view(), name='post-list'),
    path('posts/<int:pk>', views.PostDetail.as_view(), name='post'),
    path('pages', views.PageList.as_view(), name='page-list'),
    path('pages/<int:pk>', views.PageDetail.as_view(), name='page'),
]

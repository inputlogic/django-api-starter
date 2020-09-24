from django.urls import path

from . import views


urlpatterns = [
    path('create-signed-file', views.CreateSignedFile.as_view(), name='create-signed-file'),
    path('files', views.UploadFile.as_view(), name='upload-file'),
    path('files/<int:pk>', views.FileDetail.as_view(), name='file-detail'),
]

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^firebase/$',
        views.FirebaseListCreate.as_view(),
        name='firebase-list-create'),

    url(r'^firebase/(?P<registration_id>[^\/]+)$',
        views.FirebaseDestroy.as_view(),
        name='firebase-destroy'),
]

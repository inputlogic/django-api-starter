from django.urls import path

from .endpoints import TemplateCreate


urlpatterns = [
    path('mail/templates', TemplateCreate.as_view(), name='template-create')
]

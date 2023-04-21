from django.db import models
from django.urls import path
from django_mock_queries.query import MockSet, MockModel
from django_filters import rest_framework
import json
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import Serializer
from rest_framework import generics, mixins, serializers


f = open('./libs/access/access_file.json')
data = json.load(f)
PATH_PREFIX = 'access'


def mock_fields(fields):
    mockers = {
        'string': lambda: 'Foo Bar',
        'number': lambda: 3,
        'datetime': lambda: datetime.now(),
    }
    return {k: mockers.get(v, lambda: 'default')() for (k, v) in fields.items()}


def access_to_drf(access, code):
    access = data
    urlpatterns = []
    for (role, resources) in access.items():
        for resource in resources:
            urlpatterns += build_resource(resource, role)
    return urlpatterns


def build_resource(resource, role):
    name = resource['name']
    crud = resource.get('crud', None)
    procedure = resource.get('procedure', None)
    urlpatterns = []
    if crud:
        create = crud.get('create', None)
        read = crud.get('read', None)
        update = crud.get('update', None)
        delete = crud.get('delete', None) # TODO: change to delete
        serializers = create_crud_serializers(resource, role)
        views = create_crud_views(resource, role, serializers)
        urlpatterns = urlpatterns + views
    return urlpatterns


# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAdminUser]

#     def list(self, request):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)


def create_crud_serializers(resource, role):
    resource_name = resource['name']
    crud = resource.get('crud', {})
    return {
        'read': create_serializer(role, resource_name, 'read', crud.get('read', {}).get('fields', {})),
        'create': create_serializer(role, resource_name, 'create', crud.get('update', {}).get('fields', {})),
        'update': create_serializer(role, resource_name, 'update', crud.get('update', {}).get('fields', {})),
    }

def create_serializer(role, name, method, fields):
    return type(
        f'{role.title()}{name.title()}{method.title()}Serializer',
        (Serializer,),
        {**get_serializer_fields(fields)}
    )

def get_serializer_fields(fields):
    defaults = {
        'string': serializers.CharField(),
        'number': serializers.IntegerField(),
        'datetime': serializers.DateTimeField(),
        'user': serializers.CharField(),
    }
    return {k: defaults.get(v, serializers.CharField()) for (k, v) in fields.items()}

def create_crud_views(resource, role, serializers):
    name = resource['name']
    crud = resource.get('crud', {})
    read = crud.get('read', None)
    create = crud.get('create', None)
    update = crud.get('update', None)
    delete = crud.get('delete', None)
    patterns = []

    list_classes = (
        *([mixins.ListModelMixin] if read else []),
        *([mixins.CreateModelMixin] if update else []),
        generics.GenericAPIView,
    )
    print('yo', list_classes)
    if len(list_classes) > 1:
        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

        def post(self, request, *args, **kwargs):
            return self.create(request, *args, **kwargs)

        view = type(
            f'{role.title()}{name.title()}ListView',
            list_classes,
            {
                'queryset': MockSet(*[
                    mock_fields(read.get('fields', {})) for i in range(0, 100)
                ]),
                'get': get,
                'post': post,
                'filterset_class': create_filter_class(role, name, read.get('filters', {})),
                'serializer_class': serializers.get('read'),
                'permission_classes': []
            }
        )
        print('hmmm', view)
        patterns.append(path(
            f'{PATH_PREFIX}/{role.lower()}/{name.lower()}',
            view.as_view(),
            name=f'{role.lower()}-{name.lower()}'
        ))


    detail_classes = (
        *([mixins.RetrieveModelMixin] if read else []),
        *([mixins.UpdateModelMixin] if update else []),
        *([mixins.DestroyModelMixin] if delete else []),
        generics.GenericAPIView,
    )
    if len(detail_classes) > 1:
        def get(self, request, *args, **kwargs):
            return self.retrieve(request, *args, **kwargs)

        def put(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs)

        def delete(self, request, *args, **kwargs):
            return self.destroy(request, *args, **kwargs)

        view = type(
            f'{role.title()}{name.title()}DetailView',
            detail_classes,
            {
                'queryset': MockSet(*[
                    mock_fields(read.get('fields', {})) for i in range(0, 100)
                ]),
                'get': get,
                'post': post,
                'delete': delete,
                'serializer_class': serializers.get('read'),
                'permission_classes': []
            }
        )
        patterns.append(path(
            f'{PATH_PREFIX}/{role.lower()}/{name.lower()}/<pk>',
            view.as_view(),
            name=f'{role.lower()}-{name.lower()}-detail'
        ))

    return patterns

def create_filter_class(role, name, filters):
    print('filters', filters.keys())
    return type(
        f'{role.title()}{name.title()}DetailFilter',
        (rest_framework.FilterSet,),
        {
            'Meta': type('Meta', (), {
                'fields': filters.keys()
            })
        }
    )

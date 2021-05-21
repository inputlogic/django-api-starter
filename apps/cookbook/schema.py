import graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (relay.Node, )


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'notes', 'category')


class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info):
        return Ingredient.objects.select_related('category').all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)

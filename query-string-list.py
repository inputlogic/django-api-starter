import uuid
from typing import TypeVar, Generic, List, Any, Callable, get_args
from pydantic import Field
from pydantic_core import core_schema
from ninja.filter_schema import FilterSchema as NinjaFilterSchema # Use alias to avoid name clash

# Define a TypeVar for the list items
T = TypeVar('T')

class QueryStringList(Generic[T]):
    """
    A Pydantic type that parses a query string parameter into a list of a specified type.
    It handles both comma-separated values in a single parameter
    (e.g., "?tags=movie,tv") and repeated parameters (e.g., "?id=1&id=2").
    """

    # Store the target item type (e.g., str, int, uuid.UUID)
    item_type: type

    @classmethod
    def _parse_value(cls, value: Any) -> List[T]:
        """
        Parses the input value (string or list) into a list of the target item type.
        """
        items_to_validate: List[str] = []

        if isinstance(value, list):
            # Input is already a list (from repeated query parameters)
            items_to_validate = [str(item) for item in value] # Ensure items are strings before validation
        elif isinstance(value, str):
            # Input is a string (comma-separated or single value)
            items_to_validate = [item.strip() for item in value.split(',') if item.strip()]
        else:
            # Let Pydantic's validation handle other incorrect types later if necessary,
            # but ideally, web frameworks pass strings or lists for query params.
            # We could raise a ValueError here for stricter input checking.
             raise ValueError(f"Expected list or comma-separated str, got {type(value).__name__}")


        validated_items: List[T] = []
        for item_str in items_to_validate:
            try:
                # Attempt to convert/validate the item using the target item_type's constructor
                # This works well for types like int, float, str, uuid.UUID
                validated_item = cls.item_type(item_str)
                validated_items.append(validated_item)
            except (ValueError, TypeError) as e:
                # If conversion fails, raise a ValueError that Pydantic can catch
                raise ValueError(f"Invalid item '{item_str}' for type {cls.item_type.__name__}: {e}") from e

        return validated_items

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: Callable[[Any], core_schema.CoreSchema]
    ) -> core_schema.CoreSchema:
        """
        Hook into Pydantic's schema generation process.
        """
        # 1. Extract the target item type T from QueryStringList[T]
        args = get_args(source)
        if not args or len(args) != 1:
            raise TypeError(f"{cls.__name__} requires exactly one type argument, e.g., {cls.__name__}[str]")
        
        # Store the item type on the class for the parser function to use.
        # Note: This approach assumes the class object is stable during validation.
        # Pydantic generally creates validators per schema field instance.
        cls.item_type = args[0] 

        # 2. Define the core schema:
        # It should accept either a string or a list as input.
        # Then, it uses our custom parsing function `_parse_value`.

        # Schema that accepts raw input (list or string)
        # input_schema = core_schema.union_schema(
        #     [
        #         core_schema.list_schema(core_schema.any_schema()), # Accepts lists (repeated params)
        #         core_schema.str_schema()  # Accepts strings (comma-separated or single)
        #     ],
        #     custom_error_type='value_error', # Generic error type if neither matches
        #     custom_error_message='Input must be a query string or a list of query parameters'
        # )
        
        # Chain the input schema with our custom parser/validator function
        # `no_info_plain_validator_function` takes a function that accepts only the value.
        # final_schema = core_schema.no_info_plain_validator_function(
        #     cls._parse_value, # Our function that handles parsing and type conversion
        #     # We could potentially chain input_schema first, but letting _parse_value
        #     # handle both list and str input directly is simpler here.
        # )
        
        # Pydantic V2 often uses function validators directly like this. 
        # Let's simplify to just the plain validator assuming it gets the raw query param value.
        
        # Simplified schema: Directly use our parser function.
        # Pydantic will pass the raw query parameter value (str or list) to it.
        return core_schema.no_info_plain_validator_function(cls._parse_value)

# --- Example Usage ---

# Assume you have Django models like this (simplified):
# class Tag(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#
# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey('Post', on_delete=models.CASCADE)
#
# class Post(models.Model):
#     title = models.CharField(max_length=100)
#     tags = models.ManyToManyField(Tag, related_name='posts')
#     likes = models.ManyToManyField(User, through=Like, related_name='liked_posts')


# Define your FilterSchema using the custom QueryStringList type
# class PostFilterSchema(NinjaFilterSchema):
#     # Handles ?tags=movie,tv OR ?tags=movie&tags=tv
#     # Maps to queryset filter: Post.objects.filter(tags__name__in=['movie', 'tv'])
#     tags: QueryStringList[str] | None = Field(None, q='tags__name__in')
#
#     # Handles ?liked_by=uuid1,uuid2 OR ?liked_by=uuid1&liked_by=uuid2
#     # Maps to queryset filter: Post.objects.filter(likes__user__in=[UUID('uuid1'), UUID('uuid2')])
#     liked_by: QueryStringList[uuid.UUID] | None = Field(None, q='likes__user__in') # 'likes' is the ManyToManyField name from Post to User (through Like)

# Example Ninja API endpoint
# from ninja import NinjaAPI
# from django.shortcuts import get_list_or_404
# from .models import Post # Assuming models.py is in the same directory

# api = NinjaAPI()

# @api.get("/posts")
# def list_posts(request, filters: PostFilterSchema):
#     queryset = Post.objects.all()
#     filtered_queryset = filters.filter(queryset) # Apply the filters
#
#     # You might want to apply distinct() if filtering on ManyToMany fields causes duplicates
#     posts = get_list_or_404(filtered_queryset.distinct())
#
#     # Replace with your actual Post schema/serialization
#     return [{"id": post.id, "title": post.title} for post in posts]

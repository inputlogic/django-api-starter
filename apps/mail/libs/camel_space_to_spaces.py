import re

from django.utils.text import camel_case_to_spaces

re_multiple_spaces = re.compile(r'( {2,})')


def camel_space_to_spaces(value):
    """
    Split CamelCase and convert to lower case.

    Strip surrounding whitespace and multiple consecutive internal spaces.
    """
    de_cameled = camel_case_to_spaces(value)
    return re_multiple_spaces.sub(r' ', de_cameled)

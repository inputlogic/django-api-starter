import re

re_camel_case = re.compile(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))')
re_multiple_spaces = re.compile(r'( {2,})')

def camel_space_to_spaces(value):
    """
    Split CamelCase and convert to lower case. Strip surrounding whitespace and internal multiple spaces.
    """
    de_cameled = re_camel_case.sub(r' \1', value).strip().lower()
    return re_multiple_spaces.sub(r' ', de_cameled)

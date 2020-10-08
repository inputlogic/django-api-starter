import json

from django.utils.html import mark_safe

from pygments import highlight, lexers, formatters


def make_pretty_json(data):
    response = json.dumps(data, sort_keys=True, indent=2)
    formatter = formatters.HtmlFormatter(style='colorful')
    response = highlight(response, lexers.JsonLexer(), formatter)
    style = "<style>" + formatter.get_style_defs() + "</style><br>"
    return mark_safe(style + response)

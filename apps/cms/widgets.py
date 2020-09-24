from django.contrib.admin import widgets
from django.utils.html import mark_safe


class AdminImageWidget(widgets.AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(
                '<a href="{}" target="_blank"><img src="{}" alt="{}" width="150" /></a>'.format(
                    image_url, image_url, file_name
                ))
        output.append(super(widgets.AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))


class ColorInputWidget(widgets.AdminTextInputWidget):
    input_type = 'color'

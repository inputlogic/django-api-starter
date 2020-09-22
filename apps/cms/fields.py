from django.db import models

from .widgets import ColorInputWidget


class ColorField(models.CharField):
    description = "A hex color value"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorInputWidget()
        return super(models.CharField, self).formfield(**kwargs)

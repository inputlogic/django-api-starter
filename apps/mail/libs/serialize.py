from datetime import datetime

from django.db.models import Model
from django.forms.models import model_to_dict


def serialize(data):
    if type(data) is dict:
        return {k: serialize(v) for (k, v) in data.items()}
    elif type(data) is datetime:
        return data.isoformat()
    elif isinstance(data, Model):
        # NOTE: possibility of infinite loop
        return serialize(model_to_dict(data))
    return data

from datetime import datetime


def serialize(data):
    if type(data) is dict:
        return {k: serialize(v) for (k, v) in data.items()}
    elif type(data) is datetime:
        return data.isoformat()
    return data

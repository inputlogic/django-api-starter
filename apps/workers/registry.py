_registry = []


def add(handler, schedule):
    token = (handler, schedule)
    if token not in _registry:
        _registry.append(token)


def get():
    return _registry

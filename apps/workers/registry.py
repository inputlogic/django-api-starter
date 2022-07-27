_registry = []


def add(handler, schedule, run_at):
    token = (handler, schedule, run_at)
    if token not in _registry:
        _registry.append(token)


def get():
    return _registry

import json
import base64


def dict_to_base64(d):
    return base64.b64encode(json.dumps(d).encode()).decode()


def base64_to_dict(s):
    return json.loads(base64.b64decode(s.encode()).decode())

import json


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def parse_kv_lines(lines):
    result = {}
    for l in lines:
        if l:
            key, value = l.split("=", maxsplit=1)
            result[key] = value
    return result

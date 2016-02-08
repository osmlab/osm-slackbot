import yaml


def load_patterns():
    patterns = None
    with open("osmslackbot/patterns.yml", 'r') as f:
        try:
            patterns = yaml.load(f)
        except:
            raise
    return patterns


def load_templates():
    templates = None
    with open("osmslackbot/responses.yml", 'r') as f:
        try:
            templates = yaml.load(f)
        except:
            pass
    return templates


def getValue(obj, names):
    value = None
    for name in names:
        value = obj.get(name, None)
        if value:
            break
    return value

import yaml


_digests = {}


def load_digests(input):
    set_digests(yaml.load(input))


def set_digests(digests):
    global _digests
    _digests = digests or {}


def digest(asset):
    return _digests.get(asset, asset)

DEBUG = False

GEOWATCH_STOPWORDS = [
    "nobot",
    "no bot",
    "stopbot",
    "stop bot",
    "ignorebot",
    "ignore bot",
    "skipbot",
    "skip bot",
    "!bot",
    "-bot"
]

try:
    from local_settings import *  # noqa
except ImportError:
    pass

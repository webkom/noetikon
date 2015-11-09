import urllib


def slugify(text):
    return urllib.parse.quote(text)

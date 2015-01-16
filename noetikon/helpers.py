from django.utils.text import slugify as django_slugify


def slugify(text):
    return django_slugify(text).replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa').lower()

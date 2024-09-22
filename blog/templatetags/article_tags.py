from django import template

register = template.Library()


@register.filter
def truncate_chars(value, max_chars=100):

    if len(value) > max_chars:
        return f"{value[:max_chars]}..."
    return value
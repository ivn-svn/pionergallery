from django import template
import re

register = template.Library()

@register.filter
def strip_html(value):
    return re.sub(r'<[^>]*?>', '', value)

@register.filter
def strip_and_truncate(value, arg):
    stripped_value = strip_html(value)
    try:
        length = int(arg)
    except ValueError:  # Invalid literal for int().
        return value  # Return the original string if we can't convert arg to int.
    if len(stripped_value) > length:
        truncated = stripped_value[:length]
        return truncated + "..."
    return stripped_value

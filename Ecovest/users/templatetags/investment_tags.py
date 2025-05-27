from django import template
from initiatives.models import Initiative

register = template.Library()

@register.filter
def lookup(value, arg):
    if 'initiative' in arg:
        return Initiative.objects.get(id=value)
    return None
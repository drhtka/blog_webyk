from django import template
register = template.Library()

@register.filter(name='split')
def slpit_filter(value, arg):
    return value.split(arg)
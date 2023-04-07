from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    return float(value) * float(arg)


@register.filter(name='divide')
def divide(value, arg):
    return float(value) / float(arg)

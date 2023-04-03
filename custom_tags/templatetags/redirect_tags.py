from django import template
from django.shortcuts import redirect

register = template.Library()


@register.simple_tag
def redirect_to(view_name, code):
    return redirect(view_name, code=code)

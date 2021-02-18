from django import template

register = template.Library()

@register.simple_tag
def sample():
    return "<b>sample</b>"

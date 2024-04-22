from django import template
import random

register = template.Library()

@register.simple_tag
def random_color():
    colors = ['#e5d0b3','#444444','#1B5F8C','#6c757d','#8e8b51']  # Your list of colors
    return random.choice(colors)
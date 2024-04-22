from django import template
from blog.models import Payment

register = template.Library()

@register.filter(name='has_payment')
def has_payment(user):
    if user.is_authenticated:
        return Payment.objects.filter(user=user).exists()
    return False

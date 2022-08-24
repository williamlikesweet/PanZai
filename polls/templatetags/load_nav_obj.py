from polls.models import Worker
from django import template
import pandas as pd

register = template.Library()


@register.inclusion_tag('navbar.html')
def navbar_worker():
    workers = Worker.objects.filter(status=1)
    return {'workers': workers}

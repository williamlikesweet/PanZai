from polls.models import Worker
from django import template
import pandas as pd

register = template.Library()


@register.inclusion_tag('navbar.html')
def sidebar_worker():
    workers = Worker.objects.all()
    return {'workers': workers}

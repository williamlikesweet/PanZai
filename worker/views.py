from django.shortcuts import render
from django.views.generic import ListView
from .models import Worker

class WorkerList(ListView):
    model = Worker
    template_name = "hongmingstone/Worker/worker.html"
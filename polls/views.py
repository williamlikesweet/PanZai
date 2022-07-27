from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Construction
from .models import Worker
from .models import Client

def start_document(request):
    
    return render(request, 'polls/starter.html')

def index(request):
    constructions = Construction.objects.select_related('client','worker').all()
    return render(request, 'polls/index.html',{'constructions':constructions})

def worker(request):
    workers = Worker.objects.all()
    return render(request, 'polls/worker.html',{'workers':workers})

def workercreate(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get("name")
        worker_object =  Worker.objects.create(name=name) #name=name, tile=tile
        context['object'] = worker_object
    return render(request, 'polls/workercreate.html')


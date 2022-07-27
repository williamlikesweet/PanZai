from unicodedata import name
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
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

def indexcreate(request):
    workers = Worker.objects.all()
    clients = Client.objects.all()
    context = {}
    if request.method == "POST":
        worker = request.POST.get("worker_id")
        client = request.POST.get("client_id")
        work_site = request.POST.get("work_site")
        Construction_item = request.POST.get("Construction_item")
        Construction_cm = request.POST.get("Construction_cm")
        Construction_unit = request.POST.get("Construction_unit")

        construction_object =  Construction.objects.create(
            worker_id= worker,
            client_id= client,
            work_site=work_site,
            Construction_item=Construction_item,
            Construction_cm=Construction_cm,
            Construction_unit=Construction_unit
            ) 
        context['object'] = construction_object
        return HttpResponseRedirect(reverse('index') )
    return render(request, 'polls/indexcreate.html',{'workers':workers,'clients':clients})



def client(request):
    clients = Client.objects.all()
    return render(request, 'polls/client.html',{'clients':clients})

def clientcreate(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get("name")
        client_object =  Client.objects.create(name=name) 
        context['object'] = client_object
        return HttpResponseRedirect(reverse('client') )
    return render(request, 'polls/clientcreate.html')


def worker(request):
    workers = Worker.objects.all()
    return render(request, 'polls/worker.html',{'workers':workers})

def workercreate(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get("name")
        worker_object =  Worker.objects.create(name=name) #name=name, tile=tile
        context['object'] = worker_object
        return HttpResponseRedirect(reverse('worker') )

    return render(request, 'polls/workercreate.html')


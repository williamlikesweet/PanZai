from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from polls.Enums.EnumWorker import EnumWorker
from polls.models import Construction
from polls.models import Worker
from polls.models import Client
import pandas as pd


def start_document(request):
    return render(request, 'polls/starter.html')


def index(request):
    constructions = Construction.objects.select_related('client', 'worker').all()
    return render(request, 'polls/index.html', {'constructions': constructions})


def indexcreate(request):
    workers = Worker.objects.all()
    clients = Client.objects.all()
    context = {}
    if request.method == "POST":
        worker_id = request.POST.get("worker_id")
        client_id = request.POST.get("client_id")
        work_site = request.POST.get("work_site")
        Construction_item = request.POST.get("Construction_item")
        Construction_cm = request.POST.get("Construction_cm")
        Construction_unit = request.POST.get("Construction_unit")

        construction_object = Construction.objects.create(
            worker_id=worker_id,
            client_id=client_id,
            work_site=work_site,
            Construction_item=Construction_item,
            Construction_cm=Construction_cm,
            Construction_unit=Construction_unit
        )
        context['object'] = construction_object
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'polls/indexcreate.html', {'workers': workers, 'clients': clients})


def client(request):
    clients = Client.objects.all()
    return render(request, 'polls/client.html', {'clients': clients})


def clientcreate(request):
    context = {}
    if request.method == "POST":
        client_name = request.POST.get("name")
        client_object = Client.objects.create(name=client_name)
        context['object'] = client_object
        return HttpResponseRedirect(reverse('client'))
    return render(request, 'polls/clientcreate.html')


def worker_status_transfer(row):  # 多加入一欄 funtion
    if row['status'] == EnumWorker.status_on.value:
        row['status'] = '在職'
    elif row["status"] == EnumWorker.status_off.value:
        row['status'] = '離職'
    return row


def worker(request):
    # workers = Worker.objects.all()
    workers = pd.DataFrame(Worker.objects.all().values())
    workers = workers.apply(worker_status_transfer, axis=1)
    return render(request, 'polls/worker.html', {'workers': workers})


def workercreate(request):
    context = {}
    if request.method == "POST":
        worker_name = request.POST.get("name")
        worker_status = request.POST.get("status")
        worker_object = Worker.objects.create(name=worker_name, status=worker_status)  # name=name, tile=tile
        context['object'] = worker_object
        return HttpResponseRedirect(reverse('worker'))

    return render(request, 'polls/workercreate.html')

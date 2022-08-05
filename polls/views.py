import tablib
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from polls.Enums.EnumWorker import EnumWorker
from polls.models import Construction, ConstructionItem
from polls.models import Worker
from polls.models import Client
import pandas as pd
from tablib import Dataset
from polls.resources import ClientResource
import datetime


def start_document(request):
    return render(request, 'polls/starter.html')


def index(request):
    constructions = Construction.objects.select_related('client', 'worker', 'constructionItem').all()
    return render(request, 'polls/index.html', {'constructions': constructions})


def indexcreate(request):
    workers = Worker.objects.all()
    clients = Client.objects.all()
    context = {}
    if request.method == "POST":
        worker_id = request.POST.get("worker_id")
        client_id = request.POST.get("client_id")
        work_site = request.POST.get("work_site")
        construction_item = request.POST.get("construction_item")
        construction_cm = request.POST.get("construction_cm")
        construction_unit = request.POST.get("construction_unit")
        construction_split = request.POST.get("construction_split")
        publish_at = request.POST.get("publish_at")
        construction_object = Construction.objects.create(
            worker_id=worker_id,
            client_id=client_id,
            work_site=work_site,
            construction_item=construction_item,
            construction_cm=construction_cm,
            construction_unit=construction_unit,
            construction_split=construction_split,
            publish_at=publish_at,
        )
        context['object'] = construction_object
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'polls/indexcreate.html', {'workers': workers, 'clients': clients})


def constructionItem(request):
    constructionitems = ConstructionItem.objects.all()
    return render(request, 'polls/constructionItem.html', {'constructionitems': constructionitems})


def constructionItemCreate(request):
    context = {}
    if request.method == "POST":
        item = request.POST.get("item")
        Constructionitem_object = ConstructionItem.objects.create(item=item)
        context['object'] = Constructionitem_object
        return HttpResponseRedirect(reverse('constructionitem'))
    return render(request, 'polls/constructionItemcreate.html')


def client(request):
    clients = Client.objects.all()
    if request.method == 'POST' and request.FILES['importData']:
        client_resource = ClientResource()
        # file_format = request.POST['file-format']
        dataset = Dataset()
        new_clients = request.FILES['importData']
        if new_clients.content_type == 'text/csv':
            imported_data = dataset.load(new_clients.read().decode('utf-8'), format='csv')
            result = client_resource.import_data(dataset, dry_run=False)
            return HttpResponseRedirect(reverse('client'))
        else:
            imported_data = dataset.load(new_clients.read())
            result = client_resource.import_data(dataset, dry_run=False)
            return HttpResponseRedirect(reverse('client'))
    else:
        pass
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

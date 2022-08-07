from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from polls.Enums.EnumWorker import EnumWorker
from polls.models import Worker
import pandas as pd


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


def workerCreate(request):
    context = {}
    if request.method == "POST":
        worker_name = request.POST.get("name")
        worker_status = request.POST.get("status")
        worker_object = Worker.objects.create(name=worker_name, status=worker_status)  # name=name, tile=tile
        context['object'] = worker_object
        return HttpResponseRedirect(reverse('worker'))

    return render(request, 'polls/workercreate.html')

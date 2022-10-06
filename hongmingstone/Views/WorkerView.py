from django.shortcuts import render
from django import forms

from hongmingstone.Enums.EnumWorker import EnumWorker
from hongmingstone.models import Construction, ConstructionItem
from hongmingstone.models import Worker
from hongmingstone.models import Client
import pandas as pd
import numpy as np
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, FormView, CreateView, DeleteView
from django.urls import reverse_lazy
from datetime import datetime, timedelta


class AddWorkerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddWorkerForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = 1

    class Meta:
        model = Worker
        fields = ['name', 'status']
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "status": forms.RadioSelect(choices=EnumWorker.CHOICES.value)
        }


class WorkerList(ListView):
    model = Worker
    template_name = "hongmingstone/Worker/worker.html"


class WorkerCreate(CreateView):
    model = Worker
    form_class = AddWorkerForm
    template_name = "hongmingstone/Worker/workercreate.html"
    success_url = reverse_lazy('worker')


class WorkerUpdate(UpdateView):
    model = Worker
    form_class = AddWorkerForm
    template_name = "hongmingstone/Worker/workercreate.html"
    success_url = reverse_lazy('worker')


def worker_datail(request, worker_id):
    query = request.GET.get('daterangefilter')
    workers = pd.DataFrame(Worker.objects.all().values('id', 'name'))
    client = pd.DataFrame(Client.objects.all().values('id', 'name'))
    constructionItem = pd.DataFrame(ConstructionItem.objects.all().values('id', 'item'))
    if query:
        query = query.replace(' ', '')
        start = datetime.strptime(query.split('-', 1)[0], "%m/%d/%Y").date()
        end = datetime.strptime(query.split('-', 1)[1], "%m/%d/%Y").date()
        end = end + timedelta(days=1)
        constructions = pd.DataFrame(Construction.objects.filter(worker_id=worker_id).values())
        constructions = constructions[
            (constructions['publish_at'] >= str(start)) & (constructions['publish_at'] < str(end))]
        constructions = constructions.groupby(
            ['publish_at', 'worker_id', 'client_id', 'work_site', 'constructionItem_id']).sum().reset_index()
    else:
        constructions = pd.DataFrame(Construction.objects.filter(worker_id=worker_id).values())
        constructions = constructions.groupby(
            ['publish_at', 'worker_id', 'client_id', 'work_site', 'constructionItem_id']).sum().reset_index()
    resultData = pd.merge(constructions, workers, left_on="worker_id", right_on="id", how='left',
                          suffixes=('', '_worker'))
    worker_name = resultData
    resultData = pd.merge(resultData, client, left_on="client_id", right_on="id", how='left', suffixes=('', '_client'))
    resultData = pd.merge(resultData, constructionItem, left_on="constructionItem_id", right_on="id", how='left',
                          suffixes=('', '_constructionItem'))
    # resultData = resultData.apply(lambda x: x.replace(r'\.0', "", regex=True))
    try:
        resultData = resultData.pivot_table(
            index=['publish_at', 'name_client', 'work_site',
                   'item'],
            values=['construction_amount'],
        ).unstack().replace(np.nan, '')
        resultData = resultData.droplevel(0, axis=1).reset_index()
        resultData['publish_at'] = resultData['publish_at'].dt.strftime('%Y-%m-%d')
        resultData = resultData.rename(
            columns={'publish_at': '安裝日期', 'name_client': '客戶名稱', 'work_site': '案場地址'})
        DataFrame = resultData.to_html(table_id='example1',
                                       classes='table table-striped table-bordered table-head-fixed text-nowrap table-hover',
                                       float_format='{:10.0f}'.format
                                       )
        return render(request, 'hongmingstone/Worker/worker_detail.html',
                      {'resultData': resultData, 'DataFrame_html': DataFrame, 'worker_name': worker_name})
    except Exception as e:
        return render(request, '404.html', {'message': str(e)})

# class WorkerDetailView(DetailView):
#     model = Construction
#     template_name = "hongmingstone/worker_detail.html"
#     slug_field = 'worker'
#     slug_url_kwarg = 'worker_id'
#
#     def get_queryset(self):
#         constructions = Construction.objects.select_related('client', 'worker', 'constructionItem').all()
#         return constructions
#
#     def get_context_data(self, **kwargs):
#         context = super(WorkerDetailView, self).get_context_data(**kwargs)
#         return context

# def worker_status_transfer(row):  # 多加入一欄 funtion
#     if row['status'] == EnumWorker.status_on.value:
#         row['status'] = '在職'
#     elif row["status"] == EnumWorker.status_off.value:
#         row['status'] = '離職'
#     return row
#
#
# def worker(request):
#     # workers = Worker.objects.all()
#     # 轉換DataFrame
#     workers = pd.DataFrame(Worker.objects.all().values())
#     workers = workers.apply(worker_status_transfer, axis=1)
#     return render(request, 'hongmingstone/worker.html', {'workers': workers})
#
#
# def workerCreate(request):
#     context = {}
#     if request.method == "POST":
#         worker_name = request.POST.get("name")
#         worker_status = request.POST.get("status")
#         worker_object = Worker.objects.create(name=worker_name, status=worker_status)  # name=name, tile=tile
#         context['object'] = worker_object
#         return HttpResponseRedirect(reverse('worker'))
#
#     return render(request, 'hongmingstone/workercreate.html')

from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, FormView, CreateView, DeleteView
from .models import Worker
from django.urls import reverse_lazy
from hongmingstone.service.DaterangeFilterService import daterangeFilter
from hongmingstone.models import Construction, ConstructionItem, Client
import pandas as pd
import numpy as np
from .forms import WorkerForm
from .serializers import WorkerSerializer
from datetime import datetime
import calendar


class WorkerList(ListView):
    model = Worker
    serializer_class = WorkerSerializer
    template_name = "hongmingstone/Worker/worker.html"


class WorkerCreate(CreateView):
    model = Worker
    form_class = WorkerForm
    template_name = "hongmingstone/Worker/workercreate.html"
    success_url = reverse_lazy('worker')


class WorkerUpdate(UpdateView):
    model = Worker
    form_class = WorkerForm
    template_name = "hongmingstone/Worker/workercreate.html"
    success_url = reverse_lazy('worker')


def Worker_datail(request, worker_id):
    query = request.GET.get('daterangefilter')
    workers = pd.DataFrame(Worker.objects.all().values('id', 'name'))
    client = pd.DataFrame(Client.objects.all().values('id', 'name'))
    constructionItem = pd.DataFrame(ConstructionItem.objects.all().values('id', 'item'))
    if query:
        dateRange = daterangeFilter(query)
        constructions = pd.DataFrame(Construction.objects.filter(worker_id=worker_id).values())
        constructions = constructions[
            (constructions['publish_at'] >= str(dateRange.start())) & (
                    constructions['publish_at'] < str(dateRange.end()))]
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


class WorkerAmount(ListView):
    model = Construction
    template_name = "hongmingstone/Worker/worker_amount.html"

    def get_queryset(self):
        query = self.request.GET.get('daterangefilter', '')
        if query:
            dateRange = daterangeFilter(query)
            workerAmount = Construction.objects.select_related('worker').values('worker__name').annotate(
                Sum('construction_amount')).filter(publish_at__range=[dateRange.start(), dateRange.end()])
        else:
            this_month_start = datetime(datetime.now().year, datetime.now().month, 1)
            this_month_end = datetime(datetime.now().year, datetime.now().month,
                                      calendar.monthrange(datetime.now().year, datetime.now().month)[1])
            workerAmount = Construction.objects.select_related('worker').values('worker__name').annotate(
                Sum('construction_amount')).filter(publish_at__range=[this_month_start, this_month_end])
        return workerAmount

    def get_context_data(self, **kwargs):
        context = super(WorkerAmount, self).get_context_data(**kwargs)
        # context['bar_list'] = context['foo_list'].filter(Country=64)
        return context

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

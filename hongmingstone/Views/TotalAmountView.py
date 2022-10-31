from django.db.models import Sum

from hongmingstone.Service.DaterangeFilterService import daterangeFilter
from hongmingstone.models import Construction
from django.views.generic import ListView
from datetime import datetime
import calendar


class ClientAmount(ListView):
    model = Construction
    template_name = "hongmingstone/Client/client_amount.html"

    def get_queryset(self):
        query = self.request.GET.get('daterangefilter', '')
        if query:
            dateRange = daterangeFilter(query)
            clientamount = Construction.objects.select_related('client').values('client__name').annotate(
                Sum('construction_amount')).filter(publish_at__range=[dateRange.start(), dateRange.end()])
        else:
            this_month_start = datetime(datetime.now().year, datetime.now().month, 1)
            this_month_end = datetime(datetime.now().year, datetime.now().month,
                                      calendar.monthrange(datetime.now().year, datetime.now().month)[1])
            # print(this_month_start)
            clientamount = Construction.objects.select_related('client').values('client__name').annotate(
                Sum('construction_amount')).filter(publish_at__range=[this_month_start, this_month_end])
        return clientamount

    def get_context_data(self, **kwargs):
        context = super(ClientAmount, self).get_context_data(**kwargs)
        # context['bar_list'] = context['foo_list'].filter(Country=64)
        return context


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

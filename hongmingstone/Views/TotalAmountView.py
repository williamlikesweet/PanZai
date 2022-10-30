from django.db.models import Sum
from hongmingstone.models import Construction
from django.views.generic import ListView
from datetime import datetime
from datetime import timedelta
import calendar


class ClientAmount(ListView):
    model = Construction
    template_name = "hongmingstone/Client/client_amount.html"

    def get_queryset(self):
        query = self.request.GET.get('daterangefilter', '')
        if query:
            query = query.replace(' ', '')
            start = datetime.strptime(query.split('-', 1)[0], "%m/%d/%Y").date()
            end = datetime.strptime(query.split('-', 1)[1], "%m/%d/%Y").date()
            end = end + timedelta(days=1)
            query = Construction.objects.select_related('client').values('client__name').annotate(
                Sum('construction_amount')).filter(publish_at__range=[start, end])
        else:
            this_month_start = datetime(datetime.now().year, datetime.now().month, 1)
            this_month_end = datetime(datetime.now().year, datetime.now().month, calendar.monthrange(datetime.now().year, datetime.now().month)[1])
            print(this_month_start)
            query = Construction.objects.select_related('client').values('client__name').annotate(
                Sum('construction_amount')).filter(publish_at__range=[this_month_start, this_month_end])
        return query

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
            query = query.replace(' ', '')
            start = datetime.strptime(query.split('-', 1)[0], "%m/%d/%Y").date()
            end = datetime.strptime(query.split('-', 1)[1], "%m/%d/%Y").date()
            end = end + timedelta(days=1)
            query = Construction.objects.select_related('worker').values('worker__name').annotate(
                Sum('construction_amount')).filter(publish_at__range=[start, end])
        else:
            this_month_start = datetime(datetime.now().year, datetime.now().month, 1)
            this_month_end = datetime(datetime.now().year, datetime.now().month, calendar.monthrange(datetime.now().year, datetime.now().month)[1])
            query = Construction.objects.select_related('worker').values('worker__name').annotate(
                Sum('construction_amount')).filter(publish_at__range=[this_month_start, this_month_end])
        return query

    def get_context_data(self, **kwargs):
        context = super(WorkerAmount, self).get_context_data(**kwargs)
        # context['bar_list'] = context['foo_list'].filter(Country=64)
        return context

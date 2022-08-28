from django.db.models import Sum
from polls.models import Construction
from django.views.generic import ListView
from datetime import datetime, timedelta


class ClientAmount(ListView):
    model = Construction
    template_name = "polls/Client/client_amount.html"

    def get_queryset(self):
        daterangefilter = self.request.GET.get('daterangefilter', '')
        if daterangefilter:
            daterangefilter = daterangefilter.replace(' ', '')
            start = datetime.strptime(daterangefilter.split('-', 1)[0], "%m/%d/%Y").date()
            end = datetime.strptime(daterangefilter.split('-', 1)[1], "%m/%d/%Y").date()
            end = end + timedelta(days=1)
            query = Construction.objects.select_related('client').values('client__name').annotate(
                Sum('construction_amount')).filter(publish_at__range=[start, end])
        else:
            query = Construction.objects.select_related('client').values('client__name').annotate(
                Sum('construction_amount'))
        return query

    def get_context_data(self, **kwargs):
        context = super(ClientAmount, self).get_context_data(**kwargs)
        # context['bar_list'] = context['foo_list'].filter(Country=64)
        return context


class WorkerAmount(ListView):
    model = Construction
    template_name = "polls/Worker/worker_amount.html"

    def get_queryset(self):
        daterangefilter = self.request.GET.get('daterangefilter', '')
        if daterangefilter:
            daterangefilter = daterangefilter.replace(' ', '')
            start = datetime.strptime(daterangefilter.split('-', 1)[0], "%m/%d/%Y").date()
            end = datetime.strptime(daterangefilter.split('-', 1)[1], "%m/%d/%Y").date()
            end = end + timedelta(days=1)
            query = Construction.objects.select_related('worker').values('worker__name').annotate(
                Sum('construction_amount')).filter(publish_at__range=[start, end])
        else:
            query = Construction.objects.select_related('worker').values('worker__name').annotate(
                Sum('construction_amount'))
        return query

    def get_context_data(self, **kwargs):
        context = super(WorkerAmount, self).get_context_data(**kwargs)
        # context['bar_list'] = context['foo_list'].filter(Country=64)
        return context

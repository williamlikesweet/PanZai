from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from tablib import Dataset

from polls.models import Construction, ConstructionItem
from polls.models import Worker
from polls.models import Client
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, FormView, CreateView, DeleteView

from polls.resources import ConstructionResource
from datetime import datetime, timedelta
from django.db.models import Count


class AddConstructionForm(forms.ModelForm):
    class Meta:
        model = Construction
        exclude = ('worker_id', 'client_id', 'constructionItem_id')

        widgets = {
            "worker": forms.Select(attrs={'class': 'form-control select2'}),
            "client": forms.Select(attrs={'class': 'form-control select2'}),
            "constructionItem": forms.Select(attrs={'class': 'form-control select2'}),
            "work_site": forms.TextInput(attrs={'class': 'form-control'}),
            "construction_length": forms.TextInput(attrs={'class': 'form-control'}),
            "construction_unit": forms.TextInput(attrs={'class': 'form-control'}),
            "construction_split": forms.TextInput(attrs={'class': 'form-control'}),
            "construction_amount": forms.TextInput(attrs={'class': 'form-control'}),
            "publish_at": forms.DateInput(attrs={'class': 'form-control', 'type': "date"}),
            'data-target': '#datetimepicker1'
        }

    def __init__(self, *args, **kwargs):
        worker = kwargs.pop('worker_id', None)
        client = kwargs.pop('client_id', None)
        constructionItem = kwargs.pop('constructionItem_id', None)
        super(AddConstructionForm, self).__init__(*args, **kwargs)
        self.fields['work_site'].required = False
        self.fields['construction_length'].required = False
        self.fields['construction_unit'].required = False
        self.fields['construction_split'].required = False
        self.fields['construction_amount'].required = False
        self.fields['publish_at'].required = True
        self.fields['publish_at'].input_formats = ["%Y-%m-%d"]


def ConstructionImport(request):
    if request.method == 'POST' and request.FILES['importData']:
        Construction_resource = ConstructionResource()
        # file_format = request.POST['file-format']
        dataset = Dataset()
        new_construction = request.FILES['importData']
        if new_construction.content_type == 'text/csv':
            imported_data = dataset.load(new_construction.read().decode('utf-8'), format='csv')
            result = Construction_resource.import_data(dataset, dry_run=False, raise_errors=True, use_transactions=True)
            return HttpResponseRedirect(reverse('construction'))
        else:
            imported_data = dataset.load(new_construction.read())
            result = Construction_resource.import_data(dataset, dry_run=False, raise_errors=True, use_transactions=True)
            return HttpResponseRedirect(reverse('construction'))
    else:
        pass
    return render(request, 'polls/Construction/construction_import.html')


class ConstructionCreate(CreateView):
    model = Construction
    form_class = AddConstructionForm
    template_name = "polls/Construction/construction_create.html"
    success_url = reverse_lazy('construction')

    def get(self, request, *args, **kwargs):
        workers = Worker.objects.all()
        clients = Client.objects.all()
        constructionitems = ConstructionItem.objects.all()
        context = {'form': AddConstructionForm(),
                   'workers': workers,
                   'clients': clients,
                   'constructionitems': constructionitems}
        return render(request, 'polls/Construction/construction_create.html', context)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ConstructionCreate, self).get_form_kwargs(*args, **kwargs)
        kwargs['worker_id'] = self.request.POST['worker']
        kwargs['client_id'] = self.request.POST['client']
        kwargs['constructionItem_id'] = self.request.POST['constructionItem']
        return kwargs

    # 有特別需求可覆蓋
    def form_valid(self, form):
        form.instance.worker_id = self.request.POST['worker']
        form.instance.client_id = self.request.POST['client']
        form.instance.constructionItem_id = self.request.POST['constructionItem']
        form.save()
        return super(ConstructionCreate, self).form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     form = AddConstructionForm(request.POST)
    #     if form.is_valid():
    #         kwargs['worker'] = self.request.POST['worker_id']
    #         kwargs['client'] = self.request.POST['client_id']
    #         kwargs['constructionItem'] = self.request.POST['constructionItem_id']
    #         construction = form.save()
    #         construction.save()
    #         return HttpResponseRedirect(reverse_lazy('construction'))
    #     return render(request, 'polls/construction.html', {'form': form})


class ConstructionList(ListView):
    model = Construction
    template_name = "polls/Construction/construction.html"

    def get_queryset(self):
        # constructions = Construction.objects.select_related('client', 'worker','constructionItem').all()  # 排序方法 .order_by('-id')
        query = self.request.GET.get('daterangefilter')
        if query:
            query = query.replace(' ', '')
            start = datetime.strptime(query.split('-', 1)[0], "%m/%d/%Y").date()
            end = datetime.strptime(query.split('-', 1)[1], "%m/%d/%Y").date()
            end = end + timedelta(days=1)
            constructions = Construction.objects.select_related('client', 'worker', 'constructionItem').filter(
                created_at__range=[start, end])
        else:
            constructions = Construction.objects.select_related('client', 'worker',
                                                                'constructionItem').all()  # 排序方法 .order_by('-id')

        return constructions

    def get_context_data(self, **kwargs):
        context = super(ConstructionList, self).get_context_data(**kwargs)
        # context['bar_list'] = context['foo_list'].filter(Country=64)
        return context


class ConstructionUpdate(UpdateView):
    model = Construction
    form_class = AddConstructionForm
    template_name = "polls/Construction/construction_create.html"
    success_url = reverse_lazy('construction')


class ConstructionDelete(DeleteView):
    model = Construction
    template_name = "polls/Construction/construction_confirm_delete.html"
    success_url = reverse_lazy('construction')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class BatchConstruction(ListView):
    model = Construction
    template_name = "polls/Construction/batch.html"

    def get_queryset(self):
        query = Construction.objects.values('created_at').annotate(dcount=Count('created_at')).order_by()
        return query

    def get_context_data(self, **kwargs):
        context = super(BatchConstruction, self).get_context_data(**kwargs)
        # context['bar_list'] = context['foo_list'].filter(Country=64)
        return context


def delete(request, created_at):
    construction = Construction.objects.filter(created_at=created_at)
    construction.delete()
    return HttpResponseRedirect(reverse('batch'))


# DeleteView還沒成功
# class BatchDelete(DeleteView):
#     model = Construction
#     template_name = "polls/Construction/batch_confirm_delete.html"
#     success_url = reverse_lazy('construction')
#
#     def get_queryset(self):
#         return Construction.objects.filter(created_at=self.request.GET.created_at)


# 以前寫法
# def construction(request):
#     constructions = Construction.objects.select_related('client', 'worker', 'constructionItem').all()
#     return render(request, 'polls/construction.html', {'constructions': constructions})

# def constructionCreate(request):
#     workers = Worker.objects.all()
#     clients = Client.objects.all()
#     constructionitems = ConstructionItem.objects.all()
#     context = {}
#     if request.method == "POST":
#         worker_id = request.POST.get("worker_id")
#         client_id = request.POST.get("client_id")
#         constructionItem_id = request.POST.get("constructionItem_id")
#         work_site = request.POST.get("work_site")
#         construction_length = request.POST.get("construction_length")
#         if construction_length == "":
#             construction_length = None
#         construction_unit = request.POST.get("construction_unit")
#         construction_split = request.POST.get("construction_split")
#         construction_amount = request.POST.get("construction_amount")
#         publish_at = request.POST.get("publish_at")
#         construction_object = Construction.objects.create(
#             worker_id=worker_id,
#             client_id=client_id,
#             constructionItem_id=constructionItem_id,
#             work_site=work_site,
#             construction_length=construction_length,
#             construction_unit=construction_unit,
#             construction_split=construction_split,
#             construction_amount=construction_amount,
#             publish_at=publish_at,
#         )
#         context['object'] = construction_object
#         return HttpResponseRedirect(reverse('construction'))
#     return render(request, 'polls/construction_create.html',
#                   {'workers': workers, 'clients': clients, 'constructionitems': constructionitems})

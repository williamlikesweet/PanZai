from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from polls.models import Construction, ConstructionItem
from polls.models import Worker
from polls.models import Client
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, FormView, CreateView, DeleteView


class AddConstructionForm(forms.ModelForm):
    class Meta:
        model = Construction
        exclude = ('worker_id', 'client_id', 'constructionItem_id')
        # fields = [
        #     'work_site',
        #     'construction_length',
        #     'construction_unit',
        #     'construction_split',
        #     'construction_amount',
        #     'publish_at']

        widgets = {
            "worker": forms.Select(attrs={'class': 'form-control'}),
            "client": forms.Select(attrs={'class': 'form-control'}),
            "constructionItem": forms.Select(attrs={'class': 'form-control'}),
            "work_site": forms.TextInput(attrs={'class': 'form-control'}),
            "construction_length": forms.TextInput(attrs={'class': 'form-control'}),
            "construction_unit": forms.TextInput(attrs={'class': 'form-control'}),
            "construction_split": forms.TextInput(attrs={'class': 'form-control'}),
            "construction_amount": forms.TextInput(attrs={'class': 'form-control'}),
            "publish_at": forms.DateInput(attrs={'class': 'form-control', 'type': "date"})
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
        self.fields['publish_at'].required = False


class ConstructionCreate(CreateView):
    model = Construction
    form_class = AddConstructionForm
    template_name = "polls/constrctioncreate.html"
    success_url = reverse_lazy('construction')

    def get(self, request, *args, **kwargs):
        workers = Worker.objects.all()
        clients = Client.objects.all()
        constructionitems = ConstructionItem.objects.all()
        context = {'form': AddConstructionForm(),
                   'workers': workers,
                   'clients': clients,
                   'constructionitems': constructionitems}
        return render(request, 'polls/constrctioncreate.html', context)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ConstructionCreate, self).get_form_kwargs(*args, **kwargs)
        kwargs['worker_id'] = self.request.POST['worker']
        kwargs['client_id'] = self.request.POST['client']
        kwargs['constructionItem_id'] = self.request.POST['constructionItem']
        return kwargs

    # 有特別需求可覆蓋
    # def form_valid(self, form):
    #     print('thisQQ')
    #     form.instance.worker = self.request.POST.worker
    #     return super(ConstructionCreate).form_valid(form)

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
    template_name = "polls/construction.html"

    def get_queryset(self):
        constructions = Construction.objects.select_related('client', 'worker', 'constructionItem').all()
        return constructions

    def get_context_data(self, **kwargs):
        context = super(ConstructionList, self).get_context_data(**kwargs)
        # context['bar_list'] = context['foo_list'].filter(Country=64)
        return context


class ConstructionUpdate(UpdateView):
    model = Construction
    form_class = AddConstructionForm
    template_name = "polls/constrctioncreate.html"
    success_url = reverse_lazy('construction')


class ConstructionDelete(DeleteView):
    model = Construction
    success_url = reverse_lazy('construction')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

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
#     return render(request, 'polls/constrctioncreate.html',
#                   {'workers': workers, 'clients': clients, 'constructionitems': constructionitems})

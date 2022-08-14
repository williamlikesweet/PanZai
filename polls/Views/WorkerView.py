from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms

from polls.Enums.EnumWorker import EnumWorker
from polls.models import Worker
import pandas as pd
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, FormView, CreateView, DeleteView
from django.urls import reverse_lazy

CHOICES = (
    (1, '在職'),
    (0, '離職'),
)


class AddWorkerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddWorkerForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = 1

    class Meta:
        model = Worker
        fields = ['name', 'status']
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "status": forms.RadioSelect(choices=CHOICES)
        }


class WorkerList(ListView):
    model = Worker
    template_name = "polls/worker.html"


class WorkerCreate(CreateView):
    model = Worker
    form_class = AddWorkerForm
    template_name = "polls/workercreate.html"
    success_url = reverse_lazy('worker')


class WorkerUpdate(UpdateView):
    model = Worker
    form_class = AddWorkerForm
    template_name = "polls/workercreate.html"
    success_url = reverse_lazy('worker')

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
#     return render(request, 'polls/worker.html', {'workers': workers})
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
#     return render(request, 'polls/workercreate.html')

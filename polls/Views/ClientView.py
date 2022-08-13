from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from polls.models import Client
from tablib import Dataset
from polls.resources import ClientResource
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, FormView, CreateView, DeleteView
from django.urls import reverse_lazy


class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name']

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'})
        }


def ClientImport(request):
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
    return render(request, 'polls/client_import.html')


class ClientList(ListView):
    model = Client
    template_name = "polls/client.html"


class ClientCreate(CreateView):
    model = Client
    form_class = AddClientForm
    template_name = "polls/clientcreate.html"
    success_url = reverse_lazy('client')


class ClientUpdate(UpdateView):
    model = Client
    form_class = AddClientForm
    template_name = "polls/clientcreate.html"
    success_url = reverse_lazy('client')


class ClientDelete(DeleteView):
    model = Client
    success_url = reverse_lazy('client')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# def clientCreate(request):
#     context = {}
#     if request.method == "POST":
#         client_name = request.POST.get("name")
#         client_object = Client.objects.create(name=client_name)
#         context['object'] = client_object
#         return HttpResponseRedirect(reverse('client'))
#     return render(request, 'polls/clientcreate.html')

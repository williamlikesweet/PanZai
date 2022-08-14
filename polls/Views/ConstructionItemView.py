from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from polls.models import ConstructionItem
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, FormView, CreateView, DeleteView
from django.urls import reverse_lazy


class AddConstructionItemForm(forms.ModelForm):
    class Meta:
        model = ConstructionItem
        fields = ['item']

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'})
        }


class ConstructionItemList(ListView):
    model = ConstructionItem
    template_name = "polls/constructionItem.html"


class ConstructionItemCreate(CreateView):
    model = ConstructionItem
    form_class = AddConstructionItemForm
    template_name = "polls/constructionItemcreate.html"
    success_url = reverse_lazy('constructionitem')


class ConstructionItemUpdate(UpdateView):
    model = ConstructionItem
    form_class = AddConstructionItemForm
    template_name = "polls/constructionItemcreate.html"
    success_url = reverse_lazy('constructionitem')

# def constructionItem(request):
#     constructionitems = ConstructionItem.objects.all()
#     return render(request, 'polls/constructionItem.html', {'constructionitems': constructionitems})
#
#
# def constructionItemCreate(request):
#     context = {}
#     if request.method == "POST":
#         item = request.POST.get("item")
#         item_object = ConstructionItem.objects.create(item=item)
#         context['object'] = item_object
#         return HttpResponseRedirect(reverse('constructionitem'))
#     return render(request, 'polls/constructionItemcreate.html')

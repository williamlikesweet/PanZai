from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from polls.models import ConstructionItem


def constructionItem(request):
    constructionitems = ConstructionItem.objects.all()
    return render(request, 'polls/constructionItem.html', {'constructionitems': constructionitems})


def constructionItemCreate(request):
    context = {}
    if request.method == "POST":
        item = request.POST.get("item")
        item_object = ConstructionItem.objects.create(item=item)
        context['object'] = item_object
        return HttpResponseRedirect(reverse('constructionitem'))
    return render(request, 'polls/constructionItemcreate.html')

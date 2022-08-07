from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from polls.models import Construction, ConstructionItem
from polls.models import Worker
from polls.models import Client


def construction(request):
    constructions = Construction.objects.select_related('client', 'worker', 'constructionItem').all()
    return render(request, 'polls/construction.html', {'constructions': constructions})


def constructionCreate(request):
    workers = Worker.objects.all()
    clients = Client.objects.all()
    constructionitems = ConstructionItem.objects.all()
    context = {}
    if request.method == "POST":
        worker_id = request.POST.get("worker_id")
        client_id = request.POST.get("client_id")
        constructionItem_id = request.POST.get("constructionItem_id")
        work_site = request.POST.get("work_site")
        construction_length = request.POST.get("construction_length")
        if construction_length == "":
            construction_length = None
        construction_unit = request.POST.get("construction_unit")
        construction_split = request.POST.get("construction_split")
        construction_amount = request.POST.get("construction_amount")
        publish_at = request.POST.get("publish_at")
        construction_object = Construction.objects.create(
            worker_id=worker_id,
            client_id=client_id,
            constructionItem_id=constructionItem_id,
            work_site=work_site,
            construction_length=construction_length,
            construction_unit=construction_unit,
            construction_split=construction_split,
            construction_amount=construction_amount,
            publish_at=publish_at,
        )
        context['object'] = construction_object
        return HttpResponseRedirect(reverse('construction'))
    return render(request, 'polls/constrctioncreate.html',
                  {'workers': workers, 'clients': clients, 'constructionitems': constructionitems})

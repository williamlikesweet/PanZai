from django.shortcuts import render


def start_document(request):
    return render(request, 'polls/starter.html')







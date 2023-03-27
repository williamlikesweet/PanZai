from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required(login_url="Login")
def start_document(request):
    return render(request, 'hongmingstone/starter.html')







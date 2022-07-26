from django.urls import path
from . import views

urlpatterns = [
    path('start_document', views.start_document, name='start_document'),
    path('index', views.index, name='index'),
    path('worker', views.worker, name='worker'),
    path('worker/create', views.workercreate, name='workercreate'),
]
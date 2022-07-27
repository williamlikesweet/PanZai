from django.urls import path
from . import views

urlpatterns = [
    path('start_document', views.start_document, name='start_document'),

    path('index', views.index, name='index'),
    path('index/create', views.indexcreate, name='indexcreate'),

    path('worker', views.worker, name='worker'),
    path('worker/create', views.workercreate, name='workercreate'),

    path('client', views.client, name='client'),
    path('client/create', views.clientcreate, name='clientcreate'),
]
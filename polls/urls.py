from django.urls import path
from polls import views

urlpatterns = [
    path('start_document', views.start_document, name='start_document'),

    path('index', views.index, name='index'),
    path('index/create', views.indexcreate, name='indexcreate'),

    path('constructionitem', views.constructionItem, name='constructionitem'),
    path('constructionitem/create', views.constructionItemCreate, name='constructionitem_create'),

    path('worker', views.worker, name='worker'),
    path('worker/create', views.workercreate, name='workercreate'),

    path('client', views.client, name='client'),
    path('client/create', views.clientcreate, name='clientcreate'),
]
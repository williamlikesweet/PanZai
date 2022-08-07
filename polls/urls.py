from django.urls import path
from polls import views
from .Views import WorkerView, ClientView, ConstructionView, ConstructionItemView

urlpatterns = [
    path('start_document', views.start_document, name='start_document'),

    path('construction', ConstructionView.construction, name='construction'),
    path('construction/create', ConstructionView.constructionCreate, name='construction_create'),

    path('constructionitem', ConstructionItemView.constructionItem, name='constructionitem'),
    path('constructionitem/create', ConstructionItemView.constructionItemCreate, name='constructionitem_create'),

    path('worker', WorkerView.worker, name='worker'),
    path('worker/create', WorkerView.workerCreate, name='worker_create'),

    path('client', ClientView.ClientList.as_view(), name='client'),
    path('client/create', ClientView.ClientCreate.as_view(), name='client_create'),
    path('client/edit/<int:pk>', ClientView.ClientUpdate.as_view(), name='client_edit'),
    path('client/delete/<int:pk>', ClientView.ClientDelete.as_view(), name='client_delete'),

]

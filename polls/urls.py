from django.urls import path
from polls import views
from .Views import WorkerView, ClientView, ConstructionView, ConstructionItemView

urlpatterns = [
    path('start_document', views.start_document, name='start_document'),

    path('construction', ConstructionView.ConstructionList.as_view(), name='construction'),
    path('construction/create', ConstructionView.ConstructionCreate.as_view(), name='construction_create'),
    path('construction/edit/<int:pk>', ConstructionView.ConstructionUpdate.as_view(), name='construction_edit'),

    path('constructionitem', ConstructionItemView.constructionItem, name='constructionitem'),
    path('constructionitem/create', ConstructionItemView.constructionItemCreate, name='constructionitem_create'),

    path('worker', WorkerView.WorkerList.as_view(), name='worker'),
    path('worker/create', WorkerView.WorkerCreate.as_view(), name='worker_create'),
    path('worker/edit/<int:pk>', WorkerView.WorkerUpdate.as_view(), name='worker_edit'),

    path('client', ClientView.ClientList.as_view(), name='client'),
    path('client/create', ClientView.ClientCreate.as_view(), name='client_create'),
    path('client/edit/<int:pk>', ClientView.ClientUpdate.as_view(), name='client_edit'),
    path('client/delete/<int:pk>', ClientView.ClientDelete.as_view(), name='client_delete'),
    path('client/import', ClientView.ClientImport, name='client_import'),

]

from django.urls import path
from polls import views
from .Views import WorkerView, ClientView, ConstructionView, ConstructionItemView, TotalAmountView

urlpatterns = [
    path('start_document', views.start_document, name='start_document'),

    path('construction', ConstructionView.ConstructionList.as_view(), name='construction'),
    path('construction/create', ConstructionView.ConstructionCreate.as_view(), name='construction_create'),
    path('construction/edit/<int:pk>', ConstructionView.ConstructionUpdate.as_view(), name='construction_edit'),
    path('construction/delete/<int:pk>', ConstructionView.ConstructionDelete.as_view(), name='construction_delete'),
    path('construction/import', ConstructionView.ConstructionImport, name='construction_import'),

    path('batch', ConstructionView.BatchConstruction.as_view(), name='batch'),
    path('batch/delete/<created_at>', ConstructionView.delete, name='batch_delete'),

    path('constructionitem', ConstructionItemView.ConstructionItemList.as_view(), name='constructionitem'),
    path('constructionitem/create', ConstructionItemView.ConstructionItemCreate.as_view(), name='constructionitem_create'),
    path('constructionitem/edit/<int:pk>', ConstructionItemView.ConstructionItemUpdate.as_view(), name='constructionitem_edit'),

    path('worker', WorkerView.WorkerList.as_view(), name='worker'),
    path('worker/create', WorkerView.WorkerCreate.as_view(), name='worker_create'),
    path('worker/edit/<int:pk>', WorkerView.WorkerUpdate.as_view(), name='worker_edit'),
    path('worker/<worker_id>', WorkerView.worker_datail, name="worker_detail"),
    # path('worker/<int:pk>', WorkerView.worker_datail, name="worker_detail"),
    # path('worker/<slug:isbn>', WorkerView.WorkerDetailView.as_view(), name="worker_detail"),

    path('client', ClientView.ClientList.as_view(), name='client'),
    path('client/create', ClientView.ClientCreate.as_view(), name='client_create'),
    path('client/edit/<int:pk>', ClientView.ClientUpdate.as_view(), name='client_edit'),
    path('client/delete/<int:pk>', ClientView.ClientDelete.as_view(), name='client_delete'),
    path('client/import', ClientView.ClientImport, name='client_import'),

    path('Amount/client', TotalAmountView.ClientAmount.as_view(), name='client_Amount'),
    path('Amount/worker', TotalAmountView.WorkerAmount.as_view(), name='worker_Amount'),

]

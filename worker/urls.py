from django.urls import path
from worker import views

urlpatterns = [
    path('worker', views.WorkerList.as_view(), name='worker'),
    path('worker/create', views.WorkerCreate.as_view(), name='worker_create'),
    path('worker/edit/<int:pk>', views.WorkerUpdate.as_view(), name='worker_edit'),
    path('worker/<worker_id>', views.Worker_datail, name="worker_detail"),
    # path('worker/<int:pk>', WorkerView.worker_datail, name="worker_detail"),
    # path('worker/<slug:isbn>', WorkerView.WorkerDetailView.as_view(), name="worker_detail"),
]

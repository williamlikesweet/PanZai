from django.urls import path
from worker import views

urlpatterns = [
    path('worker', views.WorkerList.as_view(), name='worker'),

]

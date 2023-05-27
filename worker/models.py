from django.db import models
from django import forms
from hongmingstone.enums.EnumWorker import EnumWorker


class Worker(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    status = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_worker'


class WorkerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorkerForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = 1

    class Meta:
        model = Worker
        fields = ['name', 'status']
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "status": forms.RadioSelect(choices=EnumWorker.CHOICES.value)
        }

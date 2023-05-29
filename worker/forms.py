from django import forms
from .models import Worker
from hongmingstone.enums.EnumWorker import EnumWorker
from .serializers import WorkerSerializer


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

from import_export import resources
from polls.models import Client, Construction


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client


class ConstructionResource(resources.ModelResource):
    class Meta:
        model = Construction

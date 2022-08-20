from import_export import resources
from import_export.widgets import DateWidget

from polls.models import Client, Construction
from import_export.fields import Field


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client


class ConstructionResource(resources.ModelResource):
    publish_at = Field(attribute='publish_at', column_name='publish_at', widget=DateWidget('%Y-%m-%d'))

    class Meta:
        model = Construction
        fields = (
            'id',
            'worker',
            'client',
            'constructionItem',
            'work_site',
            'construction_length',
            'construction_unit',
            'construction_split',
            'construction_amount,',
            'publish_at',
        )

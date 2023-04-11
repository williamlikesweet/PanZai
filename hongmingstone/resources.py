from import_export import resources, fields
from import_export.widgets import DateWidget
from hongmingstone.models import Client, Construction
from import_export.fields import Field
from hongmingstone.repository.ConstructionRepository import valueTransformKey


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
        import_id_fields = ('name',)


class ConstructionResource(resources.ModelResource):
    publish_at = Field(attribute='publish_at', column_name='publish_at', widget=DateWidget('%Y-%m-%d'))
    batchID = fields.Field(attribute='batchID', column_name='batchID')

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
            'construction_amount',
            'publish_at',
            'batchID',
        )

    def before_import_row(self, row, **kwargs):
        request = kwargs.get('request')
        if request:
            row['batchID'] = request['batchID']
            row['worker'] = request['worker_name']
        row = valueTransformKey(row)
        return super().before_import_row(row, dry_run=False, raise_errors=True, use_transactions=True, **kwargs)

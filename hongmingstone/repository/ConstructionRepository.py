from hongmingstone.models import Client, Worker, ConstructionItem, Construction


def batchIdAdd():
    # batchID = 0
    result = Construction.objects.all()
    last_obj = result.values_list('batchID', flat=True).last() or 0

    if last_obj == 0:
        batchID = 1
    else:
        batchID = int(last_obj) + 1
    return batchID


def valueTransformKey(row):
    _client = row.get('client')
    _worker = row.get('worker')
    _constructionItem = row.get('constructionItem')
    if _client:
        try:
            client_id = Client.objects.filter(name=_client).values().get()
            row['client'] = client_id['id']
        except Client.DoesNotExist:
            pass
    if _worker:
        try:
            worker_id = Worker.objects.filter(name=_worker).values().get()
            row['worker'] = worker_id['id']
        except Worker.DoesNotExist:
            pass
    if _constructionItem:
        try:
            constructionItem_id = ConstructionItem.objects.filter(item=_constructionItem).values().get()
            row['constructionItem'] = constructionItem_id['id']
        except ConstructionItem.DoesNotExist:
            pass
    return row

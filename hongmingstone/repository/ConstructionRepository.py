from hongmingstone.models import Construction


def batchIdAdd():
    # batchID = 0
    result = Construction.objects.all()
    last_obj = result.values_list('batchID', flat=True).last() or 0

    if last_obj == 0:
        batchID = 1
    else:
        batchID = int(last_obj) + 1
    return batchID


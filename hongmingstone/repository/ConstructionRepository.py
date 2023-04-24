from hongmingstone.models import Client, Worker, ConstructionItem, Construction
import pandas as pd
import numpy as np

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

def preprocess_group(group):
    group = group.dropna(axis=0, how='all')
    group.insert(group.columns.get_loc(group.columns[0]), '品項', group.columns[0])
    split_cols = group.filter(regex='拆分').columns.tolist()
    if not split_cols:
        group.insert(group.columns.get_loc(group.columns[3]), '拆分', '')
    group = group.reset_index()
    group.columns = ['client', 'work_site', 'constructionItem', 'construction_length', 'construction_unit',
                     'construction_split', 'construction_amount']
    return group


def preprocess_df(df):
    df = df.replace(0, np.nan, inplace=False)
    df = df.drop(df.columns[-1], axis=1)
    group_1 = df.iloc[0:, 0:3]
    group_2 = df.iloc[0:, 3:6]
    group_3 = df.iloc[0:, 6:9]
    group_4 = df.iloc[0:, 13:17]
    group_5 = df.iloc[0:, 17:21]
    multiplex_colums = group_1.columns[:].append(group_2.columns[:]).append(group_3.columns[:]).append(
        group_4.columns[:]).append(group_5.columns[:])
    df = df.drop(columns=multiplex_colums.tolist())

    group_1 = preprocess_group(group_1)
    group_2 = preprocess_group(group_2)
    group_3 = preprocess_group(group_3)
    group_4 = preprocess_group(group_4)
    group_5 = preprocess_group(group_5)

    df = df.stack().reset_index()
    df.insert(df.columns.get_loc(df.columns[3]), '長度', '')
    df['拆分'] = ''
    df['總額'] = df[df.columns[4]]
    df.columns = ['client', 'work_site', 'constructionItem', 'construction_length', 'construction_unit',
                  'construction_split', 'construction_amount']

    resultDate = pd.concat([df, group_1, group_2, group_3, group_4, group_5], axis=0)
    return resultDate
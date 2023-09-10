from rest_framework import serializers
from .models import Worker
from hongmingstone.models import Construction, ConstructionItem, Client


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['name', 'status']


class WorkerDetailSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='clients.name')
    item_name = serializers.CharField(source='constructionItems.item')

    class Meta:
        model = Construction

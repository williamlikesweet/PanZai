from django.db import models
from django.urls import reverse


class Worker(models.Model):
    name = models.CharField(max_length=30, null=False)
    status = models.IntegerField(max_length=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_worker'


class Client(models.Model):
    name = models.CharField(max_length=30, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_client'


class ConstructionItem(models.Model):
    item = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item

    class Meta:
        db_table = 'tb_constructionitem'


class Construction(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='workers')
    constructionItem = models.ForeignKey(ConstructionItem, on_delete=models.CASCADE, related_name='constructionItems')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='clients')
    work_site = models.CharField(max_length=200, null=True)
    construction_length = models.FloatField(null=True)
    construction_unit = models.FloatField(null=True)
    construction_split = models.FloatField(null=True)
    construction_amount = models.FloatField(null=True)
    publish_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        ordering = ['publish_at']
        return

    class Meta:
        db_table = 'tb_construction'

    def get_absolute_url(self):
        return reverse('construction_edit', kwargs={'pk': self.pk})

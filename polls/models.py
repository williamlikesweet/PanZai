from django.db import models
from django.urls import reverse


class Worker(models.Model):
    name = models.CharField('師傅', max_length=30)
    status = models.IntegerField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_worker'


class Client(models.Model):
    name = models.CharField('客戶名稱', max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_client'


class Construction(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='worker')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client')
    work_site = models.CharField(max_length=200, null=True)
    construction_item = models.CharField(max_length=200, null=True)
    construction_cm = models.FloatField(null=True)
    construction_unit = models.FloatField(null=True)
    construction_split = models.FloatField(null=True)
    publish_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        ordering = ['publish_at']
        return

    class Meta:
        db_table = 'tb_construction'

    def get_absolute_url(self):
        return reverse('construction_edit', kwargs={'pk': self.pk})


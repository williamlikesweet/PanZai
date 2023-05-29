from django.db import models


class Worker(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    status = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_worker'





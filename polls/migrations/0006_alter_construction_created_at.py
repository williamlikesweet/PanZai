# Generated by Django 4.0.6 on 2022-09-25 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_alter_construction_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='construction',
            name='created_at',
            field=models.DateTimeField(default='2022-09-25 16:26:58', null=True),
        ),
    ]

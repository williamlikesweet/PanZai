# Generated by Django 4.0.6 on 2022-09-25 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_alter_construction_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='construction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

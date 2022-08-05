# Generated by Django 4.0.6 on 2022-08-03 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tb_client',
            },
        ),
        migrations.CreateModel(
            name='ConstructionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tb_constructionitem',
            },
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('status', models.IntegerField(max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tb_worker',
            },
        ),
        migrations.CreateModel(
            name='Construction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_site', models.CharField(max_length=200, null=True)),
                ('construction_length', models.FloatField(null=True)),
                ('construction_unit', models.FloatField(null=True)),
                ('construction_split', models.FloatField(null=True)),
                ('construction_amount', models.FloatField(null=True)),
                ('publish_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='polls.client')),
                ('constructionItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='constructionItems', to='polls.constructionitem')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workers', to='polls.worker')),
            ],
            options={
                'db_table': 'tb_construction',
            },
        ),
    ]
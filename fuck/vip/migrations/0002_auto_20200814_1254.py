# Generated by Django 2.1.8 on 2020-08-14 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vip', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vip',
            options={'ordering': ['level']},
        ),
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='权限名'),
        ),
    ]

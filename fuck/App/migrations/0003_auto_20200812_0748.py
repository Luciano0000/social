# Generated by Django 2.1.8 on 2020-08-12 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_day',
            field=models.IntegerField(default=1, verbose_name='出生日'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_month',
            field=models.IntegerField(default=1, verbose_name='出生月'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_year',
            field=models.IntegerField(default=2000, verbose_name='出生年'),
        ),
    ]

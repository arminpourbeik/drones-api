# Generated by Django 3.1.4 on 2020-12-17 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drones', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dronecategory',
            options={'ordering': ('name',), 'verbose_name_plural': 'Drone Categories'},
        ),
        migrations.AlterField(
            model_name='drone',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='dronecategory',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='pilot',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]

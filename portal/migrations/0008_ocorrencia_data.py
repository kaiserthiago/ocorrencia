# Generated by Django 2.0 on 2017-12-22 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_auto_20171222_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='ocorrencia',
            name='data',
            field=models.DateField(default='2017-12-22'),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.0 on 2018-03-15 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0013_auto_20180314_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='siape',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.0.4 on 2018-09-27 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0033_auto_20180822_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='img_alunos'),
        ),
    ]
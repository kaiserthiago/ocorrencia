# Generated by Django 2.0.4 on 2018-10-05 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0042_aluno_contato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encaminhamento',
            name='data',
            field=models.DateField(blank=True, null=True),
        ),
    ]
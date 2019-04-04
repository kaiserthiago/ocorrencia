# Generated by Django 2.0.4 on 2019-04-03 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0002_ocorrencia_disciplina'),
    ]

    operations = [
        migrations.AddField(
            model_name='ocorrencia',
            name='responsavel_retorno_ocorrencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='responsavel_retorno_ocorrencia', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ocorrencia',
            name='status',
            field=models.CharField(choices=[('Registrada', 'Registrada'), ('Retornada', 'Retornada')], default='Registrada', max_length=30),
        ),
        migrations.AlterField(
            model_name='matricula',
            name='ano_letivo',
            field=models.IntegerField(default=2019),
        ),
    ]
# Generated by Django 2.0.4 on 2018-08-22 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0028_auto_20180807_1327'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='configuracao',
            options={'verbose_name_plural': 'Configurações do sistema'},
        ),
        migrations.RemoveField(
            model_name='encaminhamento',
            name='analise',
        ),
        migrations.RemoveField(
            model_name='encaminhamento',
            name='responsavel_analise',
        ),
        migrations.AddField(
            model_name='encaminhamento',
            name='responsavel_providencias',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='responsavel_providencias', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 2.0.4 on 2018-06-20 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0019_auto_20180424_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encaminhamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('data', models.DateField()),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('providencias', models.TextField()),
                ('outras_informacoes', models.TextField()),
                ('analise', models.TextField()),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='portal.Empresa')),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='portal.Matricula')),
                ('responsavel_analise', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='responsavel_analise', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Encaminhamentos',
                'ordering': ['-data', 'matricula__aluno'],
            },
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('descricao', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Serviços',
                'ordering': ['descricao'],
            },
        ),
        migrations.CreateModel(
            name='ServicoCategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('descricao', models.CharField(max_length=255)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='portal.Empresa')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categorias de serviços',
                'ordering': ['descricao'],
            },
        ),
        migrations.AddField(
            model_name='servico',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='portal.ServicoCategoria'),
        ),
        migrations.AddField(
            model_name='servico',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='portal.Empresa'),
        ),
        migrations.AddField(
            model_name='servico',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='encaminhamento',
            name='servico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='portal.Servico'),
        ),
        migrations.AddField(
            model_name='encaminhamento',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
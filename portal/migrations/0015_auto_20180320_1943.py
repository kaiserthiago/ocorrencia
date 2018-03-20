# Generated by Django 2.0.3 on 2018-03-20 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0014_userprofile_siape'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curso',
            options={'ordering': ['descricao']},
        ),
        migrations.RenameField(
            model_name='empresa',
            old_name='email_responsavel',
            new_name='email_responsavel_ocorrencia',
        ),
        migrations.RenameField(
            model_name='empresa',
            old_name='responsavel',
            new_name='email_responsavel_sistema',
        ),
        migrations.AddField(
            model_name='empresa',
            name='responsavel_ocorrencia',
            field=models.CharField(default='CGTI', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresa',
            name='responsavel_sistema',
            field=models.CharField(default='cgti.cacoal@ifro.edu.br', max_length=150),
            preserve_default=False,
        ),
    ]

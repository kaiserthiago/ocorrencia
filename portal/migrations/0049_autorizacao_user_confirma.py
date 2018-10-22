# Generated by Django 2.0.4 on 2018-10-22 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0048_auto_20181019_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='autorizacao',
            name='user_confirma',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_confirma', to=settings.AUTH_USER_MODEL),
        ),
    ]
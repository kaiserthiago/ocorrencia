from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

from portal.models import Empresa
from . import views

usuario = Empresa.objects.all().order_by('nome_fantasia')

urlpatterns = [
    url(r'^register$', views.register, name='login_register'),
    url(r'^register/success$', views.register_success, name='login_register_success'),
    url(r'^login$', auth_views.login, {'extra_context':{'unidades': usuario}}, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': '/'}, name='logout'),
]
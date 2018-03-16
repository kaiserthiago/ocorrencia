from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^contato$', views.contato, name='contato'),

    url(r'^ocorrencia/relatorio$', views.ocorrencia_relatorio, name='ocorrencia_relatorio'),
    url(r'^ocorrencia/register$', views.ocorrencia_register, name='ocorrencia_register'),
    url(r'^ocorrencia/show/(?P<ocorrencia_id>\d+)$', views.ocorrencia_show, name='ocorrencia_show'),
    url(r'^ocorrencia/new$', views.ocorrencia_new, name='ocorrencia_new'),
    url(r'^ocorrencia$', views.ocorrencia, name='ocorrencia'),

    url(r'^aluno/delete/(?P<aluno_id>\d+)$', views.aluno_delete, name='aluno_delete'),
    url(r'^aluno/edit/(?P<aluno_id>\d+)$', views.aluno_edit, name='aluno_edit'),
    url(r'^aluno/new$', views.aluno_new, name='aluno_new'),
    url(r'^aluno$', views.aluno, name='aluno'),

    url(r'^curso/delete/(?P<curso_id>\d+)$', views.curso_delete, name='curso_delete'),
    url(r'^curso/edit/(?P<curso_id>\d+)$', views.curso_edit, name='curso_edit'),
    url(r'^curso/new$', views.curso_new, name='curso_new'),
    url(r'^curso$', views.curso, name='curso'),

    url(r'^turma/delete/(?P<turma_id>\d+)$', views.turma_delete, name='turma_delete'),
    url(r'^turma/edit/(?P<turma_id>\d+)$', views.turma_edit, name='turma_edit'),
    url(r'^turma/new$', views.turma_new, name='turma_new'),
    url(r'^turma$', views.turma, name='turma'),

    url(r'^matricula/delete/(?P<matricula_id>\d+)$', views.matricula_delete, name='matricula_delete'),
    url(r'^matricula/edit/(?P<matricula_id>\d+)$', views.matricula_edit, name='matricula_edit'),
    url(r'^matricula/new$', views.matricula_new, name='matricula_new'),
    url(r'^matricula$', views.matricula, name='matricula'),

    url(r'^import/matricula$', views.import_matricula, name='import_matricula'),
    url(r'^import/aluno$', views.import_aluno, name='import_aluno'),
]
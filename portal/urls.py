from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.home, name='home'),

    url('^contato$', views.contato, name='contato'),

    url('^dashboard$', views.dashboard, name='dashboard'),

    url('^ocorrencia/relatorio/(?P<aluno_id>\d+)$', views.ocorrencia_relatorio, name='ocorrencia_relatorio'),
    url('^ocorrencia/register$', views.ocorrencia_register, name='ocorrencia_register'),
    url('^ocorrencia/delete/(?P<ocorrencia_id>\d+)$', views.ocorrencia_delete, name='ocorrencia_delete'),
    url('^ocorrencia/show/(?P<ocorrencia_id>\d+)$', views.ocorrencia_show, name='ocorrencia_show'),
    url('^ocorrencia/new$', views.ocorrencia_new, name='ocorrencia_new'),
    url('^ocorrencia$', views.ocorrencia, name='ocorrencia'),

    url('^aluno/delete/(?P<aluno_id>\d+)', views.aluno_delete, name='aluno_delete'),
    url('^aluno/edit/(?P<aluno_id>\d+)$', views.aluno_edit, name='aluno_edit'),
    url('^aluno/new$', views.aluno_new, name='aluno_new'),
    url('^aluno$', views.aluno, name='aluno'),

    url('^curso/delete/(?P<curso_id>\d+)$', views.curso_delete, name='curso_delete'),
    url('^curso/edit/(?P<curso_id>\d+)$', views.curso_edit, name='curso_edit'),
    url('^curso/new$', views.curso_new, name='curso_new'),
    url('^curso$', views.curso, name='curso'),

    url('^turma/delete/(?P<turma_id>\d+)$', views.turma_delete, name='turma_delete'),
    url('^turma/edit/(?P<turma_id>\d+)$', views.turma_edit, name='turma_edit'),
    url('^turma/new$', views.turma_new, name='turma_new'),
    url('^turma$', views.turma, name='turma'),

    url('^matricula/delete/(?P<matricula_id>\d+)$', views.matricula_delete, name='matricula_delete'),
    url('^matricula/edit/(?P<matricula_id>\d+)$', views.matricula_edit, name='matricula_edit'),
    url('^matricula/new$', views.matricula_new, name='matricula_new'),
    url('^matricula$', views.matricula, name='matricula'),

    url('^import/matricula$', views.import_matricula, name='import_matricula'),
    url('^import/aluno$', views.import_aluno, name='import_aluno'),

    url(r'^usuario/desativar/(?P<user_id>\d+)$', views.usuario_desativar, name='usuario_desativar'),
    url(r'^usuario/ativar/(?P<user_id>\d+)$', views.usuario_ativar, name='usuario_ativar'),
    url(r'^usuario/lista$', views.usuario_lista, name='usuario_lista'),
    url(r'^usuario/conta', views.usuario_conta, name='usuario_conta'),

]

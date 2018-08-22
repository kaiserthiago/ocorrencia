from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.home, name='home'),

    url('^contato$', views.contato, name='contato'),

    url('^configuracao', views.configuracao, name='configuracao'),

    url('^dashboard$', views.dashboard, name='dashboard'),

    url('^ocorrencia/relatorio/(?P<aluno_id>\d+)$', views.ocorrencia_relatorio, name='ocorrencia_relatorio'),
    url('^ocorrencia/relatorio/aluno$', views.ocorrencia_relatorio_aluno, name='ocorrencia_relatorio_aluno'),
    url('^ocorrencia/register$', views.ocorrencia_register, name='ocorrencia_register'),
    url('^ocorrencia/delete/(?P<ocorrencia_id>\d+)$', views.ocorrencia_delete, name='ocorrencia_delete'),
    url('^ocorrencia/show/(?P<ocorrencia_id>\d+)$', views.ocorrencia_show, name='ocorrencia_show'),
    url('^ocorrencia/new$', views.ocorrencia_new, name='ocorrencia_new'),
    url('^ocorrencia$', views.ocorrencia, name='ocorrencia'),

    url('^encaminhamento/relatorio/(?P<aluno_id>\d+)$', views.encaminhamento_relatorio,
        name='encaminhamento_relatorio'),
    url('^encaminhamento/relatorio/aluno$', views.encaminhamento_relatorio_aluno, name='encaminhamento_relatorio_aluno'),
    url('^encaminhamento/register$', views.encaminhamento_register, name='encaminhamento_register'),
    url('^encaminhamento/delete/(?P<encaminhamento_id>\d+)$', views.encaminhamento_delete,
        name='encaminhamento_delete'),
    url('^encaminhamento/show/(?P<encaminhamento_id>\d+)$', views.encaminhamento_show, name='encaminhamento_show'),
    url('^encaminhamento/new$', views.encaminhamento_new, name='encaminhamento_new'),
    url('^encaminhamento/pendente$', views.encaminhamento_pendente, name='encaminhamento_pendente'),
    url('^encaminhamento/providencia/(?P<encaminhamento_id>\d+)$', views.encaminhamento_providencia, name='encaminhamento_providencia'),
    url('^encaminhamento$', views.encaminhamento, name='encaminhamento'),

    url('^autorizacao/relatorio/(?P<aluno_id>\d+)$', views.autorizacao_relatorio, name='autorizacao_relatorio'),
    url('^autorizacao/relatorio/aluno$', views.autorizacao_relatorio_aluno, name='autorizacao_relatorio_aluno'),
    url('^autorizacao/register$', views.autorizacao_register, name='autorizacao_register'),
    url('^autorizacao/delete/(?P<autorizacao_id>\d+)$', views.autorizacao_delete, name='autorizacao_delete'),
    url('^autorizacao/show/(?P<autorizacao_id>\d+)$', views.autorizacao_show, name='autorizacao_show'),
    url('^autorizacao/confirmar/(?P<autorizacao_id>\d+)$', views.autorizacao_confirmar, name='autorizacao_confirmar'),
    url('^autorizacao/pendente$', views.autorizacao_pendente, name='autorizacao_pendente'),
    url('^autorizacao/new$', views.autorizacao_new, name='autorizacao_new'),
    url('^autorizacao$', views.autorizacao, name='autorizacao'),

    url('^aluno/delete/(?P<aluno_id>\d+)$', views.aluno_delete, name='aluno_delete'),
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
    url(r'^user/account/change$', views.user_change_password, name='user_change_password'),
    url(r'^user/account$', views.user_account, name='user_account'),
    url(r'^user/list$', views.user_list, name='user_list'),

    url(r'^report/autorizacao/aluno/(?P<aluno_id>\d+)$', views.report_autorizacao_saida_aluno, name='report_autorizacao_saida_aluno'),
    url(r'^report/autorizacao/curso$', views.report_autorizacao_saida_curso, name='report_autorizacao_saida_curso'),
    url(r'^report/autorizacao/turma$', views.report_autorizacao_saida_turma, name='report_autorizacao_saida_turma'),

    url(r'^report/encaminhamento/aluno/(?P<aluno_id>\d+)$', views.report_encaminhamento_aluno, name='report_encaminhamento_aluno'),
    url(r'^report/encaminhamento/curso', views.report_encaminhamento_curso, name='report_encaminhamento_curso'),
    url(r'^report/encaminhamento/turma$', views.report_encaminhamento_turma, name='report_encaminhamento_turma'),

    url(r'^report/ocorrencia/aluno/(?P<aluno_id>\d+)$', views.report_ocorrencia_aluno, name='report_ocorrencia_aluno'),
    url(r'^report/ocorrencia/curso', views.report_ocorrencia_curso, name='report_ocorrencia_curso'),
    url(r'^report/ocorrencia/turma$', views.report_ocorrencia_turma, name='report_ocorrencia_turma'),

    url(r'^report/general$', views.report_general, name='report_general'),

    url('^servico/categoria/delete/(?P<servico_categoria_id>\d+)$', views.servico_categoria_delete,
        name='servico_categoria_delete'),
    url('^servico/categoria/edit/(?P<servico_categoria_id>\d+)$', views.servico_categoria_edit,
        name='servico_categoria_edit'),
    url('^servico/categoria/new$', views.servico_categoria_new, name='servico_categoria_new'),
    url('^servico/categoria$', views.servico_categoria, name='servico_categoria'),

    url('^servico/delete/(?P<servico_id>\d+)$', views.servico_delete, name='servico_delete'),
    url('^servico/edit/(?P<servico_id>\d+)$', views.servico_edit, name='servico_edit'),
    url('^servico/new$', views.servico_new, name='servico_new'),
    url('^servico$', views.servico, name='servico'),

]

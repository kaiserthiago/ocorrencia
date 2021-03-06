from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^validar$', views.validar_declaracao_matricula, name='validar_declaracao_matricula'),

    url(r'^configuracao', views.configuracao, name='configuracao'),

    url(r'^dashboard$', views.dashboard, name='dashboard'),

    url(r'^justificativa/solicitar/(?P<matricula_id>\d+)$', views.justificativa_solicitar, name='justificativa_solicitar'),
    url(r'^justificativa/indeferir/(?P<justificativa_id>\d+)$', views.justificativa_indeferimento, name='justificativa_indeferimento'),
    url(r'^justificativa/deferir/(?P<justificativa_id>\d+)$', views.justificativa_deferimento, name='justificativa_deferimento'),
    url(r'^justificativa/pendente$', views.justificativa_pendente, name='justificativa_pendente'),
    url(r'^justificativa$', views.justificativa, name='justificativa'),

    url(r'^ocorrencia/relatorio/(?P<aluno_id>\d+)$', views.ocorrencia_relatorio, name='ocorrencia_relatorio'),
    url(r'^ocorrencia/relatorio/aluno$', views.ocorrencia_relatorio_aluno, name='ocorrencia_relatorio_aluno'),
    url(r'^ocorrencia/providencia/(?P<ocorrencia_id>\d+)$', views.ocorrencia_providencia, name='ocorrencia_providencia'),
    url(r'^ocorrencia/register$', views.ocorrencia_register, name='ocorrencia_register'),
    url(r'^ocorrencia/pendente$', views.ocorrencia_pendente, name='ocorrencia_pendente'),
    url(r'^ocorrencia/delete/(?P<ocorrencia_id>\d+)$', views.ocorrencia_delete, name='ocorrencia_delete'),
    url(r'^ocorrencia/(?P<turma_id>\d+)/new$', views.ocorrencia_new, name='ocorrencia_new'),
    url(r'^ocorrencia$', views.ocorrencia, name='ocorrencia'),

    url(r'^encaminhamento/relatorio/(?P<aluno_id>\d+)$', views.encaminhamento_relatorio, name='encaminhamento_relatorio'),
    url(r'^encaminhamento/relatorio/aluno$', views.encaminhamento_relatorio_aluno, name='encaminhamento_relatorio_aluno'),
    url(r'^encaminhamento/providencia/(?P<encaminhamento_id>\d+)$', views.encaminhamento_providencia, name='encaminhamento_providencia'),
    url(r'^encaminhamento/solicitar/(?P<matricula_id>\d+)$', views.encaminhamento_solicitar, name='encaminhamento_solicitar'),
    url(r'^encaminhamento/delete/(?P<encaminhamento_id>\d+)$', views.encaminhamento_delete, name='encaminhamento_delete'),
    url(r'^encaminhamento/register$', views.encaminhamento_register, name='encaminhamento_register'),
    url(r'^encaminhamento/pendente$', views.encaminhamento_pendente, name='encaminhamento_pendente'),
    url(r'^encaminhamento/(?P<turma_id>\d+)/new$', views.encaminhamento_new, name='encaminhamento_new'),
    url(r'^encaminhamento$', views.encaminhamento, name='encaminhamento'),

    url(r'^autorizacao/relatorio/(?P<aluno_id>\d+)$', views.autorizacao_relatorio, name='autorizacao_relatorio'),
    url(r'^autorizacao/relatorio/aluno$', views.autorizacao_relatorio_aluno, name='autorizacao_relatorio_aluno'),
    url(r'^autorizacao/register$', views.autorizacao_register, name='autorizacao_register'),
    url(r'^autorizacao/delete/(?P<autorizacao_id>\d+)$', views.autorizacao_delete, name='autorizacao_delete'),
    url(r'^autorizacao/show/(?P<autorizacao_id>\d+)$', views.autorizacao_show, name='autorizacao_show'),
    url(r'^autorizacao/confirmar/(?P<autorizacao_id>\d+)$', views.autorizacao_confirmar, name='autorizacao_confirmar'),
    url(r'^autorizacao/pendente$', views.autorizacao_pendente, name='autorizacao_pendente'),
    url(r'^autorizacao/(?P<turma_id>\d+)new$', views.autorizacao_new, name='autorizacao_new'),
    url(r'^autorizacao$', views.autorizacao, name='autorizacao'),

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
    url(r'^import/aluno/atualizar', views.import_aluno_atualizar, name='import_aluno_atualizar'),
    url(r'^import/aluno$', views.import_aluno, name='import_aluno'),

    url(r'^usuario/ativar/(?P<user_id>\d+)$', views.usuario_ativar, name='usuario_ativar'),
    url(r'^usuario/negar/(?P<user_id>\d+)$', views.usuario_negar, name='usuario_negar'),
    url(r'^user/account/change$', views.user_change_password, name='user_change_password'),
    url(r'^user/account$', views.user_account, name='user_account'),

    url(r'^perfil/aluno/(?P<aluno_id>\d+)/edit/pagina/(?P<page>\d+)/turma/(?P<turma>\d+)$', views.aluno_perfil_edit, name='aluno_perfil_edit'),
    url(r'^perfil/aluno/(?P<aluno_id>\d+)$', views.perfil_individual, name='perfil_individual'),
    url(r'^perfil/turma/(?P<turma_id>\d+)$', views.perfil_turma, name='perfil_turma'),
    url(r'^perfil$', views.perfil, name='perfil'),

    url(r'^report/pdf/justificativa/(?P<justificativa_id>\d+)$', views.report_pdf_justificativa, name='report_pdf_justificativa'),

    url(r'^report/autorizacao/aluno/(?P<aluno_id>\d+)$', views.report_autorizacao_saida_aluno, name='report_autorizacao_saida_aluno'),
    url(r'^report/autorizacao/curso$', views.report_autorizacao_saida_curso, name='report_autorizacao_saida_curso'),
    url(r'^report/autorizacao/turma$', views.report_autorizacao_saida_turma, name='report_autorizacao_saida_turma'),

    url(r'^report/encaminhamento/aluno/(?P<aluno_id>\d+)$', views.report_encaminhamento_aluno, name='report_encaminhamento_aluno'),
    url(r'^report/encaminhamento/curso', views.report_encaminhamento_curso, name='report_encaminhamento_curso'),
    url(r'^report/encaminhamento/turma$', views.report_encaminhamento_turma, name='report_encaminhamento_turma'),

    url(r'^report/ocorrencia/aluno/(?P<aluno_id>\d+)$', views.report_ocorrencia_aluno, name='report_ocorrencia_aluno'),
    url(r'^report/ocorrencia/curso', views.report_ocorrencia_curso, name='report_ocorrencia_curso'),
    url(r'^report/ocorrencia/turma$', views.report_ocorrencia_turma, name='report_ocorrencia_turma'),

    url(r'^report/pdf/financeiro/turma$', views.report_pdf_dados_bancarios, name='report_pdf_dados_bancarios'),
    url(r'^report/pdf/lista/usuarios', views.report_pdf_lista_usuarios, name='report_pdf_lista_usuarios'),
    url(r'^report/pdf/lista/turma$', views.report_pdf_lista_aluno_turma, name='report_pdf_lista_aluno_turma'),
    url(r'^report/pdf/aluno/pcd', views.report_pdf_lista_aluno_pcd, name='report_pdf_lista_aluno_pcd'),

    url(r'^report/pdf/encaminhamento/(?P<encaminhamento_id>\d+)$', views.report_pdf_encaminhamento, name='report_pdf_encaminhamento'),
    url(r'^report/pdf/autorizacao/(?P<autorizacao_id>\d+)$', views.report_pdf_autorizacao, name='report_pdf_autorizacao'),
    url(r'^report/pdf/ocorrencia/(?P<ocorrencia_id>\d+)$', views.report_pdf_ocorrencia, name='report_pdf_ocorrencia'),
    url(r'^report/pdf/conclusao/integrado', views.report_pdf_declaracao_conclusao_integrado, name='report_pdf_declaracao_conclusao_integrado'),
    url(r'^report/pdf/transferencia$', views.report_pdf_declaracao_transferencia, name='report_pdf_declaracao_transferencia'),
    url(r'^report/pdf/matricula$', views.report_pdf_declaracao_matricula, name='report_pdf_declaracao_matricula'),
    url(r'^report/pdf/sabado$', views.report_pdf_declaracao_sabado_letivo, name='report_pdf_declaracao_sabado_letivo'),

    url(r'^report/xls/aluno$', views.report_aluno_xls, name='report_aluno_xls'),

    url(r'^report/general$', views.report_general, name='report_general'),

    url(r'^servico/categoria/delete/(?P<servico_categoria_id>\d+)$', views.servico_categoria_delete,
        name='servico_categoria_delete'),
    url(r'^servico/categoria/edit/(?P<servico_categoria_id>\d+)$', views.servico_categoria_edit,
        name='servico_categoria_edit'),
    url(r'^servico/categoria/new$', views.servico_categoria_new, name='servico_categoria_new'),
    url(r'^servico/categoria$', views.servico_categoria, name='servico_categoria'),

    url(r'^servico/delete/(?P<servico_id>\d+)$', views.servico_delete, name='servico_delete'),
    url(r'^servico/edit/(?P<servico_id>\d+)$', views.servico_edit, name='servico_edit'),
    url(r'^servico/new$', views.servico_new, name='servico_new'),
    url(r'^servico$', views.servico, name='servico'),

]

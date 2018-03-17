from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('contato/', views.contato, name='contato'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('ocorrencia/relatorio/', views.ocorrencia_relatorio, name='ocorrencia_relatorio'),
    path('ocorrencia/register/', views.ocorrencia_register, name='ocorrencia_register'),
    path('ocorrencia/show/(?P<ocorrencia_id>\d+)/', views.ocorrencia_show, name='ocorrencia_show'),
    path('ocorrencia/new/', views.ocorrencia_new, name='ocorrencia_new'),
    path('ocorrencia/', views.ocorrencia, name='ocorrencia'),

    path('aluno/delete/(?P<aluno_id>\d+)', views.aluno_delete, name='aluno_delete'),
    path('aluno/edit/(?P<aluno_id>\d+)/', views.aluno_edit, name='aluno_edit'),
    path('aluno/new/', views.aluno_new, name='aluno_new'),
    path('aluno/', views.aluno, name='aluno'),

    path('curso/delete/(?P<curso_id>\d+)/', views.curso_delete, name='curso_delete'),
    path('curso/edit/(?P<curso_id>\d+)/', views.curso_edit, name='curso_edit'),
    path('curso/new/', views.curso_new, name='curso_new'),
    path('curso/', views.curso, name='curso'),

    path('turma/delete/(?P<turma_id>\d+)/', views.turma_delete, name='turma_delete'),
    path('turma/edit/(?P<turma_id>\d+)/', views.turma_edit, name='turma_edit'),
    path('turma/new/', views.turma_new, name='turma_new'),
    path('turma/', views.turma, name='turma'),

    path('matricula/delete/(?P<matricula_id>\d+)/', views.matricula_delete, name='matricula_delete'),
    path('matricula/edit/(?P<matricula_id>\d+)/', views.matricula_edit, name='matricula_edit'),
    path('matricula/new/', views.matricula_new, name='matricula_new'),
    path('matricula/', views.matricula, name='matricula'),

    path('import/matricula/', views.import_matricula, name='import_matricula'),
    path('import/aluno/', views.import_aluno, name='import_aluno'),
]

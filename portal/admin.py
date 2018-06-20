from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from portal.models import Empresa, Curso, Aluno, Ocorrencia, Turma, UserProfile, Matricula, Falta, CategoriaFalta, \
    Servico, ServicoCategoria, Encaminhamento
from import_export.admin import ImportExportModelAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = True


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


class AlunoAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nome', 'email', 'responsavel', 'email_responsavel', 'empresa')
    list_filter = ['empresa']
    search_fields = ['nome']


class MatriculaAdmin(ImportExportModelAdmin):
    list_display = ('id', 'aluno', 'turma', 'ano_letivo')
    list_filter = ['turma', 'ano_letivo', 'empresa']
    search_fields = ['aluno__nome']


class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'empresa')
    list_filter = ['empresa']
    search_fields = ['descricao']


class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'matricula', 'data', 'descricao', 'falta', 'user')
    list_filter = ['falta__categoria', 'matricula__ano_letivo', 'user', 'empresa']
    search_fields = ['matricula__aluno__nome', ]

class EncaminhamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'matricula', 'data', 'descricao',     'providencias', 'servico', 'user')
    list_filter = ['servico__categoria', 'matricula__ano_letivo', 'user', 'empresa']
    search_fields = ['matricula__aluno__nome', ]


class TurmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'curso', 'descricao', 'empresa')
    list_filter = ['curso', 'empresa']
    search_fields = ['descricao']


class FaltaAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria', 'descricao')
    list_filter = ['categoria']
    search_fields = ['descricao']


class EmpresaAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'nome_fantasia', 'responsavel_ocorrencia', 'email_responsavel_ocorrencia', 'responsavel_sistema',
    'email_responsavel_sistema')
    search_fields = ['nome_fantasia']

class ServicoCategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'empresa')
    list_filter = ['empresa']
    search_fields = ['descricao']

class ServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'categoria', 'empresa')
    list_filter = ['categoria', 'empresa']
    search_fields = ['descricao']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Ocorrencia, OcorrenciaAdmin)
admin.site.register(Encaminhamento, EncaminhamentoAdmin)
admin.site.register(Matricula, MatriculaAdmin)
admin.site.register(Falta, FaltaAdmin),
admin.site.register(CategoriaFalta),
admin.site.register(ServicoCategoria, ServicoCategoriaAdmin),
admin.site.register(Servico, ServicoAdmin),

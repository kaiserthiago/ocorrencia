from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from portal.models import Empresa, Curso, Aluno, Ocorrencia, Turma, UserProfile, Matricula, Falta, CategoriaFalta, \
    Servico, ServicoCategoria, Encaminhamento, Autorizacao, Configuracao, Banco
from import_export.admin import ImportExportModelAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = True


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'first_name', 'email')
    list_filter = ['userprofile__empresa', 'is_superuser', 'is_staff', 'is_active', 'groups']
    ordering = ['first_name', 'username']


class AlunoAdmin(ImportExportModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'rg', 'emissor', 'pai', 'mae', 'email_responsavel', 'empresa')
    list_filter = ['empresa']
    search_fields = ['nome']


class BancoAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nome', 'numero')
    list_filter = ['empresa']
    search_fields = ['nome', 'numero']


class MatriculaAdmin(ImportExportModelAdmin):
    list_display = ('id', 'aluno', 'turma', 'ano_letivo')
    list_filter = ['ano_letivo', 'empresa']
    search_fields = ['aluno__nome', 'turma']


class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'empresa')
    list_filter = ['empresa']
    search_fields = ['descricao']


class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'matricula', 'data', 'descricao', 'falta', 'user')
    list_filter = ['falta__categoria', 'matricula__ano_letivo', 'empresa']
    search_fields = ['matricula__aluno__nome', 'user']


class EncaminhamentoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created_at', 'update_at', 'matricula', 'data', 'descricao', 'providencias', 'servico', 'user')
    list_filter = ['status', 'servico__categoria', 'matricula__ano_letivo', 'empresa']
    search_fields = ['matricula__aluno__nome', 'user']


class AutorizacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'matricula', 'data', 'descricao', 'status', 'user')
    list_filter = ['matricula__ano_letivo', 'empresa']
    search_fields = ['matricula__aluno__nome', 'user']


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


class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'empresa')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Banco, BancoAdmin)
admin.site.register(Ocorrencia, OcorrenciaAdmin)
admin.site.register(Encaminhamento, EncaminhamentoAdmin)
admin.site.register(Matricula, MatriculaAdmin)
admin.site.register(Falta, FaltaAdmin),
admin.site.register(CategoriaFalta),
admin.site.register(ServicoCategoria, ServicoCategoriaAdmin),
admin.site.register(Servico, ServicoAdmin),
admin.site.register(Autorizacao, AutorizacaoAdmin),
admin.site.register(Configuracao, ConfiguracaoAdmin),

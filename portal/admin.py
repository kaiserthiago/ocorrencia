from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from portal.models import Empresa, Curso, Aluno, Ocorrencia, Turma, UserProfile, Matricula, Falta, CategoriaFalta, Teste
from import_export.admin import ImportExportModelAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = True


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


class AlunoAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nome', 'empresa')
    list_filter = ['empresa']
    search_fields = ['nome']


class MatriculaAdmin(ImportExportModelAdmin):
    list_display = ('id', 'aluno', 'turma', 'ano_letivo')
    list_filter = ['turma', 'ano_letivo', 'empresa']
    search_fields = ['aluno__nome']


class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao')


class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'matricula', 'data', 'descricao', 'falta', 'user')
    list_filter = ['falta__categoria', 'matricula__turma', 'user']
    search_fields = ['matricula__aluno__nome', ]


class TurmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'curso', 'descricao')


class FaltaAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria', 'descricao')
    list_filter = ['categoria']
    search_fields = ['descricao']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Empresa)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Ocorrencia, OcorrenciaAdmin)
admin.site.register(Matricula, MatriculaAdmin)
admin.site.register(Falta, FaltaAdmin),
admin.site.register(CategoriaFalta),
admin.site.register(Teste)

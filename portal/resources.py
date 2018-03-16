from import_export import resources
from .models import Aluno, Matricula, Teste


class AlunoResource(resources.ModelResource):
    class Meta:
        model = Aluno

class MatriculaResource(resources.ModelResource):
    class Meta:
        model = Matricula

class TesteResource(resources.ModelResource):
    class Meta:
        model = Teste
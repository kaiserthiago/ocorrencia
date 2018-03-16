from datetime import date

from django.db import models
from django.contrib.auth.models import User


def get_user_name(self):
    return self.first_name + ' ' + self.last_name


User.add_to_class("__str__", get_user_name)


class Empresa(models.Model):
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, null=True, blank=True)
    ie = models.CharField(max_length=45, null=True, blank=True)
    im = models.CharField(max_length=45, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    cep = models.CharField(max_length=10, null=True, blank=True)
    cidade = models.CharField(max_length=150, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    fone = models.CharField(max_length=13, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    site = models.CharField(max_length=50, null=True, blank=True)
    logo = models.ImageField(upload_to='img_empresa', null=True, blank=True)
    responsavel = models.CharField(max_length=150)
    email_responsavel = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = 'Empresa'
        ordering = ['nome_fantasia']

    def __str__(self):
        return self.nome_fantasia


class AuditoriaMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True


class Curso(AuditoriaMixin):
    descricao = models.CharField(max_length=255)
    email = models.EmailField()

    class Meta:
        ordering = ['descricao']

    def __str__(self):
        return self.descricao

    @property
    def retorna_turmas(self):
        return self.turma_set.all().order_by('descricao')


class Turma(AuditoriaMixin):
    descricao = models.CharField(max_length=150)
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.curso.descricao + ' - ' + self.descricao

    class Meta:
        ordering = ['descricao']


class Aluno(AuditoriaMixin):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']


class Matricula(AuditoriaMixin):
    aluno = models.ForeignKey(Aluno, on_delete=models.DO_NOTHING)
    turma = models.ForeignKey(Turma, on_delete=models.DO_NOTHING)
    ano_letivo = models.IntegerField(default=date.today().year)

    class Meta:
        verbose_name_plural = 'Matrículas'
        ordering = ['-ano_letivo', 'turma', 'aluno']

    def __str__(self):
        return self.aluno.nome + ' - ' + self.turma.descricao + ' - ' + self.turma.curso.descricao

    @property
    def ocorrencias(self):
        return self.ocorrencia_set.all().order_by('-data')


class CategoriaFalta(AuditoriaMixin):
    descricao = models.CharField(max_length=150)
    artigo = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Categoria das Faltas'

    def __str__(self):
        return self.descricao

    @property
    def retorna_faltas(self):
        return self.falta_set.all().order_by('inciso')


class Falta(AuditoriaMixin):
    categoria = models.ForeignKey(CategoriaFalta, on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    inciso = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = 'Faltas'
        ordering = ['categoria__artigo']

    def __str__(self):
        return self.categoria.descricao + ' - ' + self.inciso + ' - ' + self.descricao


class Ocorrencia(AuditoriaMixin):
    matricula = models.ForeignKey(Matricula, on_delete=models.DO_NOTHING)
    data = models.DateField()
    descricao = models.TextField(verbose_name='Descrição')
    falta = models.ForeignKey(Falta, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Ocorrências'
        ordering = ['-data', 'matricula__aluno']


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.DO_NOTHING)
    empresa = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING)
    siape = models.IntegerField()


class Teste(AuditoriaMixin):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']

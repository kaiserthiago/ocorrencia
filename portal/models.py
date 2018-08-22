from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


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
    responsavel_ocorrencia = models.CharField(max_length=150)
    email_responsavel_ocorrencia = models.EmailField()
    responsavel_sistema = models.CharField(max_length=150)
    email_responsavel_sistema = models.EmailField()
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

    @property
    def count_autorizacoes(self):
        return Autorizacao.objects.filter(data__year=date.today().year,
                                          matricula__turma__curso_id=self.id).order_by().values(
            'matricula__turma__descricao').annotate(qtde=Count('matricula__turma__descricao')).distinct()


class Turma(AuditoriaMixin):
    descricao = models.CharField(max_length=150)
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.curso.descricao + ' - ' + self.descricao

    class Meta:
        ordering = ['descricao']

    @property
    def count_cat_ocorrencia(self):
        return Ocorrencia.objects.filter(data__year=date.today().year, matricula__turma_id=self.id).order_by(
            'falta__categoria__artigo').values(
            'falta__categoria__descricao').annotate(qtde=Count('falta__categoria__descricao')).distinct()

    @property
    def count_ocorrencia(self):
        return Ocorrencia.objects.filter(data__year=date.today().year, matricula__turma_id=self.id).order_by().values(
            'matricula__turma__descricao').annotate(
            qtde=Count('matricula__turma__descricao')).distinct()

    @property
    def count_cat_encaminhamento(self):
        return Encaminhamento.objects.filter(data__year=date.today().year, matricula__turma_id=self.id).order_by(
            'servico__categoria__descricao').values(
            'servico__categoria__descricao').annotate(qtde=Count('servico__categoria__descricao')).distinct()

    @property
    def count_encaminhamento(self):
        return Encaminhamento.objects.filter(data__year=date.today().year,
                                             matricula__turma_id=self.id).order_by().values(
            'matricula__turma__descricao').annotate(
            qtde=Count('matricula__turma__descricao')).distinct()

    @property
    def count_autorizacoes(self):
        return Autorizacao.objects.filter(data__year=date.today().year, matricula__turma_id=self.id).order_by().values(
            'matricula__turma__descricao').annotate(
            qtde=Count('matricula__turma__descricao')).distinct()


class Aluno(AuditoriaMixin):
    nome = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    responsavel = models.CharField(max_length=255, blank=True, null=True)
    email_responsavel = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']

    @property
    def ocorrencia_aluno(self):
        return Ocorrencia.objects.filter(matricula__aluno_id=self.id, data__year=date.today().year)

    @property
    def count_cat_ocorrencia(self):
        return Ocorrencia.objects.filter(data__year=date.today().year, matricula__aluno_id=self.id).order_by(
            'falta__categoria__artigo').values(
            'falta__categoria__descricao').annotate(qtde=Count('falta__categoria__descricao')).distinct()

    @property
    def count_ocorrencia(self):
        return Ocorrencia.objects.filter(data__year=date.today().year, matricula__aluno_id=self.id).order_by().values(
            'matricula__aluno__nome', 'matricula__aluno_id').annotate(
            qtde=Count('matricula__aluno__nome')).distinct()

    @property
    def encaminhamento_aluno(self):
        return Encaminhamento.objects.filter(matricula__aluno_id=self.id, data__year=date.today().year)

    @property
    def count_cat_encaminhamento(self):
        return Encaminhamento.objects.filter(data__year=date.today().year, matricula__aluno_id=self.id).order_by(
            'servico__categoria__descricao').values(
            'servico__categoria__descricao').annotate(qtde=Count('servico__categoria__descricao')).distinct()

    @property
    def count_encaminhamento(self):
        return Encaminhamento.objects.filter(data__year=date.today().year,
                                             matricula__aluno_id=self.id).order_by().values(
            'matricula__aluno__nome', 'matricula__aluno_id').annotate(
            qtde=Count('matricula__aluno__nome')).distinct()

    @property
    def autorizacoes_aluno(self):
        return Autorizacao.objects.filter(matricula__aluno_id=self.id, data__year=date.today().year)

    @property
    def count_autorizacoes(self):
        return Autorizacao.objects.filter(data__year=date.today().year, matricula__aluno_id=self.id).order_by().values(
            'matricula__aluno__nome', 'matricula__aluno_id').annotate(qtde=Count('matricula__aluno__nome')).distinct()


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

    @property
    def autorizacoes_saidas(self):
        return self.autorizacao_set.all()


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
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING)
    siape = models.IntegerField()


class ServicoCategoria(AuditoriaMixin):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name_plural = 'Categorias de serviços'
        ordering = ['descricao']

    @property
    def retorna_servicos(self):
        return self.servico_set.all().order_by('descricao')


class Servico(AuditoriaMixin):
    categoria = models.ForeignKey(ServicoCategoria, on_delete=models.DO_NOTHING)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name_plural = 'Serviços'
        ordering = ['descricao']


class Encaminhamento(AuditoriaMixin):
    matricula = models.ForeignKey(Matricula, on_delete=models.DO_NOTHING)
    data = models.DateField()
    servico = models.ForeignKey(Servico, on_delete=models.DO_NOTHING)
    descricao = models.TextField(blank=True, null=True)
    providencias = models.TextField(blank=True, null=True)
    outras_informacoes = models.TextField(blank=True, null=True)
    responsavel_providencias = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='responsavel_providencias',
                                            blank=True, null=True)
    status_choiches = (
        ('Encaminhado', 'Encaminhado'),
        ('Atendido', 'Atendido'),
    )
    status = models.CharField(choices=status_choiches, max_length=30, default='Encaminhado')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Encaminhamentos'
        ordering = ['-data', 'matricula__aluno']


class Autorizacao(AuditoriaMixin):
    status_choiches = (
        ('Autorizado', 'Autorizado'),
        ('Efetuado', 'Efetuado'),
    )
    status = models.CharField(choices=status_choiches, max_length=30, default='Autorizado')
    matricula = models.ForeignKey(Matricula, on_delete=models.DO_NOTHING)
    data = models.DateField()
    descricao = models.TextField()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Autorizações de saída'
        ordering = ['-data', 'matricula__aluno']


class Configuracao(AuditoriaMixin):
    ocorrencia_email_aluno = models.BooleanField(default=True)
    ocorrencia_email_responsavel_aluno = models.BooleanField(default=True)
    ocorrencia_email_responsavel_user = models.BooleanField(default=True)
    ocorrencia_email_responsavel_setor = models.BooleanField(default=True)
    ocorrencia_email_coordenacao_curso = models.BooleanField(default=True)

    encaminhamento_email_aluno = models.BooleanField(default=True)
    encaminhamento_email_responsavel_aluno = models.BooleanField(default=True)
    encaminhamento_email_responsavel_user = models.BooleanField(default=True)
    encaminhamento_email_responsavel_setor = models.BooleanField(default=True)
    encaminhamento_email_coordenacao_curso = models.BooleanField(default=True)

    autorizacao_email_aluno = models.BooleanField(default=True)
    autorizacao_email_responsavel_aluno = models.BooleanField(default=True)
    autorizacao_email_responsavel_user = models.BooleanField(default=True)
    autorizacao_email_responsavel_setor = models.BooleanField(default=True)
    autorizacao_email_coordenacao_curso = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Configurações do sistema'

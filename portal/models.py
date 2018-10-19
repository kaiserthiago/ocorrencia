import json
import threading
from datetime import date
from django.db.models.functions import TruncMonth

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404

from portal.emails import RegistraOcorrenciaMail, RegistraEncaminhamentoMail, RegistraAutorizacaoSaidaMail


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
    turno = models.CharField(max_length=150)

    def __str__(self):
        return self.curso.descricao + ' - ' + self.descricao + ' - ' + self.turno

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


class Banco(AuditoriaMixin):
    nome = models.CharField(max_length=255)
    numero = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Aluno(AuditoriaMixin):
    nome = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    rg = models.CharField(max_length=255, blank=True, null=True)
    emissor = models.CharField(max_length=255, blank=True, null=True)
    cpf = models.CharField(max_length=255, blank=True, null=True)
    nascimento = models.DateField(blank=True, null=True)
    mae = models.CharField(max_length=255, blank=True, null=True)
    pai = models.CharField(max_length=255, blank=True, null=True)
    email_responsavel = models.EmailField(blank=True, null=True)
    foto = models.ImageField(null=True, blank=True, upload_to='img_alunos')

    banco = models.ForeignKey(Banco, blank=True, null=True, on_delete=models.DO_NOTHING)
    agencia = models.CharField(max_length=50, blank=True, null=True)
    conta = models.CharField(max_length=50, blank=True, null=True)

    numero_matricula = models.CharField(max_length=50, blank=True, null=True)
    contato = models.TextField(blank=True, null=True)

    pcd = models.BooleanField(default=False)
    cid = models.CharField(max_length=50, blank=True, null=True)
    pcd_descricao = models.CharField(max_length=255, blank=True, null=True)

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

    @property
    def perfil_ocorrencias_categoria(self):
        ocorrencias = list(
            Ocorrencia.objects.filter(data__year=date.today().year, matricula__aluno_id=self.id).order_by(
                'falta__categoria__artigo').values_list('falta__categoria__descricao').annotate(
                qtde=Count('id')).distinct())

        if ocorrencias:
            ocorrencias = json.dumps(ocorrencias)

        return ocorrencias

    @property
    def perfil_encaminhamentos_categoria(self):
        encaminhamentos = list(
            Encaminhamento.objects.filter(data__year=date.today().year, matricula__aluno_id=self.id).order_by(
                'servico__categoria__descricao').values_list(
                'servico__categoria__descricao').annotate(qtde=Count('id')).distinct())

        if encaminhamentos:
            encaminhamentos = json.dumps(encaminhamentos)

        return encaminhamentos

    @property
    def perfil_encaminhamentos_status(self):
        encaminhamentos = list(Encaminhamento.objects.filter(data__year=date.today().year,
                                                             matricula__aluno_id=self.id).order_by().values_list(
            'status').annotate(qtde=Count('id')).distinct())

        if encaminhamentos:
            encaminhamentos = json.dumps(encaminhamentos)

        return encaminhamentos

    @property
    def perfil_ocorrencias_mes(self):
        datas_ocorrencia = Ocorrencia.objects.filter(matricula__aluno_id=self.id,
                                                     data__year=date.today().year).annotate(
            month=TruncMonth('data')).values('month').annotate(c=Count('id')).values_list('month', 'c').order_by()

        mes_ocorrencia = [str(obj[0].strftime('%m/%Y')) for obj in datas_ocorrencia]
        qtde_ocorrencia = [int(obj[1]) for obj in datas_ocorrencia]

        dados_grafico_datas_ocorrencia = []

        for i in range(0, datas_ocorrencia.count()):
            dados_grafico_datas_ocorrencia.append([mes_ocorrencia[i], qtde_ocorrencia[i]])

        return dados_grafico_datas_ocorrencia

    @property
    def perfil_autorizacoes_mes(self):
        datas_saida = Autorizacao.objects.filter(matricula__aluno_id=self.id,
                                                 data__year=date.today().year).annotate(
            month=TruncMonth('data')).values('month').annotate(c=Count('id')).values_list('month', 'c').order_by()

        mes_saida = [str(obj[0].strftime('%m/%Y')) for obj in datas_saida]
        qtde_saida = [int(obj[1]) for obj in datas_saida]

        dados_grafico_datas_saidas = []

        for i in range(0, datas_saida.count()):
            dados_grafico_datas_saidas.append([mes_saida[i], qtde_saida[i]])

        return dados_grafico_datas_saidas


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
    aluno = models.OneToOneField(Aluno, blank=True, null=True, unique=True, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.DO_NOTHING)
    siape = models.IntegerField(blank=True, null=True, )

    def __str__(self):
        return str(self.empresa)


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
    responsavel_providencias = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                                 related_name='responsavel_providencias',
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

    providencia_encaminhamento_email_aluno = models.BooleanField(default=True)
    providencia_encaminhamento_email_responsavel_aluno = models.BooleanField(default=True)
    providencia_encaminhamento_email_responsavel_user = models.BooleanField(default=True)
    providencia_encaminhamento_email_responsavel_setor = models.BooleanField(default=True)
    providencia_encaminhamento_email_coordenacao_curso = models.BooleanField(default=True)

    autorizacao_email_aluno = models.BooleanField(default=True)
    autorizacao_email_responsavel_aluno = models.BooleanField(default=True)
    autorizacao_email_responsavel_user = models.BooleanField(default=True)
    autorizacao_email_responsavel_setor = models.BooleanField(default=True)
    autorizacao_email_coordenacao_curso = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Configurações do sistema'

# def post_email_autorizacao(**kwargs):
#     criado = kwargs['created']
#
#     if criado:
#         autorizacao = kwargs['instance']
#
#         email = []
#         configuracao = get_object_or_404(Configuracao, empresa=autorizacao.user.userprofile.empresa)
#
#         if configuracao.autorizacao_email_aluno:
#             # VERIFICA SE TEM EMAIL DO ALUNO
#             if autorizacao.matricula.aluno.email:
#                 email.append(autorizacao.matricula.aluno.email)
#
#         if configuracao.autorizacao_email_responsavel_aluno:
#             # VERIFICA SE TEM EMAIL DO RESPONSÁVEL
#             if autorizacao.matricula.aluno.email_responsavel:
#                 email.append(autorizacao.matricula.aluno.email_responsavel)
#
#         if configuracao.autorizacao_email_responsavel_user:
#             # EMAIL DO SERVIDOR QUE REGISTROU A OCORRÊNCIA
#             email.append(autorizacao.user.email)
#
#         if configuracao.autorizacao_email_coordenacao_curso:
#             # EMAIL DA COORDENAÇÃO DE CURSO
#             email.append(autorizacao.matricula.turma.curso.email)
#
#         if configuracao.autorizacao_email_responsavel_setor:
#             # EMAIL DO SETOR RESPONSÁVEL PELAS OCORRÊNCIAS
#             email.append(autorizacao.user.userprofile.empresa.email_responsavel_ocorrencia)
#
#         if email:
#             # ENVIA OS E-MAILS
#             def enviar():
#                 RegistraAutorizacaoSaidaMail(autorizacao).send(email)
#
#             threading.Thread(target=enviar).start()
#
# def post_email_encaminhamento(**kwargs):
#     criado = kwargs['created']
#
#     if criado:
#         encaminhamento = kwargs['instance']
#
#         email = []
#         configuracao = get_object_or_404(Configuracao, empresa=encaminhamento.user.userprofile.empresa)
#
#         if configuracao.encaminhamento_email_aluno:
#             # VERIFICA SE TEM EMAIL DO ALUNO
#             if encaminhamento.matricula.aluno.email:
#                 email.append(encaminhamento.matricula.aluno.email)
#
#         if configuracao.encaminhamento_email_responsavel_aluno:
#             # VERIFICA SE TEM EMAIL DO RESPONSÁVEL
#             if encaminhamento.matricula.aluno.email_responsavel:
#                 email.append(encaminhamento.matricula.aluno.email_responsavel)
#
#         if configuracao.encaminhamento_email_responsavel_user:
#             # EMAIL DO SERVIDOR QUE REGISTROU A OCORRÊNCIA
#             email.append(encaminhamento.user.email)
#
#         if configuracao.encaminhamento_email_coordenacao_curso:
#             # EMAIL DA COORDENAÇÃO DE CURSO
#             email.append(encaminhamento.matricula.turma.curso.email)
#
#         if configuracao.encaminhamento_email_responsavel_setor:
#             # EMAIL DO SETOR RESPONSÁVEL PELAS OCORRÊNCIAS
#             email.append(encaminhamento.userprofile.empresa.email_responsavel_ocorrencia)
#
#         if email:
#             # ENVIA OS E-MAILS
#             def enviar():
#                 RegistraEncaminhamentoMail(encaminhamento).send(email)
#
#             threading.Thread(target=enviar).start()
#
# def post_email_ocorrencia(**kwargs):
#     criado = kwargs['created']
#
#     if criado:
#         ocorrencia = kwargs['instance']
#
#         email = []
#         configuracao = get_object_or_404(Configuracao, empresa=ocorrencia.user.userprofile.empresa)
#
#         if configuracao.ocorrencia_email_aluno:
#             # VERIFICA SE TEM EMAIL DO ALUNO
#             if ocorrencia.matricula.aluno.email:
#                 email.append(ocorrencia.matricula.aluno.email)
#
#         if configuracao.ocorrencia_email_responsavel_aluno:
#             # VERIFICA SE TEM EMAIL DO RESPONSÁVEL
#             if ocorrencia.matricula.aluno.email_responsavel:
#                 email.append(ocorrencia.matricula.aluno.email_responsavel)
#
#         if configuracao.ocorrencia_email_responsavel_user:
#             # EMAIL DO SERVIDOR QUE REGISTROU A OCORRÊNCIA
#             email.append(ocorrencia.user.email)
#
#         if configuracao.ocorrencia_email_coordenacao_curso:
#             # EMAIL DA COORDENAÇÃO DE CURSO
#             email.append(ocorrencia.matricula.turma.curso.email)
#
#         if configuracao.ocorrencia_email_responsavel_setor:
#             # EMAIL DO SETOR RESPONSÁVEL PELAS OCORRÊNCIAS
#             email.append(ocorrencia.user.userprofile.empresa.email_responsavel_ocorrencia)
#
#         if email:
#             # ENVIA OS E-MAILS
#             def enviar():
#                 RegistraOcorrenciaMail(ocorrencia).send(email)
#
#             threading.Thread(target=enviar).start()
#
#
#
# models.signals.post_save.connect(post_email_autorizacao, sender=Autorizacao)
# models.signals.post_save.connect(post_email_encaminhamento, sender=Encaminhamento)
# models.signals.post_save.connect(post_email_ocorrencia, sender=Ocorrencia)

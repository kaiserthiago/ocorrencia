import json
import string
import types
from datetime import date

import easy_pdf
import numpy
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User, Permission
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Sum, Avg, Func, F, ExpressionWrapper, DurationField
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import lower
from django.template.loader import render_to_string
from easy_pdf.views import PDFTemplateView
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from tablib import Dataset

from ocorrencia import settings
from portal.emails import RegistraOcorrenciaMail, ConfirmaUsuarioMail, RegistraEncaminhamentoMail, \
    RegistraAutorizacaoSaidaMail, RegistraEncaminhamentoProvidenciasMail
from portal.forms import OcorrenciaForm, CursoForm, TurmaForm, AlunoForm, UserForm, UserProfileForm, \
    ServicoCategoriaForm, ServicoForm, EncaminhamentoForm, AutorizacaoForm, ConfiguracaoForm
from portal.models import Curso, Aluno, Turma, Ocorrencia, Matricula, CategoriaFalta, Falta, UserProfile, \
    ServicoCategoria, Servico, Encaminhamento, Autorizacao, Configuracao


def home(request):
    return render(request, 'portal/home.html', {})


def contato(request):
    # matricula = get_object_or_404(Matricula, pk=1009)
    # matricula.delete()
    return render(request, 'portal/contato.html', {})


@permission_required('is_superuser')
def configuracao(request):
    usuarios = User.objects.filter(userprofile__empresa=request.user.userprofile.empresa, is_active=False).order_by(
        'first_name')

    try:
        configuracao = get_object_or_404(Configuracao, empresa=request.user.userprofile.empresa)
    except:
        configuracao = Configuracao()
        configuracao.empresa = request.user.userprofile.empresa
        configuracao.save()

    if request.method == 'POST':
        form = ConfiguracaoForm(request.POST)

        if form.is_valid():
            configuracao.autorizacao_email_aluno = form.cleaned_data['autorizacao_email_aluno']
            configuracao.autorizacao_email_responsavel_aluno = form.cleaned_data['autorizacao_email_responsavel_aluno']
            configuracao.autorizacao_email_responsavel_user = form.cleaned_data['autorizacao_email_responsavel_user']
            configuracao.autorizacao_email_responsavel_setor = form.cleaned_data['autorizacao_email_responsavel_setor']
            configuracao.autorizacao_email_coordenacao_curso = form.cleaned_data['autorizacao_email_coordenacao_curso']

            configuracao.encaminhamento_email_aluno = form.cleaned_data['encaminhamento_email_aluno']
            configuracao.encaminhamento_email_responsavel_aluno = form.cleaned_data[
                'encaminhamento_email_responsavel_aluno']
            configuracao.encaminhamento_email_responsavel_user = form.cleaned_data[
                'encaminhamento_email_responsavel_user']
            configuracao.encaminhamento_email_responsavel_setor = form.cleaned_data[
                'encaminhamento_email_responsavel_setor']
            configuracao.encaminhamento_email_coordenacao_curso = form.cleaned_data[
                'encaminhamento_email_coordenacao_curso']

            configuracao.providencia_encaminhamento_email_aluno = form.cleaned_data[
                'providencia_encaminhamento_email_aluno']
            configuracao.providencia_encaminhamento_email_responsavel_aluno = form.cleaned_data[
                'providencia_encaminhamento_email_responsavel_aluno']
            configuracao.providencia_encaminhamento_email_responsavel_user = form.cleaned_data[
                'providencia_encaminhamento_email_responsavel_user']
            configuracao.providencia_encaminhamento_email_responsavel_setor = form.cleaned_data[
                'providencia_encaminhamento_email_responsavel_setor']
            configuracao.providencia_encaminhamento_email_coordenacao_curso = form.cleaned_data[
                'providencia_encaminhamento_email_coordenacao_curso']

            configuracao.ocorrencia_email_aluno = form.cleaned_data['ocorrencia_email_aluno']
            configuracao.ocorrencia_email_responsavel_aluno = form.cleaned_data['ocorrencia_email_responsavel_aluno']
            configuracao.ocorrencia_email_responsavel_user = form.cleaned_data['ocorrencia_email_responsavel_user']
            configuracao.ocorrencia_email_responsavel_setor = form.cleaned_data['ocorrencia_email_responsavel_setor']
            configuracao.ocorrencia_email_coordenacao_curso = form.cleaned_data['ocorrencia_email_coordenacao_curso']

            configuracao.save()

            messages.success(request, 'Configurações salvas.')

            return redirect('configuracao')

    form = ConfiguracaoForm(instance=configuracao)

    context = {
        'form': form,
        'configuracao': configuracao,
        'usuarios': usuarios
    }
    return render(request, 'portal/configuracao.html', context)


@permission_required('is_superuser')
def import_aluno_atualizar(request):
    try:
        lista_nome = []
        lista_nascimento = []
        lista_cpf = []
        lista_rg = []
        lista_emissor = []
        lista_pai = []
        lista_mae = []
        lista_email = []
        lista_contato = []
        lista_numero_matricula = []

        if request.method == 'POST':
            dataset = Dataset()
            new_persons = request.FILES['myfile']

            imported_data = dataset.load(new_persons.read())

            importado = 0
            nao_importado = 0

            # VERIFICA O ARQUIVO A PARTIR DA LINHA 2
            for n in imported_data[2:]:
                lista_nome.append(n[1])
                lista_nascimento.append(n[2])
                lista_rg.append(str(n[3]))
                lista_emissor.append(str(n[4] + '/' + n[5]))
                lista_cpf.append(str(n[6]).lstrip(" "))
                lista_pai.append(n[9])
                lista_mae.append(n[10])
                lista_email.append(lower(n[12]))
                lista_contato.append(n[13])
                lista_numero_matricula.append(n[14])

            contador = 0

            for teste in lista_nome:
                if teste != '':
                    aluno = get_object_or_404(Aluno, empresa=request.user.userprofile.empresa, nome=teste.rstrip(" "))

                    if lista_nascimento[contador]:
                        data = lista_nascimento[contador]
                        data = (data[6:10] + '-' + data[3:5] + '-' + data[0:2])

                        if aluno.nascimento != data:
                            aluno.nascimento = data

                    if aluno.rg != lista_rg[contador]:
                        aluno.rg = lista_rg[contador]

                    if aluno.emissor != lista_emissor[contador]:
                        aluno.emissor = lista_emissor[contador]

                    if aluno.cpf != lista_cpf[contador]:
                        aluno.cpf = lista_cpf[contador]

                    if aluno.pai != lista_pai[contador]:
                        aluno.pai = lista_pai[contador]

                    if aluno.mae != lista_mae[contador]:
                        aluno.mae = lista_mae[contador]

                    if aluno.email != lista_email[contador]:
                        aluno.email = lista_email[contador]

                    if aluno.contato != lista_contato[contador]:
                        aluno.contato = lista_contato[contador]

                    if aluno.numero_matricula != lista_numero_matricula[contador]:
                        aluno.numero_matricula = lista_numero_matricula[contador]

                    if aluno.empresa != request.user.userprofile.empresa:
                        aluno.empresa = request.user.userprofile.empresa

                    aluno.save()

                    if aluno.cpf:
                        try:
                            User.objects.create_user(
                                username=aluno.cpf,
                                password='ifro@cacoal',
                                email=aluno.email,
                                first_name=aluno.nome,
                                is_active=True,
                            )

                            usuario = get_object_or_404(User, username=aluno.cpf)
                            permission = Permission.objects.get(name='Can change aluno')
                            usuario.user_permissions.add(permission)
                            usuario.save()

                            profile = UserProfile()
                            profile.user = usuario
                            profile.empresa = request.user.userprofile.empresa
                            profile.aluno = aluno

                            profile.save()
                        except:
                            pass

                    contador += 1
                else:
                    contador += 1

            messages.success(request, 'Dados importados')
        context = {

        }

        return render(request, 'portal/import_aluno_atualizar.html', context)

    except:
        return HttpResponse('#' + str(contador) + ' - ' + teste)


@permission_required('is_superuser')
def import_matricula(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())

        id = request.POST['SelectTurma']
        turma = get_object_or_404(Turma, id=id)

        lista_aluno = []
        lista_situacao = []
        lista_nao_importado = []

        importado = 0
        nao_importado = 0
        contador = 0

        # VERIFICA O ARQUIVO A PARTIR DA LINHA 11
        for n in imported_data[11:]:
            if n[4]:
                lista_aluno.append(n[4])
            lista_situacao.append(n[14])

        for teste in lista_aluno:
            aluno = get_object_or_404(Aluno, empresa=request.user.userprofile.empresa, nome=teste.rstrip(" "))
            if lista_situacao[contador] == 'Matriculado':
                matricula = Matricula.objects.filter(aluno=aluno, ano_letivo=int(date.today().year), turma=turma)

                if (teste.rstrip(" ") == aluno.nome) and not matricula:
                    matricula = Matricula()
                    matricula.user = request.user
                    matricula.empresa = request.user.userprofile.empresa
                    matricula.aluno = aluno
                    matricula.turma = turma
                    matricula.ano_letivo = int(date.today().year)

                    matricula.save()
                    importado += 1
                else:
                    nao_importado += 1
                    lista_nao_importado.append(teste)
                contador += 1
            else:
                contador += 1

        context = {
            'importado': importado,
            'nao_importado': nao_importado,
            'lista_nao_importado': lista_nao_importado,
            'turma': turma
        }

        return render(request, 'portal/import_matricula_success.html', context)

    cursos = Curso.objects.filter(empresa=request.user.userprofile.empresa).order_by('descricao')

    context = {
        'cursos': cursos
    }

    return render(request, 'portal/import_matricula.html', context)


@permission_required('is_superuser')
def import_aluno(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())

        aluno = []
        email = []
        responsavel = []
        lista_nao_importado = []

        importado = 0
        nao_importado = 0

        for n in imported_data[2:]:
            aluno.append(n[1])

        for a in aluno:
            aluno = Aluno.objects.filter(empresa=request.user.userprofile.empresa, nome=a.rstrip(" "))

            if not aluno:
                aluno = Aluno()
                aluno.user = request.user
                aluno.empresa = request.user.userprofile.empresa
                aluno.nome = a.rstrip(" ")

                if email:
                    aluno.email = lower(email[importado])
                else:
                    aluno.email = ''

                # aluno.responsavel = responsavel[importado]

                aluno.save()

                importado += 1
            else:
                nao_importado += 1
                lista_nao_importado.append(a)

        context = {
            'importado': importado,
            'nao_importado': nao_importado,
            'lista_nao_importado': lista_nao_importado,

        }

        return render(request, 'portal/import_aluno_success.html', context)

    return render(request, 'portal/import_aluno.html', {})


@login_required
def aluno(request):
    qs = request.GET.get('qs', '')
    alunos = Aluno.objects.filter(empresa=request.user.userprofile.empresa, nome__istartswith=str(qs)).order_by('nome')
    lista = list(string.ascii_uppercase)

    context = {
        'alunos': alunos,
        'lista': lista,
        'qs': qs,
    }

    return render(request, 'portal/aluno.html', context)


@permission_required('is_superuser')
def aluno_new(request):
    qs = request.GET.get('qs', '')

    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)

        if form.is_valid():
            aluno = Aluno()

            if form.cleaned_data['nome']:
                aluno.nome = form.cleaned_data['nome'].upper()
            else:
                aluno.nome = ''

            if form.cleaned_data['pai']:
                aluno.pai = form.cleaned_data['pai'].upper()
            else:
                aluno.pai = ''

            if form.cleaned_data['mae']:
                aluno.mae = form.cleaned_data['mae']
            else:
                aluno.mae = ''

            if form.cleaned_data['emissor']:
                aluno.emissor = form.cleaned_data['emissor']
            else:
                aluno.emissor = ''

            aluno.cpf = form.cleaned_data['cpf']
            aluno.rg = form.cleaned_data['rg']
            aluno.email = form.cleaned_data['email']
            aluno.email_responsavel = form.cleaned_data['email_responsavel']
            aluno.foto = form.cleaned_data['foto']

            aluno.banco = form.cleaned_data['banco']
            aluno.agencia = form.cleaned_data['agencia']
            aluno.conta = form.cleaned_data['conta']

            aluno.empresa = request.user.userprofile.empresa

            aluno.save()

            messages.success(request, 'Aluno registrado.')

            return redirect('/aluno?qs=' + qs)

    form = AlunoForm()

    context = {
        'form': form,
        'qs': qs
    }

    return render(request, 'portal/aluno_new.html', context)


@login_required
def aluno_edit(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    qs = request.GET.get('qs', '')

    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['nome']:
                aluno.nome = form.cleaned_data['nome'].upper()
            else:
                aluno.nome = ''

            if form.cleaned_data['pai']:
                aluno.pai = form.cleaned_data['pai'].upper()
            else:
                aluno.pai = ''

            if form.cleaned_data['mae']:
                aluno.mae = form.cleaned_data['mae']
            else:
                aluno.mae = ''

            if form.cleaned_data['emissor']:
                aluno.emissor = form.cleaned_data['emissor']
            else:
                aluno.emissor = ''

            aluno.cpf = form.cleaned_data['cpf']
            aluno.rg = form.cleaned_data['rg']
            aluno.email = form.cleaned_data['email']
            aluno.email_responsavel = form.cleaned_data['email_responsavel']
            aluno.foto = form.cleaned_data['foto']

            aluno.banco = form.cleaned_data['banco']
            aluno.agencia = form.cleaned_data['agencia']
            aluno.conta = form.cleaned_data['conta']

            aluno.save()

            if request.user.has_perm(
                    'portal.change_aluno') and not request.user.is_staff and not request.user.is_superuser:
                usuario = get_object_or_404(User, pk=request.user.id)
                usuario.first_name = aluno.nome
                usuario.save()

                messages.success(request, 'Dados atualizados.')
                return redirect('perfil_individual', aluno.id)

            else:
                messages.success(request, 'Aluno atualizado.')
                return redirect('/aluno?qs=' + qs)

    form = AlunoForm(instance=aluno)

    context = {
        'form': form,
        'aluno': aluno,
        'qs': qs
    }

    return render(request, 'portal/aluno_edit.html', context)


@permission_required('is_superuser')
def aluno_delete(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    qs = request.GET.get('qs', '')

    if request.method == 'POST':
        aluno.delete()
        messages.success(request, 'Aluno excluído.')

    return redirect('/aluno?qs=' + qs)


@permission_required('is_superuser')
def curso(request):
    cursos = Curso.objects.filter(empresa=request.user.userprofile.empresa).order_by('descricao')

    context = {
        'cursos': cursos
    }

    return render(request, 'portal/curso.html', context)


@permission_required('is_superuser')
def curso_new(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)

        if form.is_valid():
            curso = Curso()

            curso.descricao = form.cleaned_data['descricao']
            curso.email = form.cleaned_data['email']
            curso.user = request.user
            curso.empresa = request.user.userprofile.empresa

            curso.save()
            messages.success(request, 'Curso registrado.')

            return redirect('curso')

    form = CursoForm()

    context = {
        'form': form
    }

    return render(request, 'portal/curso_new.html', context)


@permission_required('is_superuser')
def curso_edit(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)

    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso.descricao = form.cleaned_data['descricao']
            curso.email = form.cleaned_data['email']

            curso.save()

            messages.success(request, 'Curso atualizado.')

            return redirect('curso')

    form = CursoForm(instance=curso)

    context = {
        'form': form,
        'curso': curso,
    }

    return render(request, 'portal/curso_edit.html', context)


@permission_required('is_superuser')
def curso_delete(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)

    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso excluído.')

    return redirect('curso')


@staff_member_required
def perfil(request):
    cursos = Curso.objects.filter(empresa=request.user.userprofile.empresa)

    context = {
        'cursos': cursos
    }

    return render(request, 'portal/perfil.html', context)


@login_required
def perfil_individual(request, aluno_id):
    if request.user.has_perm('portal.change_aluno') and not request.user.is_staff and not request.user.is_superuser:
        if int(aluno_id) == request.user.userprofile.aluno.id:
            aluno = get_object_or_404(Aluno, pk=aluno_id)
            qs = request.GET.get('qs', '')

            context = {
                'aluno': aluno,
                'qs': qs
            }

            return render(request, 'portal/perfil_individual.html', context)
        else:
            erro = 'Você não tem permissão para acessar esses dados.'
            return render(request, 'portal/erro.html', {'erro': erro})
    else:
        aluno = get_object_or_404(Aluno, pk=aluno_id)
        qs = request.GET.get('qs', '')

        context = {
            'aluno': aluno,
            'qs': qs
        }

        return render(request, 'portal/perfil_individual.html', context)


@staff_member_required
def aluno_perfil_edit(request, aluno_id, page, turma):
    aluno = get_object_or_404(Aluno, pk=aluno_id)

    if request.method == 'POST':
        page = '/perfil/turma/' + str(turma) + '?page=' + str(page)
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['nome']:
                aluno.nome = form.cleaned_data['nome'].upper()
            else:
                aluno.nome = ''

            if form.cleaned_data['pai']:
                aluno.pai = form.cleaned_data['pai'].upper()
            else:
                aluno.pai = ''

            if form.cleaned_data['mae']:
                aluno.mae = form.cleaned_data['mae']
            else:
                aluno.mae = ''

            if form.cleaned_data['emissor']:
                aluno.emissor = form.cleaned_data['emissor']
            else:
                aluno.emissor = ''

            aluno.cpf = form.cleaned_data['cpf']
            aluno.rg = form.cleaned_data['rg']
            aluno.email = form.cleaned_data['email']
            aluno.email_responsavel = form.cleaned_data['email_responsavel']
            aluno.foto = form.cleaned_data['foto']

            aluno.banco = form.cleaned_data['banco']
            aluno.agencia = form.cleaned_data['agencia']
            aluno.conta = form.cleaned_data['conta']

            aluno.save()

            messages.success(request, 'Aluno atualizado.')

            return redirect(page)

    form = AlunoForm(instance=aluno)

    context = {
        'form': form,
        'aluno': aluno,
        'turma': turma,
        'page': page
    }

    return render(request, 'portal/aluno_edit_perfil.html', context)


@staff_member_required
def perfil_turma(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)
    alunos = Matricula.objects.filter(turma=turma, ano_letivo=date.today().year)

    page = request.GET.get('page', 1)
    paginator = Paginator(alunos, 1)

    try:
        alunos = paginator.page(page)
    except PageNotAnInteger:
        alunos = paginator.page(1)
    except EmptyPage:
        alunos = paginator.page(paginator.num_pages)

    context = {
        'turma': turma,
        'alunos': alunos
    }
    return render(request, 'portal/perfil_turma.html', context)


@login_required
def dashboard(request):
    # DADOS OCORRÊNCIA POR MÊS
    datas_ocorrencia = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                                 data__year=date.today().year).annotate(
        month=TruncMonth('data')).values('month').annotate(c=Count('id')).values_list('month', 'c').order_by()

    mes_ocorrencia = [str(obj[0].strftime('%m/%Y')) for obj in datas_ocorrencia]
    qtde_ocorrencia = [int(obj[1]) for obj in datas_ocorrencia]

    dados_grafico_datas_ocorrencia = []

    for i in range(0, datas_ocorrencia.count()):
        dados_grafico_datas_ocorrencia.append([mes_ocorrencia[i], qtde_ocorrencia[i]])

    # DADOS ENCAMINHAMENTO POR MÊS
    datas_encaminhamento = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa,
                                                         data__year=date.today().year).annotate(
        month=TruncMonth('data')).values('month').annotate(c=Count('id')).values_list('month', 'c').order_by()

    mes_encaminhamento = [str(obj[0].strftime('%m/%Y')) for obj in datas_encaminhamento]
    qtde_encaminhamento = [int(obj[1]) for obj in datas_encaminhamento]

    dados_grafico_datas_encaminhamento = []

    for i in range(0, datas_encaminhamento.count()):
        dados_grafico_datas_encaminhamento.append([mes_encaminhamento[i], qtde_encaminhamento[i]])

    # for i in datas_ocorrencia:
    #     dados_grafico_datas_ocorrencia.append([i[0], i[1]])

    # DADOS DOS INDICADORES
    indicador_autorizacao = Autorizacao.objects.filter(empresa=request.user.userprofile.empresa)
    indicador_encaminhamento = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa)
    indicador_ocorrencia = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa)

    dados_encaminhamentos = Encaminhamento.objects.filter(
        empresa=request.user.userprofile.empresa, status='Atendido').order_by().annotate(tempo=ExpressionWrapper(
        F('update_at') - F('created_at'), output_field=DurationField()))

    indicador_encaminhamento_tempo = []

    for i in dados_encaminhamentos:
        indicador_encaminhamento_tempo.append(i.tempo.days)

    indicador_encaminhamento_tempo = round(numpy.mean(indicador_encaminhamento_tempo))

    # DADOS GRÁFICO DE OCORRÊNCIAS POR CATEGORIA
    categorias = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa).order_by(
        'falta__categoria__artigo').values_list('falta__categoria__descricao').annotate(qtde=Count('id')).distinct()

    # categorias_faltas = [obj[0] for obj in categorias]
    # qtde_categorias_faltas = [int(obj[1]) for obj in categorias]

    dados_grafico_ocorrencia_categoria = json.dumps(list(categorias))

    # DADOS GRÁFICO DE OCORRÊNCIAS POR CURSO
    cursos = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa).order_by().values_list(
        'matricula__turma__curso__descricao').annotate(qtde=Count('id')).distinct()

    # cursos_ocorrencia = [obj[0] for obj in cursos]
    # qtde_cursos_ocorrencia = [int(obj[1]) for obj in cursos]

    dados_grafico_ocorrencia_curso = json.dumps(list(cursos))

    courses = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                        matricula__turma__curso__in=Curso.objects.all()).order_by(
        'matricula__turma__curso__descricao').values('matricula__turma__curso__id',
                                                     'matricula__turma__curso__descricao').distinct()

    if request.method == 'POST':
        # OCORRÊNCIAS
        if 'CourseOcorrencia' in request.POST:
            id = request.POST['CourseOcorrencia']
            c = get_object_or_404(Curso, id=id)

            detalhamento = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                                     matricula__turma__curso=c).order_by(
                'servico__categoria__descricao').values(
                'falta__categoria__descricao').annotate(qtde=Count('id')).distinct()

            total = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                              matricula__turma__curso=c).order_by(
                'falta__categoria__artigo').values().aggregate(qtde=Count('id'))

            # DADOS GRÁFICO CATEGORIA DE OCORRÊNCIAS POR CURSO
            distribuicao = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                                     matricula__turma__curso=c).order_by(
                'falta__categoria__artigo').values_list('falta__categoria__descricao').annotate(
                qtde=Count('id')).distinct()

            distribuicao_ocorrencia = [obj[0] for obj in distribuicao]
            distribuicao_qtde = [obj[1] for obj in distribuicao]

            # DADOS GRÁFICO DE OCORRÊNCIAS POR TURMA
            turmas = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                               matricula__turma__curso=c).order_by(
                'matricula__turma__descricao').values_list(
                'matricula__turma__descricao').annotate(qtde=Count('id')).distinct()

            dados_grafico_ocorrencia_turma = json.dumps(list(turmas))
            dados_grafico_ocorrencia_distribuicao = json.dumps(list(distribuicao))

            turmas_ocorrencia = [obj[0] for obj in turmas]
            qtde_turmas_ocorrencia = [int(obj[1]) for obj in turmas]
        else:
            c = ''
            distribuicao = ''
            distribuicao_ocorrencia = ''
            distribuicao_qtde = ''
            detalhamento = ''
            total = ''
            turmas = ''
            turmas_ocorrencia = ''
            qtde_turmas_ocorrencia = ''
            dados_grafico_ocorrencia_turma = ''
            dados_grafico_ocorrencia_distribuicao = ''

        # ENCACMINHAMENTOS
        if 'CourseEncaminhamento' in request.POST:
            id = request.POST['CourseEncaminhamento']
            c_encaminhamento = get_object_or_404(Curso, id=id)

            detalhamento_encaminhamento = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa,
                                                                        matricula__turma__curso=c_encaminhamento).order_by(
                'servico__categoria__descricao').values(
                'servico__categoria__descricao').annotate(qtde=Count('id')).distinct()

            total_encaminhamento = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa,
                                                                 matricula__turma__curso=c_encaminhamento).order_by(
                'servico__categoria__descricao').values().aggregate(qtde=Count('id'))

            # DADOS GRÁFICO CATEGORIA DE ENCAMINHAMENTOS POR CURSO
            distribuicao_encaminhamento = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa,
                                                                        matricula__turma__curso=c_encaminhamento).order_by(
                'servico__categoria__descricao').values_list('servico__categoria__descricao').annotate(
                qtde=Count('id')).distinct()

            # distribuicao_json_encaminhamento = [obj[0] for obj in distribuicao_encaminhamento]
            # distribuicao_qtde_encaminhamento = [obj[1] for obj in distribuicao_encaminhamento]

            dados_grafico_encaminhamento_distribuicao = json.dumps(list(distribuicao_encaminhamento))

            # DADOS GRÁFICO DE ENCAMINHAMENTOS POR TURMA
            turmas_encaminhamento = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa,
                                                                  matricula__turma__curso=c_encaminhamento).order_by(
                'matricula__turma__descricao').values_list(
                'matricula__turma__descricao').annotate(qtde=Count('id')).distinct()

            # turmas_ocorrencia_encaminhamento = [obj[0] for obj in turmas_encaminhamento]
            # qtde_turmas_encaminhamento = [int(obj[1]) for obj in turmas_encaminhamento]

            dados_grafico_encaminhamento_turma = json.dumps(list(turmas_encaminhamento))
        else:
            c_encaminhamento = ''
            distribuicao_encaminhamento = ''
            distribuicao_json_encaminhamento = ''
            distribuicao_qtde_encaminhamento = ''
            detalhamento_encaminhamento = ''
            total_encaminhamento = ''
            turmas_ocorrencia_encaminhamento = ''
            turmas_encaminhamento = ''
            qtde_turmas_encaminhamento = ''
            dados_grafico_encaminhamento_turma = ''
            dados_grafico_encaminhamento_distribuicao = ''


    else:
        # OCORRÊNCIAS
        c = ''
        distribuicao = ''
        distribuicao_ocorrencia = ''
        distribuicao_qtde = ''
        detalhamento = ''
        total = ''
        turmas = ''
        turmas_ocorrencia = ''
        qtde_turmas_ocorrencia = ''

        dados_grafico_ocorrencia_turma = ''
        dados_grafico_ocorrencia_distribuicao = ''

        # ENCAMINHAMENTOS
        c_encaminhamento = ''
        distribuicao_encaminhamento = ''
        distribuicao_json_encaminhamento = ''
        distribuicao_qtde_encaminhamento = ''
        detalhamento_encaminhamento = ''
        total_encaminhamento = ''
        turmas_ocorrencia_encaminhamento = ''
        turmas_encaminhamento = ''
        qtde_turmas_encaminhamento = ''

        dados_grafico_encaminhamento_turma = ''
        dados_grafico_encaminhamento_distribuicao = ''

    # DADOS GRÁFICO DE ENCAMINHAMENTOS POR CATEGORIA
    servico_categorias = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa).order_by(
        'servico__categoria__descricao').values_list('servico__categoria__descricao').annotate(
        qtde=Count('id')).distinct()

    # categorias_faltas_encaminhamento = [obj[0] for obj in servico_categorias]
    # qtde_categorias_faltas_encaminhamento = [int(obj[1]) for obj in servico_categorias]

    dados_grafico_encaminhamento_categoria = json.dumps(list(servico_categorias))

    # DADOS GRÁFICO DE ENCAMINHAMENTOS POR CURSO
    cursos_encaminhamento = Encaminhamento.objects.filter(
        empresa=request.user.userprofile.empresa).order_by().values_list(
        'matricula__turma__curso__descricao').annotate(qtde=Count('id')).distinct()

    # cursos_ocorrencia_encaminhamento = [obj[0] for obj in cursos_encaminhamento]
    # qtde_cursos_ocorrencia_encaminhamento = [int(obj[1]) for obj in cursos_encaminhamento]

    # dados_grafico_encaminhamento_curso = json.dumps(list(cursos_encaminhamento))

    courses_encaminhamento = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa,
                                                           matricula__turma__curso__in=Curso.objects.all()).order_by(
        'matricula__turma__curso__descricao').values('matricula__turma__curso__id',
                                                     'matricula__turma__curso__descricao').distinct()

    # DADOS GRÁFICO DE ENCAMINHAMENTOS POR STATUS
    status_encaminhamento = Encaminhamento.objects.filter(
        empresa=request.user.userprofile.empresa).order_by().values_list(
        'status').annotate(qtde=Count('id')).distinct()

    # status_ocorrencia_encaminhamento = [obj[0] for obj in status_encaminhamento]
    # qtde_status_ocorrencia_encaminhamento = [int(obj[1]) for obj in status_encaminhamento]

    dados_grafico_encaminhamento_status = json.dumps(list(status_encaminhamento))

    context = {
        # GRÁFICO DE DATAS
        'dados_grafico_datas_ocorrencia': dados_grafico_datas_ocorrencia,
        'dados_grafico_datas_encaminhamento': dados_grafico_datas_encaminhamento,

        # INDICADORES
        'indicador_autorizacao': indicador_autorizacao,
        'indicador_encaminhamento': indicador_encaminhamento,
        'indicador_ocorrencia': indicador_ocorrencia,
        'indicador_encaminhamento_tempo': indicador_encaminhamento_tempo,

        # OCORRÊNCIAS
        'c': c,
        'detalhamento': detalhamento,
        'total': total,

        'dados_grafico_ocorrencia_categoria': dados_grafico_ocorrencia_categoria,
        'dados_grafico_ocorrencia_curso': dados_grafico_ocorrencia_curso,
        'dados_grafico_ocorrencia_turma': dados_grafico_ocorrencia_turma,
        'dados_grafico_ocorrencia_distribuicao': dados_grafico_ocorrencia_distribuicao,

        'dados_grafico_encaminhamento_categoria': dados_grafico_encaminhamento_categoria,
        'dados_grafico_encaminhamento_status': dados_grafico_encaminhamento_status,
        'dados_grafico_encaminhamento_distribuicao': dados_grafico_encaminhamento_distribuicao,
        'dados_grafico_encaminhamento_turma': dados_grafico_encaminhamento_turma,

        'courses': courses,
        'categorias': categorias,
        'cursos': cursos,
        'turmas': turmas,
        'distribuicao': distribuicao,

        # 'categorias_faltas': json.dumps(categorias_faltas),
        # 'qtde_categorias_faltas': json.dumps(qtde_categorias_faltas),

        # 'cursos_ocorrencia': json.dumps(cursos_ocorrencia),
        # 'qtde_cursos_ocorrencia': json.dumps(qtde_cursos_ocorrencia),

        'turmas_ocorrencia': json.dumps(turmas_ocorrencia),
        'qtde_turmas_ocorrencia': json.dumps(qtde_turmas_ocorrencia),

        'distribuicao_ocorrencia': json.dumps(distribuicao_ocorrencia),
        'distribuicao_qtde': json.dumps(distribuicao_qtde),

        # ENCAMINHAMENTOS
        'c_encaminhamento': c_encaminhamento,
        'detalhamento_encaminhamento': detalhamento_encaminhamento,
        'total_encaminhamento': total_encaminhamento,

        'courses_encaminhamento': courses_encaminhamento,
        'servico_categorias': servico_categorias,
        'cursos_encaminhamento': cursos_encaminhamento,
        'status_encaminhamento': status_encaminhamento,
        'turmas_encaminhamento': turmas_encaminhamento,
        'distribuicao_encaminhamento': distribuicao_encaminhamento,

        # 'categorias_faltas_encaminhamento': json.dumps(categorias_faltas_encaminhamento),
        # 'qtde_categorias_faltas_encaminhamento': json.dumps(qtde_categorias_faltas_encaminhamento),

        # 'cursos_ocorrencia_encaminhamento': json.dumps(cursos_ocorrencia_encaminhamento),
        # 'qtde_cursos_ocorrencia_encaminhamento': json.dumps(qtde_cursos_ocorrencia_encaminhamento),

        # 'status_ocorrencia_encaminhamento': json.dumps(status_ocorrencia_encaminhamento),
        # 'qtde_status_ocorrencia_encaminhamento': json.dumps(qtde_status_ocorrencia_encaminhamento),

        # 'turmas_ocorrencia_encaminhamento': json.dumps(turmas_ocorrencia_encaminhamento),
        # 'qtde_turmas_encaminhamento': json.dumps(qtde_turmas_encaminhamento),

        # 'distribuicao_json_encaminhamento': json.dumps(distribuicao_json_encaminhamento),
        # 'distribuicao_qtde_encaminhamento': json.dumps(distribuicao_qtde_encaminhamento),
    }

    return render(request, 'portal/dashboard.html', context)


@permission_required('is_superuser')
def turma(request):
    turmas = Turma.objects.filter(empresa=request.user.userprofile.empresa).order_by('curso', 'descricao')

    context = {
        'turmas': turmas
    }

    return render(request, 'portal/turma.html', context)


@permission_required('is_superuser')
def turma_new(request):
    cursos = Curso.objects.filter(empresa=request.user.userprofile.empresa)

    if request.method == 'POST':
        form = TurmaForm(request.POST)

        if form.is_valid():
            curso_id = request.POST['SelectCurso']
            curso = get_object_or_404(Curso, id=curso_id)

            turma = Turma()

            turma.descricao = form.cleaned_data['descricao']
            turma.curso = curso
            turma.user = request.user
            turma.empresa = request.user.userprofile.empresa

            turma.save()

            messages.success(request, 'Turma registrada.')

            return redirect('turma')

    form = TurmaForm()

    context = {
        'form': form,
        'cursos': cursos
    }

    return render(request, 'portal/turma_new.html', context)


@permission_required('is_superuser')
def turma_edit(request, turma_id):
    cursos = Curso.objects.filter(empresa=request.user.userprofile.empresa)
    turma = get_object_or_404(Turma, pk=turma_id)
    c = get_object_or_404(Curso, id=turma.curso.id)

    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma.descricao = form.cleaned_data['descricao']

            id = request.POST['SelectCurso']
            c = get_object_or_404(Curso, id=id)
            turma.curso = c

            turma.save()

            messages.success(request, 'Turma atualizada.')

            return redirect('turma')

    form = TurmaForm(instance=turma)

    context = {
        'form': form,
        'turma': turma,
        'cursos': cursos,
        'c': c
    }

    return render(request, 'portal/turma_edit.html', context)


@permission_required('is_superuser')
def turma_delete(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)

    if request.method == 'POST':
        turma.delete()
        messages.success(request, 'Turma excluída.')

    return redirect('turma')


@login_required
def ocorrencia(request):
    cursos = Curso.objects.filter(empresa=request.user.userprofile.empresa)
    ocorrencias = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa, user=request.user,
                                            data__year=date.today().year)

    context = {
        'cursos': cursos,
        'ocorrencias': ocorrencias
    }
    return render(request, 'portal/ocorrencia.html', context)


@login_required
def ocorrencia_show(request, ocorrencia_id):
    ocorrencia = get_object_or_404(Ocorrencia, id=ocorrencia_id)
    ano = date.today().year

    context = {
        'ocorrencia': ocorrencia,
        'ano': ano
    }

    return render(request, 'portal/ocorrencia_show.html', context)


@login_required
def ocorrencia_new(request):
    if request.method == 'POST':
        form = OcorrenciaForm(request.POST)

        if not form.is_valid():
            id = request.POST['SelectTurma']
            turma = get_object_or_404(Turma, id=id)
            matriculas = Matricula.objects.filter(turma=turma, ano_letivo=int(date.today().year))

            categorias = CategoriaFalta.objects.all().order_by('artigo')

            form = OcorrenciaForm()

            context = {
                'categorias': categorias,
                'matriculas': matriculas,
                'turma': turma,
                'ano': int(date.today().year),
                'form': form
            }

    return render(request, 'portal/ocorrencia_new.html', context)


@login_required
def ocorrencia_register(request):
    if request.method == 'POST':
        form = OcorrenciaForm(request.POST)

        if form.is_valid():
            mat = Matricula.objects.filter(turma=request.POST['turma'])

            for m in mat:
                if 'mat_' + str(m.aluno.id) in request.POST:
                    ocorrencia = Ocorrencia()

                    matricula = get_object_or_404(Matricula, id=m.id)

                    falta_id = request.POST['SelectFalta']
                    falta = get_object_or_404(Falta, id=falta_id)

                    ocorrencia.matricula = matricula
                    ocorrencia.falta = falta
                    ocorrencia.data = form.cleaned_data['data']
                    ocorrencia.descricao = form.cleaned_data['descricao']

                    ocorrencia.user = request.user
                    ocorrencia.empresa = request.user.userprofile.empresa

                    ocorrencia.save()

                    email = []
                    configuracao = get_object_or_404(Configuracao, empresa=request.user.userprofile.empresa)

                    if configuracao.ocorrencia_email_aluno:
                        # VERIFICA SE TEM EMAIL DO ALUNO
                        if ocorrencia.matricula.aluno.email:
                            email.append(ocorrencia.matricula.aluno.email)

                    if configuracao.ocorrencia_email_responsavel_aluno:
                        # VERIFICA SE TEM EMAIL DO RESPONSÁVEL
                        if ocorrencia.matricula.aluno.email_responsavel:
                            email.append(ocorrencia.matricula.aluno.email_responsavel)

                    if configuracao.ocorrencia_email_responsavel_user:
                        # EMAIL DO SERVIDOR QUE REGISTROU A OCORRÊNCIA
                        email.append(request.user.email)

                    if configuracao.ocorrencia_email_coordenacao_curso:
                        # EMAIL DA COORDENAÇÃO DE CURSO
                        email.append(ocorrencia.matricula.turma.curso.email)

                    if configuracao.ocorrencia_email_responsavel_setor:
                        # EMAIL DO SETOR RESPONSÁVEL PELAS OCORRÊNCIAS
                        email.append(request.user.userprofile.empresa.email_responsavel_ocorrencia)

                    if email:
                        # ENVIA OS E-MAILS
                        RegistraOcorrenciaMail(ocorrencia).send(email)

            messages.success(request, 'Ocorrência disciplinar registrada.')

            return redirect('ocorrencia')
        else:
            form = OcorrenciaForm()

            context = {
                # 'matriculas': matriculas,
                'turma': turma,
                'form': form
            }

            return render(request, 'portal/ocorrencia.html', context)


@login_required
def ocorrencia_relatorio(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    ocorrencias = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                            data__year=date.today().year, matricula__aluno=aluno_id)
    count_ocorrencias = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                                  data__year=date.today().year,
                                                  matricula__aluno=aluno_id).order_by().values(
        'falta__categoria__descricao').annotate(qtde=Count('falta__categoria__descricao')).distinct()

    context = {
        'ocorrencias': ocorrencias,
        'aluno': aluno,
        'count_ocorrencias': count_ocorrencias
    }

    return render(request, 'portal/ocorrencia_relatorio.html', context)


@login_required
def ocorrencia_delete(request, ocorrencia_id):
    ocorrencia = get_object_or_404(Ocorrencia, pk=ocorrencia_id)

    if request.method == 'POST':
        ocorrencia.delete()
        messages.success(request, 'Ocorrência excluída.')

    return redirect('ocorrencia')


@permission_required('is_superuser')
def matricula(request):
    matriculas = Matricula.objects.filter(empresa=request.user.userprofile.empresa).order_by('-ano_letivo', 'turma',
                                                                                             'aluno')

    paginator = Paginator(matriculas, 30)
    page = request.GET.get('page', 1)

    try:
        matriculas = paginator.page(page)
    except PageNotAnInteger:
        matriculas = paginator.page(1)
    except EmptyPage:
        matriculas = paginator.page(paginator.num_pages)

    context = {
        'matriculas': matriculas
    }
    return render(request, 'portal/matricula.html', context)


@permission_required('is_superuser')
def matricula_new(request):
    alunos = Aluno.objects.filter(empresa=request.user.userprofile.empresa).order_by('nome')
    turmas = Turma.objects.filter(empresa=request.user.userprofile.empresa).order_by('curso__descricao', 'descricao')

    context = {
        'alunos': alunos,
        'turmas': turmas
    }

    return render(request, 'portal/matricula_new.html', context)


@permission_required('is_superuser')
def matricula_edit(request):
    pass


@permission_required('is_superuser')
def matricula_delete(request, matricula_id):
    matricula = get_object_or_404(Matricula, pk=matricula_id)

    if request.method == 'POST':
        matricula.delete()
        messages.success(request, 'Matrícula excluída.')

    return redirect('matricula')


@login_required
def user_account(request):
    user = User.objects.get(pk=request.user.pk)
    user_form = UserForm(instance=user)

    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.save()

    profile_form = UserProfileForm(instance=user_profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() and profile_form.cleaned_data['empresa'] != None:
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.save()

            user_profile.empresa = profile_form.cleaned_data['empresa']
            user_profile.save()

            messages.success(request, 'Conta de usuário atualizada.')
        else:
            messages.error(request, 'Verifique as informações inseridas.')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user,
    }
    return render(request, 'portal/user_account.html', context)


@permission_required('is_superuser')
def usuario_ativar(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        usuario.is_active = True
        usuario.save()

        email = []
        email.append(usuario.email)

        ConfirmaUsuarioMail(usuario).send(email)

        messages.success(request, 'Usuário ativo.')

        return redirect('configuracao')


@permission_required('is_superuser')
def usuario_desativar(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        usuario.is_active = False
        usuario.save()

        messages.success(request, 'Usuário inativo.')

        return redirect('configuracao')


@login_required
def user_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Sua senha foi alterada!')

            if request.user.has_perm(
                    'portal.change_aluno') and not request.user.is_staff and not request.user.is_superuser:
                return redirect('perfil_individual', request.user.userprofile.aluno.id)
            else:
                return redirect('user_account')
        else:
            messages.error(request, 'Por favor, verifique as informações inseridas.')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form
    }
    return render(request, 'portal/user_change_password.html', context)


@login_required
def report_general(request):
    cursos = Curso.objects.filter(empresa=request.user.userprofile.empresa)
    alunos = Aluno.objects.filter(empresa=request.user.userprofile.empresa).order_by('nome')

    context = {
        'cursos': cursos,
        'alunos': alunos,
    }

    return render(request, 'portal/report_general.html', context)


@login_required
def report_autorizacao_saida_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    ano = date.today().year

    autorizacoes = Autorizacao.objects.filter(empresa=request.user.userprofile.empresa, matricula__aluno=aluno,
                                              data__year=ano).order_by('-update_at')

    total = Autorizacao.objects.filter(empresa=request.user.userprofile.empresa, matricula__aluno_id=aluno,
                                       data__year=ano)

    context = {
        'autorizacoes': autorizacoes,
        'aluno': aluno,
        'ano': ano,
        'total': total,
    }

    return render(request, 'portal/report_autorizacao_saida_aluno.html', context)


@login_required
def report_autorizacao_saida_curso(request):
    id = request.POST['SelectCursoAutorizacaoSaida']
    curso = get_object_or_404(Curso, id=id)
    ano = date.today().year

    autorizacoes = Autorizacao.objects.filter(empresa=request.user.userprofile.empresa,
                                              matricula__turma__curso=curso,
                                              data__year=ano).order_by().values(
        'matricula__turma__descricao', 'matricula__turma_id').annotate(
        qtde=Count('matricula__turma__descricao')).distinct()

    total = Autorizacao.objects.filter(empresa=request.user.userprofile.empresa, matricula__turma__curso=curso,
                                       data__year=ano)

    turmas = Turma.objects.filter(empresa=request.user.userprofile.empresa, curso=curso).order_by('descricao')

    context = {
        'autorizacoes': autorizacoes,
        'curso': curso,
        'ano': ano,
        'total': total,
        'turmas': turmas
    }

    return render(request, 'portal/report_autorizacao_saida_curso.html', context)


@login_required
def report_autorizacao_saida_turma(request):
    id = request.POST['SelectTurmaAutorizacaoSaida']
    turma = get_object_or_404(Turma, id=id)
    ano = date.today().year

    autorizacoes = Autorizacao.objects.filter(empresa=request.user.userprofile.empresa, matricula__turma=turma,
                                              data__year=ano).order_by().values(
        'matricula__aluno__nome').annotate(
        qtde=Count('matricula__aluno__nome')).distinct()

    total = Autorizacao.objects.filter(empresa=request.user.userprofile.empresa, matricula__turma=turma,
                                       data__year=ano)

    alunos = Matricula.objects.filter(turma=turma, ano_letivo=date.today().year).order_by('aluno')

    context = {
        'autorizacoes': autorizacoes,
        'turma': turma,
        'ano': ano,
        'total': total,
        'alunos': alunos
    }

    return render(request, 'portal/report_autorizacao_saida_turma.html', context)


@login_required
def report_encaminhamento_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    ano = date.today().year

    encaminhamentos = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa, matricula__aluno=aluno,
                                                    data__year=ano).order_by('-data')

    total = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa, matricula__aluno_id=aluno,
                                          data__year=ano)

    context = {
        'encaminhamentos': encaminhamentos,
        'aluno': aluno,
        'ano': ano,
        'total': total,
    }

    return render(request, 'portal/report_encaminhamento_aluno.html', context)


@login_required
def report_encaminhamento_curso(request):
    id = request.POST['SelectCursoEncaminhamento']
    curso = get_object_or_404(Curso, id=id)
    ano = date.today().year

    encaminhamentos = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa,
                                                    matricula__turma__curso=curso,
                                                    data__year=ano).order_by().values(
        'matricula__turma__descricao', 'matricula__turma_id').annotate(
        qtde=Count('matricula__turma__descricao')).distinct()

    total = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa, matricula__turma__curso=curso,
                                          data__year=ano)

    cat = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa,
                                        data__year=date.today().year,
                                        matricula__turma__curso=curso).order_by('servico__categoria__descricao').values(
        'servico__categoria__descricao').annotate(qtde=Count('servico__categoria__descricao')).distinct()

    turmas = Turma.objects.filter(empresa=request.user.userprofile.empresa, curso=curso).order_by('descricao')

    context = {
        'encaminhamentos': encaminhamentos,
        'curso': curso,
        'ano': ano,
        'total': total,
        'cat': cat,
        'turmas': turmas
    }

    return render(request, 'portal/report_encaminhamento_curso.html', context)


@login_required
def report_encaminhamento_turma(request):
    id = request.POST['SelectTurmaEncaminhamento']
    turma = get_object_or_404(Turma, id=id)
    ano = date.today().year

    encaminhamentos = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa, matricula__turma=turma,
                                                    data__year=ano).order_by().values(
        'matricula__aluno__nome').annotate(
        qtde=Count('matricula__aluno__nome')).distinct()

    total = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa, matricula__turma=turma,
                                          data__year=ano)

    cat = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa,
                                        data__year=date.today().year,
                                        matricula__turma=turma).order_by('servico__categoria__descricao').values(
        'servico__categoria__descricao').annotate(qtde=Count('servico__categoria__descricao')).distinct()

    alunos = Matricula.objects.filter(turma=turma, ano_letivo=date.today().year)

    context = {
        'encaminhamentos': encaminhamentos,
        'turma': turma,
        'ano': ano,
        'total': total,
        'cat': cat,
        'alunos': alunos
    }

    return render(request, 'portal/report_encaminhamento_turma.html', context)


@login_required
def report_ocorrencia_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    ano = date.today().year

    ocorrencias = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa, matricula__aluno=aluno,
                                            data__year=ano).order_by('-data')

    total = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa, matricula__aluno_id=aluno,
                                      data__year=ano)

    context = {
        'ocorrencias': ocorrencias,
        'aluno': aluno,
        'ano': ano,
        'total': total,
    }

    return render(request, 'portal/report_ocorrencia_aluno.html', context)


@login_required
def report_ocorrencia_curso(request):
    id = request.POST['SelectCursoOcorrencia']
    curso = get_object_or_404(Curso, id=id)
    ano = date.today().year

    ocorrencias = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa, matricula__turma__curso=curso,
                                            data__year=ano).order_by().values('matricula__turma__descricao').annotate(
        qtde=Count('matricula__turma__descricao')).distinct()

    total = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa, matricula__turma__curso=curso,
                                      data__year=ano)

    cat = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                    data__year=date.today().year,
                                    matricula__turma__curso=curso).order_by('falta__categoria__artigo').values(
        'falta__categoria__descricao').annotate(qtde=Count('falta__categoria__descricao')).distinct()

    turmas = Turma.objects.filter(empresa=request.user.userprofile.empresa, curso=curso).order_by('descricao')

    context = {
        'ocorrencias': ocorrencias,
        'curso': curso,
        'ano': ano,
        'total': total,
        'cat': cat,
        'turmas': turmas

    }

    return render(request, 'portal/report_ocorrencia_curso.html', context)


@login_required
def report_ocorrencia_turma(request):
    id = request.POST['SelectTurmaOcorrencia']
    turma = get_object_or_404(Turma, id=id)
    ano = date.today().year

    ocorrencias = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa, matricula__turma=turma,
                                            data__year=ano).order_by().values('matricula__aluno__nome',
                                                                              'matricula__aluno_id').annotate(
        qtde=Count('matricula__aluno__nome')).distinct()

    total = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa, matricula__turma=turma,
                                      data__year=ano)

    cat = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                    data__year=date.today().year,
                                    matricula__turma=turma).order_by('falta__categoria__artigo').values(
        'falta__categoria__descricao').annotate(qtde=Count('falta__categoria__descricao')).distinct()

    alunos = Matricula.objects.filter(turma=turma, ano_letivo=date.today().year)

    context = {
        'ocorrencias': ocorrencias,
        'turma': turma,
        'ano': ano,
        'total': total,
        'cat': cat,
        'alunos': alunos
    }

    return render(request, 'portal/report_ocorrencia_turma.html', context)


@login_required
def report_pdf_dados_bancarios(request):
    try:
        id = request.POST['SelectTurmaDadosBancarios']
        turma = get_object_or_404(Turma, id=id)
        ano = date.today().year

        alunos = Matricula.objects.filter(turma=turma, ano_letivo=date.today().year).order_by('aluno')

        context = {
            'turma': turma,
            'ano': ano,
            'alunos': alunos
        }

        return easy_pdf.rendering.render_to_pdf_response(request, 'pdf/report_dados_bancarios.html',
                                                         context,
                                                         using=None, download_filename=None,
                                                         content_type='application/pdf', response_class=HttpResponse)
    except:
        erro = 'Não existem dados para gerar o relatório solicitado.'
        return render(request, 'portal/erro.html', {'erro': erro})


@login_required
def report_pdf_declaracao_matricula(request):
    try:
        id = request.POST['SelectDeclaraoMatriculaAluno']
        aluno = get_object_or_404(Aluno, id=id)
        data = date.today()
        usuario = get_object_or_404(User, id=request.user.id)

        matricula = get_object_or_404(Matricula, aluno=aluno, ano_letivo=data.year)

        context = {
            'aluno': aluno,
            'matricula': matricula,
            'data': data,
            'usuario': usuario
        }

        return easy_pdf.rendering.render_to_pdf_response(request, 'pdf/report_declaracao_matricula.html',
                                                         context,
                                                         using=None, download_filename=None,
                                                         content_type='application/pdf', response_class=HttpResponse)
    except:
        erro = 'Não há matrícula vigente para o(a) aluno(a) selecionado.'
        return render(request, 'portal/erro.html', {'erro': erro})


@login_required
def report_pdf_ocorrencia(request, ocorrencia_id):
    try:
        ocorrencia = get_object_or_404(Ocorrencia, id=ocorrencia_id)

        context = {
            'ocorrencia': ocorrencia,
        }

        return easy_pdf.rendering.render_to_pdf_response(request, 'pdf/report_ocorrencia.html',
                                                         context,
                                                         using=None, download_filename=None,
                                                         content_type='application/pdf', response_class=HttpResponse)
    except:
        erro = 'Não foi possível imprimir a ocorrência. Por favor contate o suporte.'
        return render(request, 'portal/erro.html', {'erro': erro})

@login_required
def report_pdf_encaminhamento(request, encaminhamento_id):
    try:
        encaminhamento = get_object_or_404(Encaminhamento, id=encaminhamento_id)

        context = {
            'encaminhamento': encaminhamento,
        }

        return easy_pdf.rendering.render_to_pdf_response(request, 'pdf/report_encaminhamento.html',
                                                         context,
                                                         using=None, download_filename=None,
                                                         content_type='application/pdf', response_class=HttpResponse)
    except:
        erro = 'Não foi possível imprimir o encaminhamento. Por favor contate o suporte.'
        return render(request, 'portal/erro.html', {'erro': erro})

@login_required
def report_pdf_lista_aluno_turma(request):
    try:
        id = request.POST['SelectListaAlunosTurma']
        turma = get_object_or_404(Turma, id=id)
        ano = date.today().year

        alunos = Matricula.objects.filter(turma=turma, ano_letivo=date.today().year).order_by('aluno')

        context = {
            'turma': turma,
            'ano': ano,
            'alunos': alunos
        }

        return easy_pdf.rendering.render_to_pdf_response(request, 'pdf/report_lista_aluno_turma.html',
                                                         context,
                                                         using=None, download_filename=None,
                                                         content_type='application/pdf', response_class=HttpResponse)
    except:
        erro = 'Não existem dados para gerar o relatório solicitado.'
        return render(request, 'portal/erro.html', {'erro': erro})


@permission_required('is_superuser')
def servico_categoria(request):
    servico_categorias = ServicoCategoria.objects.filter(empresa=request.user.userprofile.empresa)

    context = {
        'servico_categorias': servico_categorias
    }

    return render(request, 'portal/categoria_servico.html', context)


@permission_required('is_superuser')
def servico_categoria_new(request):
    if request.method == 'POST':
        form = ServicoCategoriaForm(request.POST)

        if form.is_valid():
            servico_categoria = ServicoCategoria()

            servico_categoria.descricao = form.cleaned_data['descricao']
            servico_categoria.user = request.user
            servico_categoria.empresa = request.user.userprofile.empresa

            servico_categoria.save()

            messages.success(request, 'Categoria de serviço registrada.')

            return redirect('servico_categoria')

    form = ServicoCategoriaForm()

    context = {
        'form': form
    }

    return render(request, 'portal/categoria_servico_new.html', context)


@permission_required('is_superuser')
def servico_categoria_edit(request, servico_categoria_id):
    servico_categoria = get_object_or_404(ServicoCategoria, pk=servico_categoria_id)

    if request.method == 'POST':
        form = ServicoCategoriaForm(request.POST)

        if form.is_valid():
            servico_categoria.descricao = form.cleaned_data['descricao']

            servico_categoria.save()

            messages.success(request, 'Categoria de serviço atualizada.')

            return redirect('servico_categoria')

    form = ServicoCategoriaForm(instance=servico_categoria)

    context = {
        'form': form,
        'servico_categoria': servico_categoria,
    }

    return render(request, 'portal/categoria_servico_edit.html', context)


@permission_required('is_superuser')
def servico_categoria_delete(request, servico_categoria_id):
    servico_categoria = get_object_or_404(ServicoCategoria, pk=servico_categoria_id)

    if request.method == 'POST':
        servico_categoria.delete()

        messages.success(request, 'Categoria de serviço excluída.')

    return redirect('servico_categoria')


@permission_required('is_superuser')
def servico(request):
    servicos = Servico.objects.filter(empresa=request.user.userprofile.empresa).order_by('categoria__descricao',
                                                                                         'descricao')

    context = {
        'servicos': servicos
    }

    return render(request, 'portal/servico.html', context)


@permission_required('is_superuser')
def servico_new(request):
    categorias = ServicoCategoria.objects.filter(empresa=request.user.userprofile.empresa)

    if request.method == 'POST':
        form = ServicoForm(request.POST)

        if form.is_valid():
            categoria_id = request.POST['SelectCategoria']
            categoria = get_object_or_404(ServicoCategoria, id=categoria_id)

            servico = Servico()

            servico.descricao = form.cleaned_data['descricao']
            servico.categoria = categoria
            servico.user = request.user
            servico.empresa = request.user.userprofile.empresa

            servico.save()

            messages.success(request, 'Serviço registrado.')

            return redirect('servico')

    form = ServicoForm()

    context = {
        'form': form,
        'categorias': categorias
    }

    return render(request, 'portal/servico_new.html', context)


@permission_required('is_superuser')
def servico_edit(request, servico_id):
    categorias = ServicoCategoria.objects.filter(empresa=request.user.userprofile.empresa)
    servico = get_object_or_404(Servico, pk=servico_id)

    if request.method == 'POST':
        form = ServicoForm(request.POST)

        if form.is_valid():
            categoria_id = request.POST['SelectCategoria']
            categoria = get_object_or_404(ServicoCategoria, id=categoria_id)

            servico.descricao = form.cleaned_data['descricao']
            servico.categoria = categoria
            servico.user = request.user
            servico.empresa = request.user.userprofile.empresa

            servico.save()

            messages.success(request, 'Serviço atualizado.')

            return redirect('servico')

    form = ServicoForm(instance=servico)

    context = {
        'form': form,
        'servico': servico,
        'categorias': categorias,
    }

    return render(request, 'portal/servico_edit.html', context)


@permission_required('is_superuser')
def servico_delete(request, servico_id):
    servico = get_object_or_404(Servico, pk=servico_id)

    if request.method == 'POST':
        servico.delete()

        messages.success(request, 'Serviço excluído.')

    return redirect('servico')


@login_required
def encaminhamento(request):
    cursos = Curso.objects.filter(empresa=request.user.userprofile.empresa)
    encaminhamentos = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa, user=request.user,
                                                    data__year=date.today().year)

    context = {
        'cursos': cursos,
        'encaminhamentos': encaminhamentos
    }
    return render(request, 'portal/encaminhamento.html', context)


@login_required
def encaminhamento_pendente(request):
    cursos = Curso.objects.filter(empresa=request.user.userprofile.empresa)
    encaminhamentos = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa,
                                                    data__year=date.today().year, status='Encaminhado')

    context = {
        'cursos': cursos,
        'encaminhamentos': encaminhamentos
    }
    return render(request, 'portal/encaminhamento_pendente.html', context)


@login_required
def encaminhamento_providencia(request, encaminhamento_id):
    encaminhamento = get_object_or_404(Encaminhamento, id=encaminhamento_id)

    if request.method == 'POST':
        providencias = request.POST['providencias']

        encaminhamento.providencias = providencias
        encaminhamento.status = 'Atendido'
        encaminhamento.responsavel_providencias = request.user

        encaminhamento.save()

        email = []
        configuracao = get_object_or_404(Configuracao, empresa=request.user.userprofile.empresa)

        if configuracao.providencia_encaminhamento_email_aluno:
            # VERIFICA SE TEM EMAIL DO ALUNO
            if encaminhamento.matricula.aluno.email:
                email.append(encaminhamento.matricula.aluno.email)

        if configuracao.providencia_encaminhamento_email_responsavel_aluno:
            # VERIFICA SE TEM EMAIL DO RESPONSÁVEL
            if encaminhamento.matricula.aluno.email_responsavel:
                email.append(encaminhamento.matricula.aluno.email_responsavel)

        if configuracao.providencia_encaminhamento_email_responsavel_user:
            # EMAIL DO SERVIDOR QUE REGISTROU A OCORRÊNCIA
            email.append(request.user.email)

        if configuracao.providencia_encaminhamento_email_coordenacao_curso:
            # EMAIL DA COORDENAÇÃO DE CURSO
            email.append(encaminhamento.matricula.turma.curso.email)

        if configuracao.providencia_encaminhamento_email_responsavel_setor:
            # EMAIL DO SETOR RESPONSÁVEL PELAS OCORRÊNCIAS
            email.append(request.user.userprofile.empresa.email_responsavel_ocorrencia)

        if email:
            # ENVIA OS E-MAILS
            RegistraEncaminhamentoProvidenciasMail(encaminhamento).send(email)

        messages.success(request, 'Providências adotadas registradas.')

        return redirect('encaminhamento_pendente')


@login_required
def encaminhamento_show(request, encaminhamento_id):
    encaminhamento = get_object_or_404(Encaminhamento, id=encaminhamento_id)
    ano = date.today().year

    context = {
        'encaminhamento': encaminhamento,
        'ano': ano
    }

    return render(request, 'portal/encaminhamento_show.html', context)


@login_required
def encaminhamento_new(request):
    if request.method == 'POST':
        form = EncaminhamentoForm(request.POST)

        if not form.is_valid():
            id = request.POST['SelectTurma']
            turma = get_object_or_404(Turma, id=id)
            matriculas = Matricula.objects.filter(turma=turma, ano_letivo=int(date.today().year))

            servico_categorias = ServicoCategoria.objects.filter(empresa=request.user.userprofile.empresa).order_by(
                'descricao')

            form = EncaminhamentoForm()

            context = {
                'servico_categorias': servico_categorias,
                'matriculas': matriculas,
                'turma': turma,
                'ano': int(date.today().year),
                'form': form
            }

    return render(request, 'portal/encaminhamento_new.html', context)


@login_required
def encaminhamento_register(request):
    if request.method == 'POST':
        form = EncaminhamentoForm(request.POST)

        if form.is_valid():
            mat = Matricula.objects.filter(turma=request.POST['turma'])

            for m in mat:
                if 'mat_' + str(m.aluno.id) in request.POST:
                    encaminhamento = Encaminhamento()

                    matricula = get_object_or_404(Matricula, id=m.id)

                    servico_id = request.POST['SelectServico']
                    servico = get_object_or_404(Servico, id=servico_id)

                    encaminhamento.matricula = matricula
                    encaminhamento.servico = servico
                    encaminhamento.data = form.cleaned_data['data']
                    encaminhamento.descricao = form.cleaned_data['descricao']
                    encaminhamento.providencias = form.cleaned_data['providencias']
                    encaminhamento.outras_informacoes = form.cleaned_data['outras_informacoes']

                    encaminhamento.user = request.user
                    encaminhamento.empresa = request.user.userprofile.empresa

                    encaminhamento.save()

                    email = []
                    configuracao = get_object_or_404(Configuracao, empresa=request.user.userprofile.empresa)

                    if configuracao.encaminhamento_email_aluno:
                        # VERIFICA SE TEM EMAIL DO ALUNO
                        if encaminhamento.matricula.aluno.email:
                            email.append(encaminhamento.matricula.aluno.email)

                    if configuracao.encaminhamento_email_responsavel_aluno:
                        # VERIFICA SE TEM EMAIL DO RESPONSÁVEL
                        if encaminhamento.matricula.aluno.email_responsavel:
                            email.append(encaminhamento.matricula.aluno.email_responsavel)

                    if configuracao.encaminhamento_email_responsavel_user:
                        # EMAIL DO SERVIDOR QUE REGISTROU A OCORRÊNCIA
                        email.append(request.user.email)

                    if configuracao.encaminhamento_email_coordenacao_curso:
                        # EMAIL DA COORDENAÇÃO DE CURSO
                        email.append(encaminhamento.matricula.turma.curso.email)

                    if configuracao.encaminhamento_email_responsavel_setor:
                        # EMAIL DO SETOR RESPONSÁVEL PELAS OCORRÊNCIAS
                        email.append(request.user.userprofile.empresa.email_responsavel_ocorrencia)

                    if email:
                        # ENVIA OS E-MAILS
                        RegistraEncaminhamentoMail(encaminhamento).send(email)

            messages.success(request, 'Encaminhamento registrado.')

            return redirect('encaminhamento')
        else:
            form = EncaminhamentoForm()

            context = {
                # 'matriculas': matriculas,
                'turma': turma,
                'form': form
            }

            return render(request, 'portal/encaminhamento.html', context)


@login_required
def encaminhamento_delete(request, encaminhamento_id):
    encaminhamento = get_object_or_404(Encaminhamento, pk=encaminhamento_id)

    if request.method == 'POST':
        encaminhamento.delete()

        messages.success(request, 'Encaminhamento excluído.')

    return redirect('encaminhamento')


@login_required
def encaminhamento_relatorio(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    encaminhamentos = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa,
                                                    data__year=date.today().year, matricula__aluno=aluno_id)
    count_encaminhamentos = Encaminhamento.objects.filter(empresa=request.user.userprofile.empresa,
                                                          data__year=date.today().year,
                                                          matricula__aluno=aluno_id).order_by().values(
        'servico__categoria__descricao').annotate(qtde=Count('servico__categoria__descricao')).distinct()

    context = {
        'encaminhamentos': encaminhamentos,
        'aluno': aluno,
        'count_encaminhamentos': count_encaminhamentos
    }

    return render(request, 'portal/encaminhamento_relatorio.html', context)


@staff_member_required
def autorizacao(request):
    cursos = Curso.objects.filter(empresa=request.user.userprofile.empresa)
    autorizacoes = Autorizacao.objects.filter(empresa=request.user.userprofile.empresa, user=request.user,
                                              data__year=date.today().year)

    context = {
        'cursos': cursos,
        'autorizacoes': autorizacoes
    }
    return render(request, 'portal/autorizacao.html', context)


@staff_member_required
def autorizacao_show(request, autorizacao_id):
    autorizacao = get_object_or_404(Autorizacao, id=autorizacao_id)
    ano = date.today().year

    context = {
        'autorizacao': autorizacao,
        'ano': ano
    }

    return render(request, 'portal/autorizacao_show.html', context)


@staff_member_required
def autorizacao_new(request):
    if request.method == 'POST':
        form = AutorizacaoForm(request.POST)

        if not form.is_valid():
            id = request.POST['SelectTurma']
            turma = get_object_or_404(Turma, id=id)
            matriculas = Matricula.objects.filter(turma=turma, ano_letivo=int(date.today().year))

            # servico_categorias = ServicoCategoria.objects.all().order_by('id')

            form = AutorizacaoForm()

            context = {
                # 'servico_categorias': servico_categorias,
                'matriculas': matriculas,
                'turma': turma,
                'ano': int(date.today().year),
                'form': form
            }

    return render(request, 'portal/autorizacao_new.html', context)


@staff_member_required
def autorizacao_register(request):
    if request.method == 'POST':
        form = AutorizacaoForm(request.POST)

        if form.is_valid():
            mat = Matricula.objects.filter(turma=request.POST['turma'])

            for m in mat:
                if 'mat_' + str(m.aluno.id) in request.POST:
                    autorizacao = Autorizacao()

                    matricula = get_object_or_404(Matricula, id=m.id)

                    autorizacao.matricula = matricula
                    autorizacao.data = form.cleaned_data['data']
                    autorizacao.descricao = form.cleaned_data['descricao']

                    autorizacao.user = request.user
                    autorizacao.empresa = request.user.userprofile.empresa

                    autorizacao.save()

            messages.success(request, 'Autorização de saída registrada.')
            return redirect('autorizacao')
        else:
            form = AutorizacaoForm()

            context = {
                # 'matriculas': matriculas,
                'turma': turma,
                'form': form
            }

            return render(request, 'portal/autorizacao.html', context)


@staff_member_required
def autorizacao_delete(request, autorizacao_id):
    autorizacao = get_object_or_404(Autorizacao, pk=autorizacao_id)

    if request.method == 'POST':
        autorizacao.delete()

        messages.success(request, 'Autorização de saída excluída.')

    return redirect('autorizacao')


@staff_member_required
def autorizacao_relatorio_aluno(request):
    if request.method == 'POST':
        id = request.POST['SelectAlunoAutorizacao']

        return redirect('autorizacao_relatorio', id)


@login_required
def encaminhamento_relatorio_aluno(request):
    if request.method == 'POST':
        id = request.POST['SelectAlunoEncaminhamento']

        return redirect('encaminhamento_relatorio', id)


@login_required
def ocorrencia_relatorio_aluno(request):
    if request.method == 'POST':
        id = request.POST['SelectAlunoOcorrencia']

        return redirect('ocorrencia_relatorio', id)


@staff_member_required
def autorizacao_relatorio(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)

    autorizacoes = Autorizacao.objects.filter(empresa=request.user.userprofile.empresa,
                                              data__year=date.today().year, matricula__aluno=aluno_id)

    context = {
        'autorizacoes': autorizacoes,
        'aluno': aluno,
    }

    return render(request, 'portal/autorizacao_relatorio.html', context)


@login_required
def autorizacao_pendente(request):
    autorizacoes = Autorizacao.objects.filter(empresa=request.user.userprofile.empresa, data__year=date.today().year,
                                              status='Autorizado')
    context = {
        'autorizacoes': autorizacoes
    }
    return render(request, 'portal/autorizacao_pendente.html', context)


@login_required
def autorizacao_confirmar(request, autorizacao_id):
    autorizacao = get_object_or_404(Autorizacao, id=autorizacao_id)

    if request.method == 'POST':
        autorizacao.status = 'Efetuado'

        autorizacao.save()

        email = []
        configuracao = get_object_or_404(Configuracao, empresa=request.user.userprofile.empresa)

        if configuracao.autorizacao_email_aluno:
            # VERIFICA SE TEM EMAIL DO ALUNO
            if autorizacao.matricula.aluno.email:
                email.append(autorizacao.matricula.aluno.email)

        if configuracao.autorizacao_email_responsavel_aluno:
            # VERIFICA SE TEM EMAIL DO RESPONSÁVEL
            if autorizacao.matricula.aluno.email_responsavel:
                email.append(autorizacao.matricula.aluno.email_responsavel)

        if configuracao.autorizacao_email_responsavel_user:
            # EMAIL DO SERVIDOR QUE REGISTROU A OCORRÊNCIA
            email.append(request.user.email)

        if configuracao.autorizacao_email_coordenacao_curso:
            # EMAIL DA COORDENAÇÃO DE CURSO
            email.append(autorizacao.matricula.turma.curso.email)

        if configuracao.autorizacao_email_responsavel_setor:
            # EMAIL DO SETOR RESPONSÁVEL PELAS OCORRÊNCIAS
            email.append(request.user.userprofile.empresa.email_responsavel_ocorrencia)

        if email:
            # ENVIA OS E-MAILS
            RegistraAutorizacaoSaidaMail(autorizacao).send(email)

        messages.success(request, 'Saída confirmada.')

        return redirect('autorizacao_pendente')

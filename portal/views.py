import json
from datetime import date

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import upper
from tablib import Dataset

from portal.emails import RegistraOcorrenciaMail, ConfirmaUsuarioMail
from portal.forms import OcorrenciaForm, CursoForm, TurmaForm, AlunoForm
from portal.models import Curso, Aluno, Turma, Ocorrencia, Matricula, CategoriaFalta, Falta


def home(request):
    return render(request, 'portal/home.html', {})


def contato(request):
    return render(request, 'portal/contato.html', {})


@staff_member_required
def import_matricula(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())

        id = request.POST['SelectTurma']
        turma = get_object_or_404(Turma, id=id)

        lista = []

        importado = 0
        nao_importado = 0
        # i=1
        # for n in imported_data:
        #     aluno = Aluno.objects.filter(nome=upper(n[0]))
        #     if not aluno:
        #         lista.append(str(i)+' - '+upper(n[0])+'<br>')
        #     i+=1
        # return HttpResponse(lista)

        for n in imported_data:
            lista.append(upper(n[0]))

        for teste in lista:
            aluno = get_object_or_404(Aluno, empresa=request.user.userprofile.empresa, nome=teste)
            matricula = Matricula.objects.filter(aluno=aluno, ano_letivo=int(date.today().year))

            if (teste == aluno.nome) and not matricula:
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

        context = {
            'importado': importado,
            'nao_importado': nao_importado
        }

        return render(request, 'portal/import_matricula_success.html', context)

    cursos = Curso.objects.filter(empresa=request.user.userprofile.empresa).order_by('descricao')

    context = {
        'cursos': cursos
    }

    return render(request, 'portal/import_matricula.html', context)


@staff_member_required
def import_aluno(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())

        lista = []

        importado = 0
        nao_importado = 0

        for n in imported_data:
            lista.append(upper(n[0]))

        for teste in lista:
            aluno = Aluno.objects.filter(empresa=request.user.userprofile.empresa, nome=teste)

            if not aluno:
                aluno = Aluno()
                aluno.user = request.user
                aluno.empresa = request.user.userprofile.empresa
                aluno.nome = teste

                aluno.save()
                importado += 1
            else:
                nao_importado += 1

        context = {
            'importado': importado,
            'nao_importado': nao_importado
        }

        return render(request, 'portal/import_aluno_success.html', context)

    return render(request, 'portal/import_aluno.html', {})


@staff_member_required
def aluno(request):
    alunos = Aluno.objects.filter(empresa=request.user.userprofile.empresa).order_by('nome')

    context = {
        'alunos': alunos,
    }

    return render(request, 'portal/aluno.html', context)


@staff_member_required
def aluno_new(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)

        if form.is_valid():
            aluno = Aluno()

            aluno.nome = form.cleaned_data['nome'].upper()
            aluno.user = request.user
            aluno.empresa = request.user.userprofile.empresa

            aluno.save()

            return redirect('aluno')

    form = AlunoForm()

    context = {
        'form': form
    }

    return render(request, 'portal/aluno_new.html', context)


@staff_member_required
def aluno_edit(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)

    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno.nome = form.cleaned_data['nome'].upper()

            aluno.save()

            messages.success(request, 'Aluno atualizado.')

            return redirect('aluno')

    form = AlunoForm(instance=aluno)

    context = {
        'form': form,
        'aluno': aluno,
    }

    return render(request, 'portal/aluno_edit.html', context)


@staff_member_required
def aluno_delete(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)

    if request.method == 'POST':
        aluno.delete()
        messages.success(request, 'Aluno excluído.')

    return redirect('aluno')


@staff_member_required
def curso(request):
    cursos = Curso.objects.filter(empresa=request.user.userprofile.empresa).order_by('descricao')

    context = {
        'cursos': cursos
    }

    return render(request, 'portal/curso.html', context)


@staff_member_required
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

            return redirect('curso')

    form = CursoForm()

    context = {
        'form': form
    }

    return render(request, 'portal/curso_new.html', context)


@staff_member_required
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


@staff_member_required
def curso_delete(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)

    if request.method == 'POST':
        curso.delete()
    return redirect('curso')


@login_required
def dashboard(request):
    # DADOS GRÁFICO DE OCORRÊNCIAS POR CATEGORIA
    categorias = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa).order_by(
        'falta__categoria__artigo').values_list('falta__categoria__descricao').annotate(qtde=Count('id')).distinct()

    categorias_faltas = [obj[0] for obj in categorias]
    qtde_categorias_faltas = [int(obj[1]) for obj in categorias]

    # DADOS GRÁFICO DE OCORRÊNCIAS POR CURSO
    cursos = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa).order_by().values_list(
        'matricula__turma__curso__descricao').annotate(qtde=Count('id')).distinct()

    cursos_ocorrencia = [obj[0] for obj in cursos]
    qtde_cursos_ocorrencia = [int(obj[1]) for obj in cursos]

    courses = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa, matricula__turma__curso__in=Curso.objects.all()).order_by(
        'matricula__turma__curso__descricao').values('matricula__turma__curso__id',
                                                     'matricula__turma__curso__descricao').distinct()

    if request.method == 'POST':
        id = request.POST['Course']
        c = get_object_or_404(Curso, id=id)

        detalhamento = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                                 matricula__turma__curso=c).order_by('falta__categoria__artigo').values(
            'falta__categoria__descricao').annotate(qtde=Count('id')).distinct()

        total = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                          matricula__turma__curso=c).order_by(
            'falta__categoria__artigo').values().aggregate(qtde=Count('id'))

        # DADOS GRÁFICO CATEGORIA DE OCORRÊNCIAS POR CURSO
        distribuicao = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                                 matricula__turma__curso=c).order_by(
            'falta__categoria__artigo').values_list('falta__categoria__descricao').annotate(qtde=Count('id')).distinct()

        distribuicao_ocorrencia = [obj[0] for obj in distribuicao]
        distribuicao_qtde = [obj[1] for obj in distribuicao]

        # DADOS GRÁFICO DE OCORRÊNCIAS POR TURMA
        turmas = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa,
                                           matricula__turma__curso=c).order_by(
            'matricula__turma__descricao').values_list(
            'matricula__turma__descricao').annotate(qtde=Count('id')).distinct()

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

    context = {
        'c': c,
        'detalhamento': detalhamento,
        'total': total,

        'courses': courses,
        'categorias': categorias,
        'cursos': cursos,
        'turmas': turmas,
        'distribuicao': distribuicao,

        'categorias_faltas': json.dumps(categorias_faltas),
        'qtde_categorias_faltas': json.dumps(qtde_categorias_faltas),

        'cursos_ocorrencia': json.dumps(cursos_ocorrencia),
        'qtde_cursos_ocorrencia': json.dumps(qtde_cursos_ocorrencia),

        'turmas_ocorrencia': json.dumps(turmas_ocorrencia),
        'qtde_turmas_ocorrencia': json.dumps(qtde_turmas_ocorrencia),

        'distribuicao_ocorrencia': json.dumps(distribuicao_ocorrencia),
        'distribuicao_qtde': json.dumps(distribuicao_qtde),
    }

    return render(request, 'portal/dashboard.html', context)


@staff_member_required
def turma(request):
    turmas = Turma.objects.filter(empresa=request.user.userprofile.empresa).order_by('curso', 'descricao')

    context = {
        'turmas': turmas
    }

    return render(request, 'portal/turma.html', context)


@staff_member_required
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

            return redirect('turma')

    form = TurmaForm()

    context = {
        'form': form,
        'cursos': cursos
    }

    return render(request, 'portal/turma_new.html', context)


@staff_member_required
def turma_edit(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)

    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma.descricao = form.cleaned_data['descricao']
            turma.curso = form.cleaned_data['curso']

            turma.save()

            messages.success(request, 'Turma atualizada.')

            return redirect('turma')

    form = TurmaForm(instance=turma)

    context = {
        'form': form,
        'turma': turma,
    }

    return render(request, 'portal/turma_edit.html', context)


@login_required
def turma_delete(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id)

    if request.method == 'POST':
        turma.delete()
    return redirect('turma')


@login_required
def ocorrencia(request):
    cursos = Curso.objects.filter(empresa=request.user.userprofile.empresa)
    ocorrencias = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa, user=request.user, data__year=date.today().year)

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
                    # EMAIL DO RESPONSÁVEL PELAS OCORRÊNCIAS
                    email.append(request.user.userprofile.empresa.email_responsavel_ocorrencia)
                    # EMAIL DO PROFESSOR
                    email.append(request.user.email)
                    # EMAIL DO COORDENADOR
                    email.append(ocorrencia.matricula.turma.curso.email)

                    RegistraOcorrenciaMail(ocorrencia).send(email)

            return redirect('ocorrencia')
        else:
            form = OcorrenciaForm()

            context = {
                # 'matriculas': matriculas,
                'turma': turma,
                'form': form
            }

            return render(request, 'portal/ocorrencia.html', context)


@staff_member_required
def ocorrencia_delete(request, ocorrencia_id):
    ocorrencia = get_object_or_404(Ocorrencia, pk=ocorrencia_id)

    if request.method == 'POST':
        ocorrencia.delete()
        messages.success(request, 'Ocorrência excluída.')

    return redirect('ocorrencia')


@staff_member_required
def matricula(request):
    matriculas = Matricula.objects.filter(empresa=request.user.userprofile.empresa).order_by('-ano_letivo', 'turma', 'aluno')

    context = {
        'matriculas': matriculas
    }
    return render(request, 'portal/matricula.html', context)


@staff_member_required
def matricula_new(request):
    alunos = Aluno.objects.filter(empresa=request.user.userprofile.empresa).order_by('nome')
    turmas = Turma.objects.filter(empresa=request.user.userprofile.empresa).order_by('curso__descricao', 'descricao')

    context = {
        'alunos': alunos,
        'turmas': turmas
    }

    return render(request, 'portal/matricula_new.html', context)


@staff_member_required
def matricula_edit(request):
    pass


@staff_member_required
def matricula_delete(request, matricula_id):
    matricula = get_object_or_404(Matricula, pk=matricula_id)

    if request.method == 'POST':
        matricula.delete()
        messages.success(request, 'Matrícula excluída.')

    return redirect('matricula')


@staff_member_required
def usuario_lista(request):
    usuarios_inativos = User.objects.filter(userprofile__empresa=request.user.userprofile.empresa, is_active=False)
    usuarios_ativos = User.objects.filter(userprofile__empresa=request.user.userprofile.empresa, is_active=True)

    context = {
        'usuarios_inativos': usuarios_inativos,
        'usuarios_ativos': usuarios_ativos,
    }
    return render(request, 'portal/usuario_lista.html', context)


@staff_member_required
def usuario_confirmar(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        usuario.is_active = True
        usuario.save()

        email = []
        email.append(usuario.email)

        ConfirmaUsuarioMail(usuario).send(email)

        messages.success(request, 'Usuário ativo.')

        return redirect('usuario_lista')

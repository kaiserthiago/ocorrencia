import json
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from tablib import Dataset

from portal.emails import RegistraOcorrenciaMail
from portal.forms import OcorrenciaForm, CursoForm, TurmaForm, AlunoForm
from portal.models import Curso, Aluno, Turma, Ocorrencia, Matricula, CategoriaFalta, Falta, Teste
from portal.resources import MatriculaResource, TesteResource


def home(request):
    return render(request, 'portal/home.html', {})


def contato(request):
    return render(request, 'portal/contato.html', {})


@login_required
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

        for n in imported_data:
            lista.append(n[0])

        for teste in lista:
            aluno = get_object_or_404(Aluno, nome=teste)
            matricula = Matricula.objects.filter(aluno=aluno, ano_letivo=int(date.today().year))

            if teste == aluno.nome and not matricula:
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

    cursos = Curso.objects.all().order_by('descricao')

    context = {
        'cursos': cursos
    }

    return render(request, 'portal/import_matricula.html', context)


@login_required
def import_aluno(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())

        lista = []

        importado = 0
        nao_importado = 0

        for n in imported_data:
            lista.append(n[0])

        for teste in lista:
            aluno = Aluno.objects.filter(nome=teste)

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


@login_required
def aluno(request):
    alunos = Aluno.objects.all().order_by('nome')

    context = {
        'alunos': alunos,
    }

    return render(request, 'portal/aluno.html', context)


@login_required
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


@login_required
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


@login_required
def aluno_delete(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)

    if request.method == 'POST':
        aluno.delete()
        messages.success(request, 'Aluno excluído.')

    return redirect('aluno')


@login_required
def curso(request):
    cursos = Curso.objects.all().order_by('descricao')

    context = {
        'cursos': cursos
    }

    return render(request, 'portal/curso.html', context)


@login_required
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


@login_required
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


@login_required
def curso_delete(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)

    if request.method == 'POST':
        curso.delete()
    return redirect('curso')


@login_required
def dashboard(request):
    faltas = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa).order_by(
        'falta__categoria__artigo').values_list('falta__categoria__descricao').annotate(qtde=Count('id')).distinct()

    cursos = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa).order_by().values_list(
        'matricula__turma__curso__descricao').annotate(qtde=Count('id')).distinct()

    turmas = Ocorrencia.objects.filter(empresa=request.user.userprofile.empresa).order_by().values_list(
        'matricula__turma__curso__descricao', 'matricula__turma__descricao').annotate(qtde=Count('id')).distinct()

    # DADOS GRÁFICO DE OCORRÊNCIAS POR CATEGORIA
    categorias_faltas = [obj[0] for obj in faltas]
    qtde_categorias_faltas = [int(obj[1]) for obj in faltas]

    # DADOS GRÁFICO DE OCORRÊNCIAS POR CURSO
    cursos_ocorrencia = [obj[0] for obj in cursos]
    qtde_cursos_ocorrencia = [int(obj[1]) for obj in cursos]

    # DADOS GRÁFICO DE OCORRÊNCIAS POR TURMA
    turmas_ocorrencia = [obj[0]+' - '+obj[1] for obj in turmas]
    qtde_turmas_ocorrencia = [int(obj[2]) for obj in turmas]

    context = {
        'faltas': faltas,
        'cursos': cursos,
        'turmas': turmas,
        'categorias_faltas': json.dumps(categorias_faltas),
        'qtde_categorias_faltas': json.dumps(qtde_categorias_faltas),
        'cursos_ocorrencia': json.dumps(cursos_ocorrencia),
        'qtde_cursos_ocorrencia': json.dumps(qtde_cursos_ocorrencia),
        'turmas_ocorrencia': json.dumps(turmas_ocorrencia),
        'qtde_turmas_ocorrencia': json.dumps(qtde_turmas_ocorrencia),
    }

    return render(request, 'portal/dashboard.html', context)


@login_required
def turma(request):
    turmas = Turma.objects.all().order_by('curso', 'descricao')

    context = {
        'turmas': turmas
    }

    return render(request, 'portal/turma.html', context)


@login_required
def turma_new(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)

        if form.is_valid():
            turma = Turma()

            turma.descricao = form.cleaned_data['descricao']
            turma.curso = form.cleaned_data['curso']
            turma.user = request.user
            turma.empresa = request.user.userprofile.empresa

            turma.save()

            return redirect('turma')

    form = TurmaForm()

    context = {
        'form': form
    }

    return render(request, 'portal/turma_new.html', context)


@login_required
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
    cursos = Curso.objects.all()
    ocorrencias = Ocorrencia.objects.filter(user=request.user, data__year=date.today().year)

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

                    RegistraOcorrenciaMail(ocorrencia).send(request.user.userprofile.empresa.email_responsavel,
                                                            request.user.email, ocorrencia.matricula.turma.curso.email)
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
def ocorrencia_relatorio(request):
    pass


@login_required
def matricula(request):
    matriculas = Matricula.objects.all().order_by('-ano_letivo', 'turma', 'aluno')

    context = {
        'matriculas': matriculas
    }
    return render(request, 'portal/matricula.html', context)


@login_required
def matricula_new(request):
    alunos = Aluno.objects.all().order_by('nome')
    turmas = Turma.objects.all().order_by('curso__descricao', 'descricao')

    context = {
        'alunos': alunos,
        'turmas': turmas
    }

    return render(request, 'portal/matricula_new.html', context)


@login_required
def matricula_edit(request):
    pass


@login_required
def matricula_delete(request):
    pass

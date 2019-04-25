from django import forms
from django.contrib.auth.models import User

from portal.models import UserProfile, Ocorrencia, Curso, Turma, Aluno, ServicoCategoria, Servico, Encaminhamento, \
    Autorizacao, Configuracao, Banco, Justificativa


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': ''}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail'
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('empresa',)

        widgets = {
            'empresa': forms.Select(attrs={'class': 'mdb-select md-form colorful-select dropdown-success'}),
        }

        labels = {
            'empresa': 'Unidade de lotação'
        }


class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ('data', 'descricao', 'disciplina', 'providencias')

        widgets = {
            'data': forms.TextInput(attrs={
                'class': 'form-control datepicker',
                'placeholder': 'Clique para selecionar'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control md-textarea validate',
                'placeholder': 'Utilize esse espaço para descrever, detalhadamente, a ocorrência',
                'rows': '3'
            }),
            'providencias': forms.Textarea(attrs={
                'class': 'form-control md-textarea validate',
                'placeholder': 'Utilize esse espaço para descrever as providências adotadas',
                'rows': '3',
                'required': 'required'
            }),
            'disciplina': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Informe a disciplina'
            })
        }

        labels = {
            'descricao': 'Descrição da ocorrência',
            'providencias': 'Providências adotadas'
        }


class EncaminhamentoForm(forms.ModelForm):
    class Meta:
        model = Encaminhamento
        fields = ('data', 'descricao', 'providencias', 'outras_informacoes')

        widgets = {
            'data': forms.TextInput(attrs={
                'class': 'form-control datepicker',
                'placeholder': 'Clique para selecionar',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control md-textarea validate',
                'rows': '3',
                'required': ''
            }),
            'providencias': forms.Textarea(attrs={
                'class': 'form-control md-textarea validate',
                'placeholder': 'Utilize esse espaço para descrever as providências adotadas',
                'rows': '6',
                'required': 'required'
            }),
            'outras_informacoes': forms.Textarea(attrs={
                'class': 'form-control md-textarea validate',
                'rows': '3'
            }),
        }

        labels = {
            'descricao': 'Descrição',
            'providencias': 'Providências adotadas',
            'outras_informacoes': 'Outras informações que julgue necessárias',
        }


class JustificativaForm(forms.ModelForm):
    class Meta:
        model = Justificativa
        fields = ('data_inicial', 'descricao', 'tempo_afastamento', 'motivo_indeferimento')

        widgets = {
            'data_inicial': forms.TextInput(attrs={
                'class': 'form-control datepicker',
                'placeholder': 'Clique para selecionar',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control md-textarea validate',
                'placeholder': 'Utilize esse espaço para descrever sua justificativa de faltas e/ou trabalho/prova.',
                'rows': '4',
                'required': 'required'
            }),
            'motivo_indeferimento': forms.Textarea(attrs={
                'class': 'form-control md-textarea validate',
                'placeholder': 'Utilize esse espaço para descrever o motivo do INDEFERIMENTO do pedido de justificativa',
                'rows': '4',
            }),
            'tempo_afastamento': forms.NumberInput(attrs={
                'class': 'form-control md-textarea validate',
                'required': 'required'
            }),
        }

        labels = {
            'descricao': 'Descrição da Justificativa',
            'data_inicial': 'Data de início do afastamento',
            'tempo_afastamento': 'Quantidade de dias de afastamento',
            'motivo_indeferimento': 'Motivação do indeferimento'
        }


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('descricao', 'email')

        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control validate',
                'required': '',
                'autofocus': ''
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control validate'
            })
        }

        labels = {
            'descricao': 'Descrição',
            'email': 'E-mail Coordenação'
        }


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ('descricao', 'turno')

        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control validate',
                'required': '',
                'autofocus': ''
            }),
            'turno': forms.TextInput(attrs={
                'class': 'form-control validate',
                'required': ''
            })
        }

        labels = {
            'descricao': 'Descrição'
        }


class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        exclude = ('user', 'empresa')

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control validate',
                'required': '',
                'autofocus': ''
            }),
            'numero': forms.NumberInput(attrs={
                'class': 'form-control validate'
            })
        }

        labels = {
            'numero': 'Número'
        }


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        exclude = ('user', 'empresa')

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control validate',
                'required': '',
                'autofocus': '',
                'style': 'text-transform:uppercase'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control validate',
            }),
            'pai': forms.TextInput(attrs={
                'class': 'form-control validate',
                'style': 'text-transform:uppercase'
            }),
            'mae': forms.TextInput(attrs={
                'class': 'form-control validate',
                'style': 'text-transform:uppercase'
            }),
            'rg': forms.TextInput(attrs={
                'class': 'form-control validate',
                'style': 'text-transform:uppercase'
            }),
            'emissor': forms.TextInput(attrs={
                'class': 'form-control validate',
                'style': 'text-transform:uppercase'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control validate',
            }),
            'email_responsavel': forms.EmailInput(attrs={
                'class': 'form-control validate',
            }),
            'foto': forms.FileInput(attrs={
                'class': 'file-path validate'
            }),
            'banco': forms.Select(attrs={
                'class': 'mdb-select md-form colorful-select dropdown-success'
            }),
            'agencia': forms.TextInput(attrs={
                'class': 'form-control validate',
            }),
            'conta': forms.TextInput(attrs={
                'class': 'form-control validate',
            }),
            'numero_matricula': forms.TextInput(attrs={
                'class': 'form-control validate',
            }),
            'contato': forms.Textarea(attrs={
                'class': 'form-control md-textarea validate',
                'rows': '2'
            }),
            'pcd': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'cid': forms.TextInput(attrs={
                'class': 'form-control validate'
            }),
            'pcd_descricao': forms.TextInput(attrs={
                'class': 'form-control validate'
            })

        }

        labels = {
            'email': 'E-mail aluno',
            'pai': 'Nome do pai',
            'mae': 'Nome da mãe',
            'rg': 'RG',
            'cpf': 'CPF',
            'emissor': 'Órgão emissor',
            'email_responsavel': 'E-mail responsável',
            'agencia': 'Agência',
            'numero_matricula': 'Nº Matrícula',
            'pcd_descricao': 'Descrição da deficiência'
        }


class ServicoCategoriaForm(forms.ModelForm):
    class Meta:
        model = ServicoCategoria
        exclude = ('user', 'empresa')

        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control validate',
                'required': '',
                'autofocus': ''
            }),
        }

        labels = {
            'descricao': 'Descrição',
        }


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        exclude = ('categoria', 'user', 'empresa')

        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control validate',
                'required': '',
                'autofocus': ''
            }),
        }

        labels = {
            'descricao': 'Descrição',
        }


class AutorizacaoForm(forms.ModelForm):
    class Meta:
        model = Autorizacao
        fields = ('data', 'descricao')

        widgets = {
            'data': forms.TextInput(attrs={
                'class': 'form-control datepicker',
                'placeholder': 'Clique para selecionar'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control md-textarea validate',
                'rows': '3'
            }),
        }

        labels = {
            'descricao': 'Descrição',
        }


class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = Configuracao
        exclude = ('user', 'empresa')

        widgets = {
            'ocorrencia_email_aluno': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'ocorrencia_email_responsavel_aluno': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'ocorrencia_email_responsavel_user': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'ocorrencia_email_responsavel_setor': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'ocorrencia_email_coordenacao_curso': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'encaminhamento_email_aluno': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'encaminhamento_email_responsavel_aluno': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'encaminhamento_email_responsavel_user': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'encaminhamento_email_responsavel_setor': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'encaminhamento_email_coordenacao_curso': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'providencia_ocorrencia_email_aluno': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'providencia_ocorrencia_email_responsavel_aluno': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'providencia_ocorrencia_email_responsavel_user': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'providencia_ocorrencia_email_responsavel_setor': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'providencia_ocorrencia_email_coordenacao_curso': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'providencia_encaminhamento_email_aluno': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'providencia_encaminhamento_email_responsavel_aluno': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'providencia_encaminhamento_email_responsavel_user': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'providencia_encaminhamento_email_responsavel_setor': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'providencia_encaminhamento_email_coordenacao_curso': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'autorizacao_email_aluno': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'autorizacao_email_responsavel_aluno': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'autorizacao_email_responsavel_user': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'autorizacao_email_responsavel_setor': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'autorizacao_email_coordenacao_curso': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'justificativa_email_aluno': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'justificativa_email_retorno_aluno': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'justificativa_email_setor': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

        labels = {
            'ocorrencia_email_aluno': 'Estudante',
            'ocorrencia_email_responsavel_aluno': 'Responsável',
            'ocorrencia_email_responsavel_user': 'Servidor',
            'ocorrencia_email_responsavel_setor': 'CAED/DEPAE',
            'ocorrencia_email_coordenacao_curso': 'Coordenador',

            'encaminhamento_email_aluno': 'Estudante',
            'encaminhamento_email_responsavel_aluno': 'Responsável',
            'encaminhamento_email_responsavel_user': 'Servidor',
            'encaminhamento_email_responsavel_setor': 'CAED/DEPAE',
            'encaminhamento_email_coordenacao_curso': 'Coordenador',

            'providencia_encaminhamento_email_aluno': 'Estudante',
            'providencia_encaminhamento_email_responsavel_aluno': 'Responsável',
            'providencia_encaminhamento_email_responsavel_user': 'Servidor/Aluno',
            'providencia_encaminhamento_email_responsavel_setor': 'CAED/DEPAE',
            'providencia_encaminhamento_email_coordenacao_curso': 'Coordenador',

            'providencia_ocorrencia_email_aluno': 'Estudante',
            'providencia_ocorrencia_email_responsavel_aluno': 'Responsável',
            'providencia_ocorrencia_email_responsavel_user': 'Servidor/Aluno',
            'providencia_ocorrencia_email_responsavel_setor': 'CAED/DEPAE',
            'providencia_ocorrencia_email_coordenacao_curso': 'Coordenador',

            'autorizacao_email_aluno': 'Estudante',
            'autorizacao_email_responsavel_aluno': 'Responsável',
            'autorizacao_email_responsavel_user': 'Servidor',
            'autorizacao_email_responsavel_setor': 'CAED/DEPAE',
            'autorizacao_email_coordenacao_curso': 'Coordenador',

            'justificativa_email_retorno_aluno': 'Retorno estudante',
            'justificativa_email_aluno': 'Estudante',
            'justificativa_email_setor': 'CAED/DEPAE'
        }

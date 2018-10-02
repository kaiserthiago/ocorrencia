from django import forms
from django.contrib.auth.models import User

from portal.models import UserProfile, Ocorrencia, Curso, Turma, Aluno, ServicoCategoria, Servico, Encaminhamento, \
    Autorizacao, Configuracao, Banco


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
        fields = ('data', 'descricao')

        widgets = {
            'data': forms.TextInput(attrs={
                'class': 'form-control datepicker',
                'placeholder': 'Clique para selecionar'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control md-textarea validate',
                'rows': '3'
            })
        }

        labels = {
            'descricao': 'Descrição da ocorrência'
        }


class EncaminhamentoForm(forms.ModelForm):
    class Meta:
        model = Encaminhamento
        fields = ('data', 'descricao', 'providencias', 'outras_informacoes')

        widgets = {
            'data': forms.TextInput(attrs={
                'class': 'form-control datepicker',
                'placeholder': 'Clique para selecionar'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control md-textarea validate',
                'rows': '3'
            }),
            'providencias': forms.Textarea(attrs={
                'class': 'form-control md-textarea validate',
                'rows': '3'
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
        fields = ('descricao',)

        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control validate',
                'required': '',
                'autofocus': ''
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

        }

        labels = {
            'email': 'E-mail aluno',
            'pai': 'Nome do pai',
            'mae': 'Nome da mãe',
            'rg': 'RG',
            'cpf': 'CPF',
            'emissor': 'Órgão emissor',
            'email_responsavel': 'E-mail responsável',
            'agencia': 'Agência'
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
            'providencia_encaminhamento_email_responsavel_user': 'Servidor',
            'providencia_encaminhamento_email_responsavel_setor': 'CAED/DEPAE',
            'providencia_encaminhamento_email_coordenacao_curso': 'Coordenador',

            'autorizacao_email_aluno': 'Estudante',
            'autorizacao_email_responsavel_aluno': 'Responsável',
            'autorizacao_email_responsavel_user': 'Servidor',
            'autorizacao_email_responsavel_setor': 'CAED/DEPAE',
            'autorizacao_email_coordenacao_curso': 'Coordenador',
        }

from django import forms
from django.contrib.auth.models import User

from portal.models import UserProfile, Ocorrencia, Curso, Turma, Aluno


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
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
            'empresa': forms.Select(attrs={'class': 'mdb-select colorful-select dropdown-primary'})
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
                'class': 'md-textarea validate'
            })
        }

        labels = {
            'descricao': 'Descrição da ocorrência'
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


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        exclude = ('user',)

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control validate',
                'required': '',
                'autofocus': ''
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control validate',
            }),
            'responsavel': forms.TextInput(attrs={
                'class': 'form-control validate',
            }),
            'email_responsavel': forms.EmailInput(attrs={
                'class': 'form-control validate',
            }),
            'empresa': forms.Select(attrs={
                'class': 'mdb-select colorful-select dropdown-primary',
                'required': ''
            })
        }

        labels = {
            'empresa': 'Câmpus',
            'email': 'E-mail aluno',
            'responsavel': 'Responsável',
            'email_responsavel': 'E-mail responsável',
        }

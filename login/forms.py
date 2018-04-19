from django import forms
from django.contrib.auth.models import User


class RegistroForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': 'True', 'max_lenght': '150'}), label='Nome')

    # last_name = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'required': 'True', 'max_lenght': '150'}), label='Sobrenome')

    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': 'True', 'max_lenght': '30'}), label='Usuário', error_messages={
        'invalid': 'Usuário pode conter apenas letras e números'
    })

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': 'True', 'max_lenght': '30'}), label='E-mail')

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'required': 'True', 'max_lenght': '30', 'render_value': 'False'}),
        label='Senha')

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'required': 'True', 'max_lenght': '30', 'render_value': 'False'}),
        label='Repita senha')

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError('Esse usuário já existe')

    def clean(self):
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError('As senhas informadas devem ser iguais')

        return self.cleaned_data

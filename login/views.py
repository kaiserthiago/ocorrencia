from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect, get_object_or_404

from login.forms import RegistroForm
from portal.emails import ResponsavelUsuarioMail, RegistraUsuarioMail
from portal.forms import UserProfileForm
from portal.models import UserProfile, Empresa


def register(request):
    unidades = Empresa.objects.all().order_by('nome_fantasia')

    if request.method == 'POST':
        user_form = RegistroForm(request.POST)

        if user_form.is_valid():
            User.objects.create_user(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'],
                email=user_form.cleaned_data['email'],
                first_name=user_form.cleaned_data['first_name'],
                # last_name=user_form.cleaned_data['last_name'],
                is_active=False,
            )

            id = request.POST['SelectUnidade']
            empresa = get_object_or_404(Empresa, id=id)

            usuario = get_object_or_404(User, username=user_form.cleaned_data['username'])

            profile = UserProfile()
            profile.user = usuario
            profile.empresa = empresa
            profile.siape = int(request.POST['username'])

            profile.save()

            email = []
            email_user = []

            email.append(empresa.email_responsavel_sistema)
            email_user.append(usuario.email)

            ResponsavelUsuarioMail(usuario).send(email)
            RegistraUsuarioMail(usuario).send(email_user)

            return redirect('login_register_success')

    user_form = RegistroForm()

    context = {
        'user_form': user_form,
        'unidades': unidades
    }
    return render(request, 'registration/login.html', context)


def register_success(request):
    return render_to_response('registration/register_success.html', {})

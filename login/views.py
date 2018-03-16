from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect, get_object_or_404

from login.forms import RegistroForm
from portal.forms import UserProfileForm
from portal.models import UserProfile

@staff_member_required
def register(request):
    if request.method == 'POST':
        user_form = RegistroForm(request.POST)

        if user_form.is_valid():
            User.objects.create_user(
                username=user_form.cleaned_data['username'].lower(),
                password=user_form.cleaned_data['password'],
                email=user_form.cleaned_data['email'],
                first_name=user_form.cleaned_data['first_name'],
                last_name=user_form.cleaned_data['last_name']
            )
            # new_user = authenticate(username=user_form.cleaned_data['username'],
            #                         password=user_form.cleaned_data['password'],
            #                         )
            # login(request, new_user)

            return redirect('register_success')
    else:
        user_form = RegistroForm()

    context = {
        'user_form': user_form,
    }
    return render(request, 'registration/register.html', context)



def register_success(request):
    return render_to_response('registration/register_success.html', {})

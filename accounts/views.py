from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ProfileForm, ChangePasswordForm

NEW_PASSWORD_RULES = [
    'Must be at least 8 charcters long',
    'Must contain both lower and upper case letters',
    'Must contain at least one number',
    'Can not contain the user\'s first or last name',
    'Can not contain the username associated with the account',
    'Must contain one of the following characters: @ ! $ # *'
]


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:profile')
                    )
                else:
                    messages.error(
                        request,
                        'That user account has been disabled.'
                    )
        else:
            messages.error(
                request,
                'Username or password is incorrect.'
            )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                'You\'ve been signed up! We signed you in too.'
            )
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, 'You\'ve been signed out! Come back soon.')
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'profile': request.user.profile})


@login_required
def edit_profile(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(
            data=request.POST,
            instance=request.user.profile,
            files=request.FILES
        )
        if form.is_valid():
            profile = form.save(commit=False)
            profile.is_new = False
            profile.save()
            messages.success(
                request,
                'Your profile has been updated!'
            )
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    user = request.user
    form = ChangePasswordForm(user=user)
    if request.method == 'POST':
        form = ChangePasswordForm(user=user,data=request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            messages.success(request, 'Your password was updated successfully, please sign in using your new password.')
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/change_password_form.html', {'form': form, 'rules': NEW_PASSWORD_RULES})
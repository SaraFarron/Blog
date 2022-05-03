from re import template
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from datetime import datetime, timezone

from BlogApp.decorators import unauthenticated_user
from BlogApp.models import Comment, Post
from .forms import *
from .utils import create_token, seconds_to_formatted_string


NEWLO = True


class LoginPage(View):
    @method_decorator(unauthenticated_user)
    def get(self, request):
        template = 'user/login.html' if not NEWLO else 'new-layout/user/login.html'
        return render(request, template)

    @method_decorator(unauthenticated_user)
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('blog:home')
        else:
            messages.info(request, 'Username or password is incorrect')

        template = 'user/login.html' if not NEWLO else 'new-layout/user/login.html'
        return render(request, template)


class RegisterPage(View):
    @method_decorator(unauthenticated_user)
    def post(self, request):
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            token = create_token(user)
            cleaned_data = form.cleaned_data
            username, email = cleaned_data['username'], cleaned_data['email']
            guest = Guest.objects.create(
                user=user,
                name=username,
                token=token.key,
                email=email,
            )
            guest.save()
            login(request, user)
            messages.success(request, f'Account {username} created successfully')

            context = {'user': guest}
            return render(request, 'user/profile.html', context)
        else:
            messages.error(request, 'Passwords are different or this username has been taken')
            template = 'user/register.html' if not NEWLO else 'new-layout/user/register.html'
            return render(request, template )

    @method_decorator(unauthenticated_user)
    def get(self, request):
        template = 'user/register.html' if not NEWLO else 'new-layout/user/register.html'
        return render(request, template )


class LogoutUser(View):
    @method_decorator(login_required(login_url='user:login'))
    def get(self, request):
        logout(request)
        return redirect('user:login')


class Profile(View):
    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, pk):
        try:
            user = Guest.objects.get(user=pk)
        except ObjectDoesNotExist:
            return render(request, 'user/guest_does_not_exist.html')
        posts = Post.objects.filter(user=user).order_by('-creation_date')
        comments = Comment.objects.filter(user=user)
        saves_posts = Post.objects.filter(saved_by=user)
        last_time_banned = user.last_ban_date
        context = {'posts': posts,
                   'comments': comments, 'user': user,
                   'request_user': request.user,
                   'saves_posts': saves_posts}

        if last_time_banned:
            time_since_ban = datetime.now(timezone.utc) - last_time_banned
            time_since_ban = seconds_to_formatted_string(time_since_ban)
            context['time_since_ban'] = time_since_ban
        return render(request, 'user/profile.html' if not NEWLO else 'new-layout/user/profile.html', context)


class ProfileSettings(View):
    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, pk):
        user = Guest.objects.get(name=request.user)
        form = ProfileSetForm(instance=user)

        context = {'form': form, 'user': user}
        return render(request, 'user/profile_settings.html', context)

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, pk):
        user = Guest.objects.get(name=request.user)
        form = ProfileSetForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

        context = {'form': form}
        return render(request, 'user/profile_settings.html', context)

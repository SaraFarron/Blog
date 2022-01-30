from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.authtoken.models import Token
from datetime import datetime, timezone

from BlogApp.decorators import *
from .forms import *


class LoginPage(View):

    @method_decorator(unauthenticated_user)
    def get(self, request):

        context = {}
        return render(request, 'user/login.html', context)

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

        context = {}
        return render(request, 'user/login.html', context)


class RegisterPage(View):

    @method_decorator(unauthenticated_user)
    def post(self, request):

        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            token = Token.objects.create(user=user)
            token.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            login(request, user)
            guest = Guest.objects.create(
                user=user,
                name=username,
                token=token.key,
                email=email,
            )
            guest.save()
            messages.success(request, f'Account {username} created successfully')

            context = {'user': guest}
            return render(request, 'user/profile.html', context)

        else:
            messages.error(request, 'Passwords are different or this username has been taken')
            return render(request, 'user/register.html')

    @method_decorator(unauthenticated_user)
    def get(self, request):

        context = {}
        return render(request, 'user/register.html', context)


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

        posts = Post.objects.filter(user=user)
        last_time_banned = user.last_ban_date

        context = {'posts': posts, 'user': user, 'request_user': request.user}

        if last_time_banned:
            time_since_ban = datetime.now(timezone.utc) - last_time_banned
            seconds = time_since_ban.seconds

            match seconds:
                case seconds if seconds > 86400: time_since_ban = str(time_since_ban.days) + ' days'
                case seconds if seconds > 3600: time_since_ban = str(round(seconds / 3600)) + ' hours'
                case seconds if seconds > 60: time_since_ban = str(round(seconds / 60)) + ' minutes'
                case _: time_since_ban = str(seconds) + ' seconds'

            context['time_since_ban'] = time_since_ban
        return render(request, 'user/profile.html', context)


class ProfileSettings(View):

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, pk):
        user = Guest.objects.get(name=request.user)
        form = ProfileSetForm(instance=user)

        context = {'form': form}
        return render(request, 'user/profile_settings.html', context)

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, pk):
        user = Guest.objects.get(name=request.user)
        form = ProfileSetForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

        context = {'form': form}
        return render(request, 'user/profile_settings.html', context)

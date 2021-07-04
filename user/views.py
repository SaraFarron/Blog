from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

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
        if request.user.is_authenticated:
            return redirect('blog:home')
        elif form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            Guest.objects.create(
                user=user,
                name=username,
            )
            messages.success(request, f'Account {username} created successfully')
            return HttpResponseRedirect(reverse('user:profile', args=(username,)))

    @method_decorator(unauthenticated_user)
    def get(self, request):
        context = {}
        return render(request, 'user/register.html', context)


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('user:login')


class Profile(View):

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request):
        user = Guest.objects.get(name=request.user)
        posts = Post.objects.filter(user=user)
        profile_picture = user.profile_picture.url

        context = {'posts': posts, 'user': user, 'pfp': profile_picture}
        return render(request, 'user/profile.html', context)


class ProfileSettings(View):

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request):
        user = Guest.objects.get(name=request.user)
        profile_picture = user.profile_picture.url
        form = ProfileSetForm(instance=user)

        if request.method == 'POST':
            form = ProfileSetForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()

        context = {'pfp': profile_picture, 'form': form}
        return render(request, 'user/profile_settings.html', context)

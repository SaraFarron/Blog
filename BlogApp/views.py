from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import View
from django.utils.decorators import method_decorator

from .decorators import *
from .forms import *


class Home(View):

    @method_decorator(login_required(login_url='Blog:login'))
    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all().order_by('user')
        except TypeError:
            template = loader.get_template('Blog/unauthenticated.html')
            return HttpResponse(template.render())

        context = {'posts': posts, 'user': request.user.username}
        return render(request, 'index.html', context)


class HomeByDate(View):
    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all().order_by('-creation_date')
        except TypeError:
            template = loader.get_template('Blog/unauthenticated.html')
            return HttpResponse(template.render())

        context = {'posts': posts, 'user': request.user.username}
        return render(request, 'index.html', context)


class PostPage(View):

    @method_decorator(login_required(login_url='Blog:login'))
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=post)

        context = {'post': post, 'comments': comments}
        return render(request, 'Blog/post.html', context)


class CreatePost(View):

    @method_decorator(login_required(login_url='Blog:login'))
    def get(self, request, *args, **kwargs):
        form = PostForm

        context = {'form': form}
        return render(request, 'Blog/create_post.html', context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = Guest.objects.get(name=request.user)
            form.save()
            return redirect('Blog:home')
        form = PostForm

        context = {'form': form}
        return render(request, 'Blog/create_post.html', context)


class UpdatePost(View):
    decorators = [login_required(login_url='Blog:login'), user_owns_the_post]

    @method_decorator(decorators)
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        form = PostForm(instance=post)
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('Blog:home')

        context = {'form': form}
        return render(request, 'Blog/create_post.html', context)


class DeletePost(View):
    decorators = [login_required(login_url='Blog:login'), user_owns_the_post]

    @method_decorator(decorators)
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        if request.method == 'POST':
            post.delete()
            return redirect('Blog:home')

        context = {'post': post}
        return render(request, 'Blog/delete_post.html', context)


class LoginPage(View):

    @method_decorator(unauthenticated_user)
    def get(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Blog:home')
        else:
            messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, 'Blog/login.html', context)


# TODO Make redirect if user is authenticated
class RegisterPage(View):
    def get(self, request):
        form = CreateUserForm(request.POST)
        user = request.user
        if user.is_authenticated:
            return redirect('Blog:profile')
        elif form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            Guest.objects.create(
                user=user,
                name=username,
            )
            messages.success(request, f'Account {username} created successfully')
            return HttpResponseRedirect(reverse('Blog:profile', args=(username,)))


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('Blog:login')


class Profile(View):

    @method_decorator(login_required(login_url='Blog:login'))
    def get(self, request, pk):
        user = Guest.objects.get(name=pk)
        posts = Post.objects.filter(user=user)
        profile_picture = user.profile_picture.url

        context = {'posts': posts, 'user': user, 'pfp': profile_picture}
        return render(request, 'Blog/profile.html', context)


class CreateComment(View):

    @method_decorator(login_required(login_url='Blog:login'))
    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(id=pk)
            form.instance.author = Guest.objects.get(name=request.user)
            form.instance.post = Post.objects.get(id=pk)
            form.save()
            return HttpResponseRedirect(reverse('Blog:post', args=(post.id,)))
        form = CommentForm

        context = {'form': form}
        return render(request, 'Blog/create_post.html', context)

    @method_decorator(login_required(login_url='Blog:login'))
    def get(self, request, pk):
        form = CommentForm

        context = {'form': form}
        return render(request, 'Blog/create_post.html', context)



class ProfileSettings(View):

    @method_decorator(login_required(login_url='Blog:login'))
    def get(self, request):
        user = Guest.objects.get(name=request.user)
        profile_picture = user.profile_picture.url
        form = ProfileSetForm(instance=user)

        if request.method == 'POST':
            form = ProfileSetForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()

        context = {'pfp': profile_picture, 'form': form}
        return render(request, 'Blog/profile_settings.html', context)

# TODO Switch to class-based views

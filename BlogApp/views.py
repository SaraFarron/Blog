from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .decorators import *
from .forms import *


def index(request):

    try:
        posts = Post.objects.all().order_by('user')
    except TypeError:
        template = loader.get_template('Blog/unauthenticated.html')
        return HttpResponse(template.render())

    context = {'posts': posts, 'user': request.user.username}
    return render(request, 'index.html', context)


def index_order_by_date(request):

    try:
        posts = Post.objects.all().order_by('creation_date')
    except TypeError:
        template = loader.get_template('Blog/unauthenticated.html')
        return HttpResponse(template.render())

    context = {'posts': posts, 'user': request.user.username}
    return render(request, 'index.html', context)


@login_required(login_url='login')
def post_page(request, pk):

    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=post)
    
    context = {'post': post, 'comments': comments}
    return render(request, 'Blog/post.html', context)


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = Guest.objects.get(name=request.user)
            form.save()
            return redirect('Blog:home')
    form = PostForm

    context = {'form': form}
    return render(request, 'Blog/create_post.html', context)


@user_owns_the_post
@login_required(login_url='login')
def update_post(request, pk):

    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('Blog:home')

    context = {'form': form}
    return render(request, 'Blog/create_post.html', context)


@user_owns_the_post
@login_required(login_url='login')
def delete_post(request, pk):

    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('Blog:home')

    context = {'post': post}
    return render(request, 'Blog/delete_post.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
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


# @unauthenticated_user
def register_page(request):
    """TODO error while redirect, reverse doesn't work"""

    if request.user.is_authenticated:
        return redirect('Blog:home')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            Guest.objects.create(
                user=user,
                name=username,
            )

            messages.success(request, f'Account {username} created successfully')
            return redirect(f'Blog:profile/{username}')  # error here
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'Blog/register.html', context)


def logout_user(request):
    logout(request)
    return redirect('Blog:login')


def profile(request, pk):

    user = Guest.objects.get(name=pk)
    posts = Post.objects.filter(user=user)

    context = {'posts': posts, 'user': user}
    return render(request, 'Blog/profile.html', context)


def create_comment(request, pk):

    if request.method == 'POST':
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

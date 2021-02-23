from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.template import loader

from .decorators import *
from .models import *
from .forms import *


def index(request):  # order_by()

    try:
        posts = Post.objects.all()
    except TypeError:
        template = loader.get_template('Blog/unauthenticated.html')
        return HttpResponse(template.render())

    if request.GET.get('order_by_author'):
        posts = Post.objects.all().order_by('user')
    elif request.GET.get('order_by_date'):
        posts = Post.objects.all().order_by('creation_date')
    
    # if request.method == 'GET':


    context = {'posts': posts}
    return render(request, 'index.html', context)


# def order_post_by_author(request):

#     posts = Post.objects.order_by('user')

#     context = {'posts': posts}
#     return render(request, 'index.html', context)


# def order_post_by_date(request):

#     posts = Post.objects.order_by('creation_date')

#     context = {'posts': posts}
#     return render(request, 'index.html', context)



@login_required(login_url='login')
def post_page(request, pk):

    post = Post.objects.get(id=pk)
    
    context = {'post': post}
    return render(request, 'Blog/post.html', context)


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('Blog:home')
    form = PostForm

    context = {'form': form}
    return render(request, 'Blog/create_post.html', context)


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


@unauthenticated_user
def register_page(request):
    form = CreateUserForm
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='guest')
            user.groups.add(group)
            Guest.objects.create(
                user=user,
                name=username,
            )
            messages.success(request, f'Account {username} created successfully')
            return redirect('Blog:login')  # redirect to profile page
        else:
            pass

    context = {'form': form}
    return render(request, 'Blog/register.html', context)


def logout_user(request):
    logout(request)
    return redirect('Blog:login')


def profile(request, pk):

    user = Guest.objects.filter(id=pk)
    posts = Post.objects.filter(user=request.user)

    context = {'posts': posts, 'user':user}
    return render(request, 'Blog/profile.html', context)

# TODO create a post page with dynamic url | backend ready
# TODO user profile page, that includes:
#  name, last name, avatar, email , phone, skype, posts
# TODO home page shows all posts, posts has author name,
#  can be sorted by date and author
# TODO Users can leave comments under posts (cannot comment your own post)

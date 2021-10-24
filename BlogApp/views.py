from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import *
from .forms import *


class Home(View):

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request):
        try:
            posts = Post.objects.all().order_by('user')
        except TypeError:
            template = loader.get_template('blog/unauthenticated.html')
            return HttpResponse(template.render())

        context = {'posts': posts, 'user': request.user.username}
        return render(request, 'index.html', context)


class HomeByDate(View):
    def get(self, request):
        try:
            posts = Post.objects.all().order_by('-creation_date')
        except TypeError:
            template = loader.get_template('blog/unauthenticated.html')
            return HttpResponse(template.render())

        context = {'posts': posts, 'user': request.user.username}
        return render(request, 'index.html', context)


class PostPage(View):

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=post)

        context = {'post': post, 'comments': comments}
        return render(request, 'blog/post.html', context)


class CreatePost(View):

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, ):
        form = PostForm

        context = {'form': form}
        return render(request, 'blog/create_post.html', context)

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, ):
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = Guest.objects.get(name=request.user)
            form.save()
            return redirect('blog:home')
        form = PostForm

        context = {'form': form}
        return render(request, 'blog/create_post.html', context)


class UpdatePost(View):
    decorators = [login_required(login_url='user:login'), user_owns_the_post]

    @method_decorator(decorators)
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        form = PostForm(instance=post)

        context = {'form': form}
        return render(request, 'blog/create_post.html', context)

    @method_decorator(decorators)
    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('blog:home')

        context = {'form': form}
        return render(request, 'blog/create_post.html', context)


class DeletePost(View):
    decorators = [login_required(login_url='user:login'), user_owns_the_post]

    @method_decorator(decorators)
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        context = {'post': post}
        return render(request, 'blog/delete_post.html', context)

    @method_decorator(decorators)
    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        post.delete()
        return redirect('blog:home')


class CreateComment(View):

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(id=pk)
            form.instance.author = Guest.objects.get(name=request.user)
            form.instance.post = Post.objects.get(id=pk)
            form.save()
            return HttpResponseRedirect(reverse('blog:post', args=(post.id,)))
        form = CommentForm

        context = {'form': form}
        return render(request, 'blog/create_post.html', context)

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, pk):
        form = CommentForm

        context = {'form': form}
        return render(request, 'blog/create_post.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import *
from .forms import *


class Home(View):
    def get(self, request):
        posts = Post.objects.all().order_by('user')

        context = {'posts': posts, 'user': request.user}
        return render(request, 'index.html', context)


class HomeByDate(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-creation_date')

        context = {'posts': posts, 'user': request.user.username}
        return render(request, 'index.html', context)


class PostPage(View):

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=post)
        replies = []
        for comment in comments:
            replies += list(comment.replies.all())
        for reply in replies:
            comments = comments.exclude(id=reply.id)

        context = {'post': post, 'comments': comments}
        return render(request, 'blog/post.html', context)


class CreatePost(View):

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, ):
        user = Guest.objects.get(name=request.user.username)

        if user.is_banned:
            return render(request, '403page.html')

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
            author = Guest.objects.get(name=request.user)

            form.instance.user = author
            form.instance.post = post
            form.instance.post.number_of_comments += 1
            form.save()

            return HttpResponseRedirect(reverse('blog:post', args=(post.id,)))
        form = CommentForm

        context = {'form': form}
        return render(request, 'blog/create_comment.html', context)

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, pk):
        user = Guest.objects.get(name=request.user.username)

        if user.is_banned or user.is_muted:
            return render(request, '403page.html')

        form = CommentForm

        context = {'form': form}
        return render(request, 'blog/create_comment.html', context)


class Reply(View):

    @method_decorator(login_required(login_url='user:login'))
    def get(self, request, post_pk, comment):
        user = Guest.objects.get(name=request.user.username)

        if user.is_banned or user.is_muted:
            return render(request, '403page.html')
        form = CommentForm

        context = {'form': form}
        return render(request, 'blog/reply.html', context)

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, post_pk, comment):
        form = CommentForm(request.POST)

        if form.is_valid():
            post = Post.objects.get(id=post_pk)
            parent_comment = Comment.objects.get(id=comment)
            author = Guest.objects.get(name=request.user)

            form.instance.user = author
            form.instance.post = post
            new_comment = form.save()
            parent_comment.replies.add(new_comment)

            return HttpResponseRedirect(reverse('blog:post', args=(post.id,)))
        form = CommentForm

        context = {'form': form}
        return render(request, 'blog/reply.html', context)


def handler404(request, exception=None):
    return render(request, '404page.html')


def handler400(request, exception=None):
    return render(request, '400page.html')


def handler403(request, exception=None):
    return render(request, '403page.html')


def handler500(request, exception=None):
    return render(request, '500page.html')

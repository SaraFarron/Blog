from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from api.utils import get_comments_with_replies, update_instance_rating
from .utils import new_comment
from .decorators import user_owns_the_post
from .forms import *


class Index(View):
    def get(self, request):
        return HttpResponseRedirect('/about/')


class About(View):
    def get(self, request):
        context = {'user': request.user}
        return render(request, 'blog/about.html', context)


class Home(View):
    def get(self, request):
        request_guest = None
        if request.user.is_authenticated:
            request_guest = Guest.objects.get(id=request.user.id)
        if 'sorting' in request.COOKIES:
            sorting = request.COOKIES['sorting']
        else:
            sorting = 'novelty'

        if sorting == 'novelty':
            posts = Post.objects.select_related('user').order_by('-creation_date')
        else:
            posts = Post.objects.select_related('user').order_by('-number_of_comments')

        context = {'posts': posts, 'user': request.user, 'sorting': sorting, 'request_guest': request_guest}
        return render(request, 'blog/home.html', context)

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, ):
        request_guest = Guest.objects.get(id=request.user.id)
        if 'sorting' in request.COOKIES:
            sorting = request.COOKIES['sorting']
        else:
            sorting = 'novelty'

        if sorting == 'novelty':
            posts = Post.objects.select_related('user').order_by('-creation_date')
        else:
            posts = Post.objects.select_related('user').order_by('-number_of_comments')

        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = Guest.objects.get(name=request.user)
            form.save()
            return redirect('blog:home')

        return render(request, 'errors/400page.html')


class PostPage(View):
    def get(self, request, pk):
        request_guest = None
        if request.user.is_authenticated:
            request_guest = Guest.objects.get(id=request.user.id)
        post = Post.objects.get(id=pk)
        comments = sorted(get_comments_with_replies(post),
                          key=lambda d: d.publication_date,
                          reverse=True
                          )

        context = {'post': post, 'comments': comments, 'request_guest': request_guest}

        try:  # Occurs if user is not authorised
            user = Guest.objects.get(user=request.user)
        except TypeError:
            return render(request, 'blog/post/postpage.html', context)
        saved_by_users = post.saved_by.all()
        context |= {'user': user, 'saved_by': saved_by_users}

        return render(request, 'blog/post/postpage.html', context)


class CreatePost(View):
    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, ):
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = Guest.objects.get(name=request.user)
            form.save()
            return redirect('blog:home')

        return render(request, 'errors/400page.html')


class UpdatePost(View):
    decorators = [login_required(login_url='user:login'), user_owns_the_post]

    @method_decorator(decorators)
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        form = PostForm(instance=post)
        context = {'form': form, 'post': post}
        return render(request, 'blog/post/post-edit.html', context)

    @method_decorator(decorators)
    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('blog:home')

        context = {'form': form, 'post': post}
        return render(request, 'blog/post/post-edit.html', context)


class DeletePost(View):
    decorators = [login_required(login_url='user:login'), user_owns_the_post]

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
            new_comment(request, form, post)
            return HttpResponseRedirect(reverse('blog:post', args=(post.id,)))

        return render(request, 'errors/400page.html')


class Reply(View):

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, post_pk, comment):
        form = CommentForm(request.POST)

        if form.is_valid():
            post = Post.objects.get(id=post_pk)
            reply = new_comment(request, form, post)
            parent_comment = Comment.objects.get(id=comment)
            parent_comment.replies.add(reply)
            parent_comment.save()
            return HttpResponseRedirect(reverse('blog:post', args=(post.id,)))

        return render(request, 'errors/400page.html')


class Save(View):

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = Guest.objects.get(id=request.user.id)
        post.saved_by.add(user)
        post.save()
        return request.META.get('HTTP_REFERER')  # This might not work


class Vote(View):

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, pk):
        page = request.META.get('HTTP_REFERER')
        action = request.headers.action  # TODO
        if 'post' in page:
            instance = Post.objects.get(pk=pk)
        elif 'comment' in page:
            instance = Comment.objects.get(pk=pk)
        else:
            return render(request, 'errors/400page.html')

        user = Guest.objects.get(id=request.user.id)
        if action == 'upvote':
            instance.upvoted_users.add(user)
        elif action == 'downvote':
            instance.downvoted_users.add(user)
        instance.save()
        update_instance_rating(instance)  # This might lead to duplicated requests
        return request.META.get('HTTP_REFERER')  # This might not work


def handler404(request, exception=None): return render(request, 'errors/404page.html')


def handler400(request, exception=None): return render(request, 'errors/400page.html')


def handler403(request, exception=None): return render(request, 'errors/403page.html')


def handler500(request, exception=None): return render(request, 'errors/500page.html')

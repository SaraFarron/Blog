from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from api.utils import get_comments_with_replies, update_instance_rating
from .utils import new_comment, get_instance
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

        posts = Post.objects.prefetch_related(
            'user',
            'saved_by',
            'upvoted_users',
            'downvoted_users'
        )

        if sorting == 'novelty':
            posts.order_by('-creation_date')
        else:
            posts.order_by('-number_of_comments')

        context = {'posts': posts, 'user': request.user, 'sorting': sorting, 'request_guest': request_guest}
        return render(request, 'blog/home.html', context)

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, ):
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
        post = Post.objects.select_related('user').get(id=pk)
        comments = sorted(get_comments_with_replies(post),
                          key=lambda d: d.publication_date,
                          reverse=True
                          )

        context = {'post': post, 'comments': comments, 'request_guest': request_guest}

        try:  # Occurs if user is not authorised
            user = Guest.objects.get(user=request.user)
        except TypeError:
            return render(request, 'blog/post/postpage.html', context)
        context |= {'user': user}

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


#Supposed to work with iframe
class Save(View):

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, pk):
        user = Guest.objects.get(id=request.user.id)
        model = request.POST['element']
        instance = get_instance(model, pk)

        if user in instance.saved_by.all():
            instance.saved_by.remove(user)
        else:
            instance.saved_by.add(user)

        instance.save()
        return render(request, 'empty.html')


#Supposed to work with iframe
class Vote(View):

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, pk):
        user = Guest.objects.get(id=request.user.id)
        model = request.POST['element']
        instance = get_instance(model, pk)

        action = request.POST['action']
        update_instance_rating(instance, user, action)  # This might lead to duplicated requests
        return render(request, 'empty.html')


def handler404(request, exception=None): return render(request, 'errors/404page.html')


def handler400(request, exception=None): return render(request, 'errors/400page.html')


def handler403(request, exception=None): return render(request, 'errors/403page.html')


def handler500(request, exception=None): return render(request, 'errors/500page.html')

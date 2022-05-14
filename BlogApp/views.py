from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from api.utils import update_instance_rating, toggle_save_instance, get_comments_with_replies
from .decorators import user_owns_the_post
from .forms import *


class Index(View):
    def get(self, request):
        return HttpResponseRedirect('/about/')


class About(View):
    def get(self, request):
        context = {'user': request.user}

        return render(request, 'new-layout/about.html', context)


class Home(View):
    def get(self, request):
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
        
        return render(request, 'new-layout/blog/home.html', context)

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, ):
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = Guest.objects.get(name=request.user)
            form.save()
            return redirect('blog:home')

        form = PostForm
        posts = Post.objects.all().order_by('-creation_date')
        context = {'posts': posts, 'user': request.user}

        return render(request, 'new-layout/blog/home.html', context)


class HomeByRating(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-number_of_comments')
        context = {'posts': posts, 'user': request.user}
        return render(request, 'new-layout/blog/home.html', context)


class PostPage(View):
    def get(self, request, pk, save=False, vote=None):
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
            return render(request, 'new-layout/blog/postpage.html', context)
        saved_by_users = post.saved_by.all()
        context |= {'user': user, 'saved_by': saved_by_users}

        if save is True:  # TODO kwargs are not sent here
            toggle_save_instance(post, user)
        elif vote:
            response = update_instance_rating(post, user, vote)
            if response.status_code != 200:
                return render(request, '403page.html')

        return render(request, 'new-layout/blog/postpage.html', context)


class CreatePost(View):
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
        context = {'form': form, 'post': post}

        template = 'new-layout/blog/post-edit.html'
        return render(request, template, context)

    @method_decorator(decorators)
    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('blog:home')

        context = {'form': form, 'post': post}

        return render(request, 'new-layout/blog/post-edit.html', context)


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
            user = Guest.objects.get(name=request.user)
            form.instance.user = user
            form.instance.post = post
            post.number_of_comments = Comment.objects.filter(post=post).count() + 1
            form.save()
            post.save()

            return HttpResponseRedirect(reverse('blog:post', args=(post.id,)))
        form = CommentForm

        context = {'form': form}
        return render(request, 'blog/create_comment.html', context)


class Reply(View):

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, post_pk, comment):
        form = CommentForm(request.POST)

        if form.is_valid():
            post = Post.objects.get(id=post_pk)
            parent_comment = Comment.objects.get(id=comment)
            user = Guest.objects.get(name=request.user)
            form.instance.user = user
            form.instance.post = post
            new_comment = form.save()
            parent_comment.replies.add(new_comment)
            post.number_of_comments = Comment.objects.filter(post=post).count() + 1

            return HttpResponseRedirect(reverse('blog:post', args=(post.id,)))
        form = CommentForm

        context = {'form': form}
        return render(request, 'blog/reply.html', context)


def handler404(request, exception=None): return render(request, '404page.html')


def handler400(request, exception=None): return render(request, '400page.html')


def handler403(request, exception=None): return render(request, '403page.html')


def handler500(request, exception=None): return render(request, '500page.html')

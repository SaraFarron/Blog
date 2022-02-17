from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from api.utils import update_instance_rating, toggle_save_instance, get_comments_with_replies
from .decorators import user_owns_the_post
from .forms import *

newlo = True

class TestPage(View):
    def get(self, request):
        return render(request, 'new-layout/test.html', { })

class Index(View):
    def get(self, request):
        if 'user_loc' in request.COOKIES:
            loc = request.COOKIES['user_loc']
        else:
            loc = request.LANGUAGE_CODE
        return HttpResponseRedirect('/' + loc + '/about/')


class About(View):
    def get(self, request):
        browser_locale = request.LANGUAGE_CODE  # return browser language code (ru/en/etc)
        context = {'user': request.user}
        response = render(request, 'index.html' if not newlo else 'new-layout/about.hmtl', context)
        response.set_cookie('user_loc', browser_locale)
        return response


class Home(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-id')
        context = {'posts': posts, 'user': request.user}
        return render(request, 'home.html' if not newlo else 'new-layout/blog/home.html', context)

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, ):
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = Guest.objects.get(name=request.user)
            form.save()
            return redirect('blog:home')

        form = PostForm
        posts = Post.objects.all().order_by('-rating')
        context = {'posts': posts, 'user': request.user}
        return render(request, 'new-layout/blog/home.html', context)


class HomeByRating(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-creation_date')
        context = {'posts': posts, 'user': request.user}
        return render(request, 'home.html', context)


class SavedContents(View):
    def get(self, request):
        user = Guest.objects.get(user=request.user)
        saved_posts = Post.objects.filter(saved_by=user)
        saved_comments = Comment.objects.filter(saved_by=user)
        context = {'posts': saved_posts, 'comments': saved_comments}
        return render(request, 'blog/saved.html', context)


class PostPage(View):
    def get(self, request, pk, save=False, vote=None):
        post = Post.objects.get(id=pk)
        comments = get_comments_with_replies(post)
        context = {'post': post, 'comments': comments}

        try:  # Occurs if user is not authorised
            user = Guest.objects.get(user=request.user)
        except TypeError:
            return render(request, 'blog/post.html', context)
        saved_by_users = post.saved_by.all()
        context |= {'user': user, 'saved_by': saved_by_users}

        if save is True:  # TODO kwargs are not sent here
            toggle_save_instance(post, user)
        elif vote:
            response = update_instance_rating(post, user, vote)
            if response.status_code != 200:
                return render(request, '403page.html')

        return render(request, 'blog/post.html', context)


class CreatePost(View):
    @method_decorator(login_required(login_url='user:login'))  # method_decorator is needed for correct work
    def get(self, request, ):
        user = Guest.objects.get(name=request.user.username)
        if user.is_banned:
            return render(request, '403page.html')
        form = PostForm #думаю, лучше верстать форму самостоятельно

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
        return render(request, 'blog/update_post.html', context)

    @method_decorator(decorators)
    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('blog:home')

        context = {'form': form}
        return render(request, 'blog/update_post.html', context)


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
            user = Guest.objects.get(name=request.user)
            form.instance.user = user
            form.instance.post = post
            post.number_of_comments = len(Comment.objects.filter(post=post))
            form.save()
            post.save()

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
            user = Guest.objects.get(name=request.user)
            form.instance.user = user
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

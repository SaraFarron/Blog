from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from api.utils import get_comments_with_replies, update_instance_rating
from .utils import new_comment, get_instance
from .decorators import user_owns_instance
from .forms import *


class Index(View):
    def get(self, request):
        return HttpResponseRedirect(reverse('blog:about'))


class About(View):
    def get(self, request):
        context = {'user': request.user}
        return render(request, 'blog/about.html', context)


class Home(View):
    def get(self, request, sort=None, filter=None):
        request_guest = None
        if request.user.is_authenticated:
            request_guest = Guest.objects.get(id=request.user.id)
        elif filter:
            return render(request, 'errors/user_not_logged_in.html')

        if request_guest:
            match filter:
                case 'bookmarked':
                    posts = request_guest.post_saved_by
                case 'liked':
                    posts = request_guest.upvoted_post_users
                case 'disliked':
                    posts = request_guest.downvoted_post_users
                case None:
                    posts = Post.objects
                case _:
                    return render(request, 'errors/404page.html')
        else:
            posts = Post.objects

        posts = posts.prefetch_related(
            'user',
            'saved_by',
            'upvoted_users',
            'downvoted_users'
        )

        if sort is None:
            sort = 'by_' +(request.COOKIES['sorting'] if 'sorting' in request.COOKIES else 'novelty')

        match sort:
            case 'by_novelty':
                posts = posts.order_by('-creation_date')
            case 'by_popularity':
                posts = posts.order_by('-number_of_comments')
            case 'by_rating':
                posts = posts.order_by('-rating')
            case _:
                return render(request, 'errors/404page.html')

        context = {
            'posts': posts,
            'user': request.user,
            'sorting': sort[3:],
            'sort': sort,
            'filter': filter,
            'request_guest': request_guest
        }
        return render(request, 'blog/home.html', context)

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


class UpdateObject(View):
    decorators = [login_required(login_url='user:login'), user_owns_instance]

    @method_decorator(decorators)
    def post(self, request, pk):
        model = request.POST['element']
        instance, form = get_instance(model, pk, request.POST)

        if form.is_valid():
            form.save()
            return redirect(request.META['HTTP_REFERER'])

        #errors handling?
        return redirect(request.META['HTTP_REFERER'])


class DeleteObject(View):
    decorators = [login_required(login_url='user:login'), user_owns_instance]

    @method_decorator(decorators)
    def post(self, request, pk):
        model = request.POST['element']
        instance, _ = get_instance(model, pk)
        instance.delete()

        return redirect(reverse('blog:home')) if model == 'post' else redirect(request.META['HTTP_REFERER'])


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


# Supposed to work with iframe
class Save(View):

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, pk):
        user = Guest.objects.get(id=request.user.id)
        model = request.POST['element']
        instance, _ = get_instance(model, pk)

        if user in instance.saved_by.all():
            instance.saved_by.remove(user)
        else:
            instance.saved_by.add(user)

        instance.save()
        return render(request, 'empty.html')


# Supposed to work with iframe
class Vote(View):

    @method_decorator(login_required(login_url='user:login'))
    def post(self, request, pk):
        user = Guest.objects.get(id=request.user.id)
        model = request.POST['element']
        instance, _ = get_instance(model, pk)

        action = request.POST['action']
        update_instance_rating(instance, user, action)  # This might lead to duplicated requests
        return render(request, 'empty.html')


def handler404(request, exception=None): return render(request, 'errors/404page.html')


def handler400(request, exception=None): return render(request, 'errors/400page.html')


def handler403(request, exception=None): return render(request, 'errors/403page.html')


def handler500(request, exception=None): return render(request, 'errors/500page.html')

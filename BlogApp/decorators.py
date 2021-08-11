from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from .models import Post


def unauthenticated_user(view_func):

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def user_owns_the_post(view_func):

    def wrapper_func(request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        if str(request.user) == str(post.user):
            return view_func(request, pk, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('blog:home'))

    return wrapper_func

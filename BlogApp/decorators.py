from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from .utils import get_instance


def unauthenticated_user(view_func):

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def user_owns_instance(view_func):

    def wrapper_func(request, pk, *args, **kwargs):
        model = request.POST['element']
        instance, _ = get_instance(model, pk)
        if str(request.user) == str(instance.user):
            return view_func(request, pk, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('blog:home'))

    return wrapper_func

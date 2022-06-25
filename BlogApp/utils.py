from .models import Comment, Post
from .forms import PostForm, CommentForm
from user.models import Guest


def new_comment(request, form, post):
    user = Guest.objects.get(name=request.user)
    form.instance.user = user
    form.instance.post = post
    form.instance.owner_id = user.id
    form.instance.owner_name = user.name
    form.instance.owner_is_moderator = user.is_moderator
    form.instance.owner_pfp_url = user.profile_picture.url
    post.number_of_comments = Comment.objects.filter(post=post).count() + 1
    comment = form.save()
    post.save()
    return comment


def get_instance(model, pk):
    """
        Returns model and form
    """
    match model:
        case 'post':
            instance = Post.objects.get(pk=pk)
            form = PostForm(instance=instance)
        case 'comment':
            instance = Comment.objects.get(pk=pk)
            form = CommentForm(instance=instance)
        case _:
            raise model + " - wrong type"

    return instance, form

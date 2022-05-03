from BlogApp.models import Comment, Post
from user.models import Guest
from django.contrib.auth.models import User
from user.utils import create_token
from uuid import uuid4
from django.db.utils import IntegrityError


LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut laore et " \
              "dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut " \
              "aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cilum " \
              "dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui " \
              "officia deserunt mollit anim id est laborum. "
LOREM_IPSUM_LONG = "Sed ut perspiciatis, unde omnis iste natus error sit voluptatem accusantium doloremque " \
                   "laudantium, totam rem aperiam eaque ipsa, quae ab illo inventore veritatis et quasi architecto " \
                   "beatae vitae dicta sunt, explicabo. Nemo enim ipsam voluptatem, quia voluptas sit, asprnatur aut " \
                   "odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione voluptatem sequi nesciunt, " \
                   "neque porro quisquam est, qui dolorem ipsum, quia dolor sit, amet, consectetur, adipisci velit, " \
                   "sed quia non numquam eius modi tempora incidunt, ut labore et dolore magnam aliquam quaerat " \
                   "voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit " \
                   "laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit, " \
                   "qui in ea voluptate velit esse, quam nihil molestiae consequatur, vel illum, qui dolorem eum " \
                   "fugiat, quo voluptas nulla pariatur? At vero eos et accusamus et iusto odio dignissimos ducimus, " \
                   "qui blanditiis praesentium voluptatum deleniti atque corrupti, quos dolores et quas molestias " \
                   "excepturi sint, obcaecati cupiditate non provident, similique sunt in culpa, qui officia deerunt " \
                   "mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita " \
                   "distinctio. Nam libero tempore, cum soluta nobis est eligendi optio, cumque nihil impedit, " \
                   "quo minus id, quod maxime placeat, facere possimus, omnis voluptas assumenda est, omnis dolor " \
                   "repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe " \
                   "eveniet, ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic " \
                   "tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut " \
                   "perferendis doloribus asperiores repellat. "


def populate_users(n: int) -> None:
    for i in range(n):
        username = uuid4().hex[:5]
        try:
            user = User.objects.create(
                    username=username,
                    password=uuid4().hex,
                    email=f'{username}@gmail.com'
                )
            user.save()
        except IntegrityError:
            print('User already exists')
            continue
        token = create_token(user)
        guest = Guest.objects.create(
                user=user,
                name=username,
                token=token.key,
                email=f'{username}@gmail.com'
            )
        guest.save()


def populate_posts(n: int) -> None:
    user = Guest.objects.all().first()
    for i in range(n):
        post = Post.objects.create(
            user=user,
            name=f'TestUser{i} TestPost',
            description=LOREM_IPSUM,
            text=LOREM_IPSUM_LONG
        )
        post.save()


def populate_comments(n: int) -> None:
    user = Guest.objects.all().first()
    post = Post.objects.all().first()
    for i in range(n):
        comment = Comment.objects.create(
            user=user,
            post=post,
            text=LOREM_IPSUM
        )
        post.number_of_comments = Comment.objects.filter(post=post).count() + 1
        comment.save()

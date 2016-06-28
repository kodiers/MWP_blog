from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse

from .helpers import ajax_required

from .forms import UserRegistrationForm, CommentForm, PostForm

from .models import Post

# Create your views here.


def register(request):
    """
    Registration view. Show registration form and register user.
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/registration_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


def index(request):
    """
    Main page. Show blogs sorted by votes(rating) count. Paginate by 5.
    """
    # compute last week
    last_week = timezone.now() - timezone.timedelta(7)
    # get post with most votes
    posts = Post.objects.filter(created__gte=last_week).annotate(count=Count('users_votes')).order_by('-count')
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', {'posts': posts})


def user_page(request, username):
    """
    Show users records
    """
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    return render(request, 'blog/user_page.html', {'user': user, 'posts': posts})


def post_detail(request, post):
    """
    Show post info. Show comments form and add comments.
    """
    post = get_object_or_404(Post, slug=post)
    comments = post.comments.all()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, "blog/detail.html",
                      {'post': post, 'comments': comments, 'comment_form': comment_form, 'new_comment': new_comment})


@login_required
def post_create(request, post=None):
    """
    Create or edit post
    """
    if post:
        post = get_object_or_404(Post, slug=post)
        if post.author != request.user:
            return HttpResponseForbidden()
    else:
        post = Post(author=request.user)
    post_form = PostForm(request.POST or None, instance=post)
    if request.POST:
        if post_form.is_valid():
            post_form.save()
            return redirect(reverse('blog:post_detail', args=[post.slug]))
    return render(request, 'blog/add.html', {'post_form': post_form, 'post': post})



@ajax_required
@login_required
@require_POST
def post_vote(request):
    """
    Add vote to post
    """
    post_id = request.POST['id']
    action = request.POST['action']
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            # Check if user isn't owner of post
            if post.author != request.user:
                if action == 'vote':
                    post.users_votes.add(request.user)
                else:
                    post.users_votes.remove(request.user)
                return JsonResponse({'status': 'ok'})
        except Exception:
            pass
    return JsonResponse({'status': 'error'})
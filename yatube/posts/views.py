from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post, Group, User


max_posts = 10


def paginator_func(request, post_list, max_posts=max_posts):
    paginator = Paginator(post_list, max_posts)
    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')
    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    post_list = Post.objects.all()

    context = {'page_obj': paginator_func(request, post_list), }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.post_group.all()

    context = {
        'group': group,
        'page_obj': paginator_func(request, post_list),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.post_author.all()

    context = {
        'author': author,
        'page_obj': paginator_func(request, post_list),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    posts = Post.objects.filter(author=post.author)
    context = {
        'post': post,
        'posts': posts,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form, })
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', request.user)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        form = PostForm(request.POST or None, instance=post)
        if not form.is_valid():
            return render(request,
                          'posts/create_post.html',
                          {'form': form,
                           'post': post,
                           })
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:post_detail', post_id=post.id)
    return redirect('posts:post_detail', post.pk)

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post, Group, User


max_posts = 10


def index(request):
    post_list = Post.objects.order_by('-pub_date')
    paginator = Paginator(post_list, max_posts)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.post_group.filter(
        group=group
    ).order_by('-pub_date')

    paginator = Paginator(post_list, max_posts)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.post_author.filter(author=author).order_by('-pub_date')

    paginator = Paginator(post_list, max_posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_lenght = Post.objects.filter(author=post.author).count()
    context = {
        'post': post,
        'post_lenght': post_lenght,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request,
                      'posts/create_post.html',
                      {'form': form,
                       'card_header': 'Добавить запись',
                       'button_text': 'Добавить',
                       })
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
                           'card_header': 'Редактировать запись',
                           'button_text': 'Сохранить'
                           })
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:post_detail', post_id=post.id)
    else:
        return redirect('posts:post_detail', post.pk)

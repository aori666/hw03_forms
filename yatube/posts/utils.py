from django.core.paginator import Paginator
from yatube.settings import max_posts


def paginator_func(request, post_list, max_posts=max_posts):
    paginator = Paginator(post_list, max_posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

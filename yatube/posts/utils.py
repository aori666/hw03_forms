from django.core.paginator import Paginator
from yatube.settings import MAX_POSTS


def paginator_func(request, post_list, max_posts=MAX_POSTS):
    paginator = Paginator(post_list, max_posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

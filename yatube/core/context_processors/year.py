from django.utils import timezone


def year(request):
    """Выводит текущий год."""
    return {
        'year': timezone.now().year
    }

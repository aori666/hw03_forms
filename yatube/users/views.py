from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    # Функция reverse_lazy позволяет получить URL по параметрам функции path()
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'

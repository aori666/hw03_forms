from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        labels = {'text': 'Сообщение поста', 'group': 'Группа'}
        help_texts = {'text': 'Введите текст', 'group': 'Выберите группу'}
        fields = {'text', 'group'}

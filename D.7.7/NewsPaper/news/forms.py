from django import forms
from .models import Post
from .models import User
from django_filters import ModelChoiceFilter

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        #fields = '__all__'

        #fields = ['title', 'type_post', 'text_post', 'authors_id']
        fields = ['title', 'text_post', 'authors_id']

        labels = {'title': 'Заголовок', 'text_post': 'Текст', 'authors_id': 'Фамилия автора'}
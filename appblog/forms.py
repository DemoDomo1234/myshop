from django import forms
from .models import MyBlog
from taggit.forms import TagField

class CreateForm(forms.ModelForm):
    tags = TagField()
    class Meta:
        model = MyBlog
        fields = ('titel', 'body', 'image', 'image' , 'film' , 'category' , 'music')

class SearchForm(forms.Form):
    search = forms.CharField()
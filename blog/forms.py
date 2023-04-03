from django import forms
from .models import Blog
from taggit.forms import TagField


class CreateForm(forms.ModelForm):
    tags = TagField()
    class Meta:
        model = Blog
        fields = ('titel', 'body', 'image',
                    'film', 'category', 'music', 'tags')
        
    def clean(self):
 
        super().clean()
         
        titel = self.cleaned_data.get('titel')
        body = self.cleaned_data.get('body')
 
        if len(titel) < 5 :
            self._errors['titel'] = self.error_class([
                'titel minimum 5 characters required'])

        if len(body) < 5 :
            self._errors['body'] = self.error_class([
                'body minimum 5 characters required'])
            
        if "<script>" in body :
            self._errors['body'] = self.error_class([
                'you cant script'])
 
        return self.cleaned_data


class SearchForm(forms.Form):
    search = forms.CharField()
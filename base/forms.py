from django import forms
from .models import Category


class ListForm(forms.Form):
    titel = forms.CharField(max_length=50)
    body = forms.CharField(widget=forms.Textarea)

    def clean(self):

        titel = self.cleaned_data.get('titel')
        body = self.cleaned_data.get('body')

        if len(titel) < 3 :
            self._errors['titel'] = self.error_class([
                'titel minimum 3 characters required'])

        if len(body) < 3 :
            self._errors['body'] = self.error_class([
                'body minimum 3 characters required'])

        return self.cleaned_data


class lists(forms.Form):
    titel = forms.CharField(max_length=50)



class ImageForm(forms.Form):
    image = forms.ImageField()


class CreateCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['titel', 'more']


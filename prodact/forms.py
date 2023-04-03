from django import forms
from taggit.forms import TagField
from mdeditor.fields import MDTextFormField


class CreateForm(forms.Form): 
    titel = forms.CharField(max_length=100)
    body = MDTextFormField()
    image = forms.ImageField()
    weigth = forms.IntegerField(min_value=0)
    size = forms.IntegerField(min_value=0)
    garanty = MDTextFormField()
    tags = TagField()

    def clean(self):

        titel = self.cleaned_data.get('titel')
        body = self.cleaned_data.get('body')
        garanty = self.cleaned_data.get('garanty')

        if len(titel) < 3 :
            self._errors['titel'] = self.error_class([
                'titel minimum 3 characters required'])
            
        if len(body) < 10 :
            self._errors['body'] = self.error_class([
                'body minimum 10 characters required'])
            
        if "<script>" in body :
            self._errors['body'] = self.error_class([
                'you cant script'])

        if "<script>" in garanty :
            self._errors['garanty'] = self.error_class([
                'you cant script'])

        return self.cleaned_data


class UpdateForm(forms.Form):
    titel = forms.CharField(max_length=100)
    body = MDTextFormField()
    image = forms.ImageField()
    garanty = MDTextFormField()
    tags = TagField()

    def clean(self):

        titel = self.cleaned_data.get('titel')
        body = self.cleaned_data.get('body')
        garanty = self.cleaned_data.get('garanty')


        if len(titel) < 3 :
            self._errors['titel'] = self.error_class([
                'titel minimum 3 characters required'])
            
        if len(body) < 10 :
            self._errors['body'] = self.error_class([
                'body minimum 10 characters required'])
            
        if "<script>" in body :
            self._errors['body'] = self.error_class([
                'you cant script'])
            
        if "<script>" in garanty :
            self._errors['garanty'] = self.error_class([
                'you cant script'])

        return self.cleaned_data


class SendEmail(forms.Form):
    name = forms.CharField(max_length=20)
    massage = forms.CharField(max_length=20)
    subject = forms.CharField(max_length=20)
    email = forms.EmailField(required=True)


class Share(forms.Form):
    email = forms.EmailField()


class Num(forms.Form):
    num = forms.IntegerField(min_value= 1)


class SearchForm(forms.Form):
    search = forms.CharField()


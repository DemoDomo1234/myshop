from django import forms
from .models import Category
from taggit.forms import TagField
from mdeditor.fields import MDTextFormField

class CreateForm(forms.Form): 
    titel = forms.CharField(max_length=100)
    body = MDTextFormField()
    image = forms.ImageField()
    price = forms.IntegerField(min_value= 0)
    weigth = forms.IntegerField(min_value= 0)
    size = forms.IntegerField(min_value= 0)
    discount = forms.IntegerField(min_value= 0 , max_value = 100)
    number = forms.IntegerField(min_value= 0)
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
        if len(garanty) < 10 :
            self._errors['garanty'] = self.error_class([
                'garanty minimum 10 characters required'])

        return self.cleaned_data

class UpdateForm(forms.Form):
    titel = forms.CharField(max_length=100)
    body = MDTextFormField()
    image = forms.ImageField()
    price = forms.IntegerField(min_value= 0)
    discount = forms.IntegerField(min_value= 0 , max_value = 100)
    number = forms.IntegerField(min_value= 0)
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
        if len(garanty) < 10 :
            self._errors['garanty'] = self.error_class([
                'garanty minimum 10 characters required'])

        return self.cleaned_data

class SendEmail(forms.Form):
    name = forms.CharField(max_length=20)
    massage = forms.CharField(max_length=20)
    subject = forms.CharField(max_length=20)
    email = forms.EmailField(required=True)

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
    
class Share(forms.Form):
    email = forms.EmailField()

class Num(forms.Form):
    num = forms.IntegerField(min_value= 1)

class AddressForm(forms.Form):
    name = forms.CharField(max_length=50)
    floor = forms.CharField(max_length=2)
    plaque = forms.CharField(max_length=5)
    number = forms.CharField(max_length=11)

    def clean(self):

        floor = self.cleaned_data.get('floor')
        number = self.cleaned_data.get('number')
        plaque = self.cleaned_data.get('plaque')
        name = self.cleaned_data.get('name')

        if len(name) < 5 :
            self._errors['name'] = self.error_class([
                'name minimum 5 characters required'])

        if len(number) < 11 :
            self._errors['number'] = self.error_class([
                'number minimum 11 characters required'])
        if number.isdigit() == False :
            self._errors['number'] = self.error_class([
                'number just number'])

        if len(floor) < 2 :
            self._errors['floor'] = self.error_class([
                'floor minimum 2 characters required'])
        if floor.isdigit() == False :
            self._errors['floor'] = self.error_class([
                'floor just number'])

        if len(plaque) < 1 :
            self._errors['plaque'] = self.error_class([
                'plaque minimum 1 characters required'])
        if plaque.isdigit() == False :
            self._errors['plaque'] = self.error_class([
                'plaque just number'])

        return self.cleaned_data

class UpdateAddressForm(forms.Form):
    name = forms.CharField(max_length=50)
    floor = forms.CharField(max_length=2)
    plaque = forms.CharField(max_length=5)
    number = forms.CharField(max_length=11)

    def clean(self):

        floor = self.cleaned_data.get('floor')
        number = self.cleaned_data.get('number')
        plaque = self.cleaned_data.get('plaque')
        name = self.cleaned_data.get('name')



        if len(number) < 11 :
            self._errors['number'] = self.error_class([
                'number minimum 11 characters required'])
        if number.isdigit() == False :
            self._errors['number'] = self.error_class([
                'number just number'])

        if len(floor) < 2 :
            self._errors['floor'] = self.error_class([
                'floor minimum 2 characters required'])
        if floor.isdigit() == False :
            self._errors['floor'] = self.error_class([
                'floor just number'])

        if len(plaque) < 5 :
            self._errors['plaque'] = self.error_class([
                'plaque minimum 5 characters required'])
        if plaque.isdigit() == False :
            self._errors['plaque'] = self.error_class([
                'plaque just number'])

        if len(name) < 5 :
            self._errors['name'] = self.error_class([
                'name minimum 5 characters required'])

        return self.cleaned_data

class SearchForm(forms.Form):
    search = forms.CharField()

class ImageForm(forms.Form):
    image = forms.ImageField()

class CreateCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['titel' , 'more']

class Sellers(forms.Form):
    price = forms.IntegerField(min_value= 0)
    discount = forms.IntegerField(min_value= 0 , max_value = 100)
    number = forms.IntegerField(min_value= 0)
    garanty = MDTextFormField()

class ColorNumForm(forms.Form):
    color = forms.CharField(max_length=100)
    num = forms.IntegerField(min_value= 1)
    size = forms.IntegerField(min_value= 1)

    def clean(self):
 
        super(ColorNumForm, self).clean()
         
        color = self.cleaned_data.get('color')

        if len(color) < 2 :
            self._errors['color'] = self.error_class([
                'color minimum 2 characters required'])

        if color.isalpha() == False :
            self._errors['color'] = self.error_class([
                'color just charecter'])
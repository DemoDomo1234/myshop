from django import forms
from .models import Category

class CreateForm(forms.Form):
    titel = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea())
    image = forms.ImageField()
    price = forms.IntegerField(min_value= 0)
    discount = forms.IntegerField(min_value= 0 , max_value = 100)
    number = forms.IntegerField(min_value= 0)

class UpdateForm(forms.Form):
    titel = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
    price = forms.IntegerField(min_value= 0)
    discount = forms.IntegerField(min_value= 0 , max_value = 100)
    number = forms.IntegerField(min_value= 0)

class SendEmail(forms.Form):
    name = forms.CharField(max_length=20)
    massage = forms.CharField(max_length=20)
    subject = forms.CharField(max_length=20)
    email = forms.EmailField(required=True)

class ListForm(forms.Form):
    titel = forms.CharField(max_length=10)
    body = forms.CharField(widget=forms.Textarea)

class lists(forms.Form):
    titel = forms.CharField(max_length=10)

class Share(forms.Form):
    email = forms.EmailField()

class Num(forms.Form):
    num = forms.IntegerField(min_value= 1)

class AddressForm(forms.Form):
    name = forms.CharField(max_length=50)
    floor = forms.CharField(max_length=2)
    plaque = forms.CharField(max_length=5)
    number = forms.CharField(max_length=11)

class UpdateAddressForm(forms.Form):
    floor = forms.CharField(max_length=20)
    plaque = forms.CharField(max_length=5)

class SearchForm(forms.Form):
    search = forms.CharField()

class ImageForm(forms.Form):
    image = forms.ImageField()

class CreateCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['titel' , 'more']

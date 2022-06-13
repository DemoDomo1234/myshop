from django import forms

class SingupForm(forms.Form):
    username = forms.CharField(max_length=20)
    name = forms.CharField(max_length=20)
    familie = forms.CharField(max_length=20)
    email = forms.EmailField()
    number = forms.CharField(max_length=11)
    password = forms.CharField(widget= forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ChangepassForm(forms.Form):
    password1 = forms.CharField(widget= forms.PasswordInput)
    password2 = forms.CharField(widget= forms.PasswordInput)

class UpdateForm(forms.Form):
    username = forms.CharField(max_length=20)
    name = forms.CharField(max_length=20)
    familie = forms.CharField(max_length=20)
    email = forms.EmailField()
    number = forms.CharField(max_length=11)
    password1 = forms.CharField(widget= forms.PasswordInput)
    password2 = forms.CharField(widget= forms.PasswordInput)
    password3 = forms.CharField(widget= forms.PasswordInput)
       
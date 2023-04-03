from django import forms
from .models import User
from django.contrib.auth import authenticate


class SingupForm(forms.Form):
    choices = (
        ('m', 'man'),
        ('w', 'wonamn'),
    )
    username = forms.CharField(max_length=20)
    name = forms.CharField(max_length=20)
    familie = forms.CharField(max_length=20)
    email = forms.EmailField()
    number = forms.CharField(max_length=11)
    password = forms.CharField(widget= forms.PasswordInput)
    gender = forms.CharField(max_length=200, widget=forms.Select(choices=choices))
    date_of_birth = forms.DateField()
    national_code = forms.CharField(max_length=10)
    
    def clean(self):
 
        super().clean()
         
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        number = self.cleaned_data.get('number')
        name = self.cleaned_data.get('name')
        familie = self.cleaned_data.get('familie')
        national_code = self.cleaned_data.get('national_code')

        if len(username) < 4 :
            self._errors['username'] = self.error_class([
                'username minimum 5 characters required'])
            
        if len(name) < 5 :
            self._errors['name'] = self.error_class([
                'name minimum 5 characters required'])
            
        if len(familie) < 5 :
            self._errors['familie'] = self.error_class([
                'familie minimum 5 characters required'])
            
        is_str = False
        for x in password :
            if x.isalpha() :
                is_str = True
                  
        if is_str == False :
            self._errors['password'] = self.error_class([
                'The password must contain letters, numbers and capital letters'])
            
        is_num = False
        for x in password :
            if x.isdigit() :
                is_num = True
                  
        if is_num == False :
            self._errors['password'] = self.error_class([
                'The password must contain letters, numbers and capital letters'])
            
        if len(password) < 8 :
            self._errors['password'] = self.error_class([
                'Password Should Contain a minimum of 8 characters'])
            
        if len(number) < 11 :
            self._errors['number'] = self.error_class([
                'number Should Contain a minimum of 11 characters'])
            
        if number.isdigit() == False :
            self._errors['number'] = self.error_class([
                'number just number'])

        if len(national_code) < 10 :
            self._errors['national_code'] = self.error_class([
                'national_code Should Contain a minimum of 10 characters'])
            
        if national_code.isdigit() == False :
            self._errors['national_code'] = self.error_class([
                'national_code just number'])
            
        if name.isalpha() == False :
            self._errors['name'] = self.error_class([
                'name just str'])
            
        if familie.isalpha() == False :
            self._errors['familie'] = self.error_class([
                'familie just str'])

        is_username = False
        try :
            myusername = User.objects.get(username = username)
        except :
            is_username = True

        if is_username == False :
            self._errors['username'] = self.error_class([
                'username it was'])
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        # get request from view
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
    def clean(self):
 
        super().clean()
         
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        is_username = True
        try :
            myusername = User.objects.get(username = username)
        except :
            is_username = False
            
        user = authenticate(self.request, username=username, password=password)
        
        if is_username == False :
            self._errors['username'] = self.error_class([
                'username is not true'])
        elif user is None :
            self._errors['password'] = self.error_class([
                'password is not true'])

        return self.cleaned_data
 

class ChangepassForm(forms.Form):
    password_one = forms.CharField(widget=forms.PasswordInput)
    password_tow = forms.CharField(widget=forms.PasswordInput)   
    
    def clean(self):
 
        super().clean()
         
        password_one = self.cleaned_data.get('password_one')
        password_tow = self.cleaned_data.get('password_tow')

        is_str = False
        for x in password_one :
            if x.isalpha() :
                is_str = True
                  
        if is_str == False :
            self._errors['password_one'] = self.error_class([
                'The password must contain letters, numbers and capital letters'])

        is_num = False
        for x in password_one :
            if x.isdigit() :
                is_num = True
                  
        if is_num == False :
            self._errors['password_one'] = self.error_class([
                'The password must contain letters, numbers and capital letters'])
            
        if len(password_one) < 8 :
            self._errors['password_one'] = self.error_class([
                'Password Should Contain a minimum of 8 characters'])
            
        if password_one != password_tow :
            self._errors['password_one'] = self.error_class([
                'Password1 == password2'])
            
        return self.cleaned_data


class UpdateForm(forms.Form):
    username = forms.CharField(max_length=20)
    name = forms.CharField(max_length=20)
    familie = forms.CharField(max_length=20)
    email = forms.EmailField()
    number = forms.CharField(max_length=11)
    password = forms.CharField(widget= forms.PasswordInput)
    password_one = forms.CharField(widget= forms.PasswordInput)
    password_tow = forms.CharField(widget= forms.PasswordInput)
    gender = forms.BooleanField()
    date_of_birth = forms.DateField()
    national_code = forms.CharField(max_length=10)
    
    def __init__(self, *args, **kwargs):
        # get user from view
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        

    def clean(self):
 
        super().clean()
         
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        password_one = self.cleaned_data.get('password_one')
        password_tow = self.cleaned_data.get('password_tow')
        number = self.cleaned_data.get('number')
        national_code = self.cleaned_data.get('national_code')
        name = self.cleaned_data.get('name')
        familie = self.cleaned_data.get('familie')
        myuser = User.objects.get(id = self.user.id)

        if not myuser.check_password(password):
            self._errors['password'] = self.error_class([
                'password is not true'])

        if len(username) < 5 :
            self._errors['username'] = self.error_class([
                'username minimum 5 characters required'])
            
        if len(name) < 5 :
            self._errors['name'] = self.error_class([
                'name minimum 5 characters required'])
            
        if len(familie) < 5 :
            self._errors['familie'] = self.error_class([
                'familie minimum 5 characters required'])
            
        is_str = False
        for x in password_one :
            if x.isalpha() :
                is_str = True
                  
        if is_str == False :
            self._errors['password_one'] = self.error_class([
                'The password must contain letters, numbers and capital letters'])
            
        is_num = False
        for x in password_one :
            if x.isdigit() :
                is_num = True
                  
        if is_num == False :
            self._errors['password_one'] = self.error_class([
                'The password must contain letters, numbers and capital letters'])
            
        if len(password_one) < 8 :
            self._errors['password_one'] = self.error_class([
                'Password Should Contain a minimum of 8 characters'])
            
        if password_one != password_tow :
            self._errors['password_one'] = self.error_class([
                'Password1 == password2'])
            
        if len(number) < 11 :
            self._errors['number'] = self.error_class([
                'number Should Contain a minimum of 11 characters'])
            
        if number.isdigit() == False :
            self._errors['number'] = self.error_class([
                'number just number'])

        if len(national_code) < 10 :
            self._errors['national_code'] = self.error_class([
                'national_code Should Contain a minimum of 10 characters'])
            
        if national_code.isdigit() == False :
            self._errors['national_code'] = self.error_class([
                'national_code just number'])
            
        if name.isalpha() == False :
            self._errors['name'] = self.error_class([
                'name just str'])
            
        if familie.isalpha() == False :
            self._errors['familie'] = self.error_class([
                'familie just str'])
 
        return self.cleaned_data


from django import forms
from .models import User
from django.contrib.auth import authenticate

class SingupForm(forms.Form):
    choices = (
        ('m' , 'man'),
        ('w' , 'wonamn'),
    )
    username = forms.CharField(max_length=20)
    name = forms.CharField(max_length=20)
    familie = forms.CharField(max_length=20)
    email = forms.EmailField()
    number = forms.CharField(max_length=11)
    password = forms.CharField(widget= forms.PasswordInput)
    gender = forms.CharField(max_length=200 , widget = forms.Select(choices=choices))
    date_of_birth = forms.DateField()
    national_code = forms.CharField(max_length=10)
    
    def clean(self):
 
        super(SingupForm, self).clean()
         
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        number = self.cleaned_data.get('number')
        name = self.cleaned_data.get('name')
        familie = self.cleaned_data.get('familie')
        national_code = self.cleaned_data.get('national_code')

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

        is_username = True
        try :
            myusername = User.objects.get(username = username)
        except :
            is_username = False
        if is_username == False :
            self._errors['username'] = self.error_class([
                'username it was'])
        return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)
        
    def clean(self):
 
        super(LoginForm, self).clean()
         
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        is_username = True
        try :
            myusername = User.objects.get(username = username)
        except :
            is_username = False
        user = authenticate(self.request , username = username , password = password)
        if is_username == False :
            self._errors['username'] = self.error_class([
                'username is not true'])
        elif user is None :
            self._errors['password'] = self.error_class([
                'password is not true'])

        return self.cleaned_data
 
class ChangepassForm(forms.Form):
    password_one = forms.CharField(widget= forms.PasswordInput)
    password_tow = forms.CharField(widget= forms.PasswordInput)   
    
    def clean(self):
 
        super(ChangepassForm, self).clean()
         
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
        self.user = kwargs.pop('user', None)
        super(UpdateForm, self).__init__(*args, **kwargs)
        

    def clean(self):
 
        super(UpdateForm, self).clean()
         
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
   
class CreateCompanySeller(forms.Form):
    choices = (
        ('d' , 'تجاری'),
        ('s' , 'قیر تجاری'),
        ('n' , 'شخصی'),
    )
    company_name = forms.CharField(max_length=200)
    company_type = forms.CharField(max_length=200 , widget = forms.Select(choices=choices))
    fixed_number = forms.CharField(max_length=11 )
    economic_code = forms.CharField(max_length=11)
    permission_to_sign = forms.CharField(max_length=11)

    def clean(self):
 
        super(CreateCompanySeller, self).clean()
         
        company_name = self.cleaned_data.get('company_name')
        fixed_number = self.cleaned_data.get('fixed_number')
        economic_code = self.cleaned_data.get('economic_code')
        permission_to_sign = self.cleaned_data.get('permission_to_sign')

        if company_name.isalpha() == False :
            self._errors['company_name'] = self.error_class([
                'company_name just str'])
        if len(company_name) < 5 :
            self._errors['company_name'] = self.error_class([
                'company_name minimum 5 characters required'])

        if len(fixed_number) < 11 :
            self._errors['fixed_number'] = self.error_class([
                'fixed_number minimum 11 characters required'])
        if len(economic_code) < 11 :
            self._errors['economic_code'] = self.error_class([
                'economic_code minimum 11 characters required'])
        if len(permission_to_sign) < 11 :
            self._errors['permission_to_sign'] = self.error_class([
                'permission_to_sign minimum 11 characters required'])
        if fixed_number.isdigit() == False :
            self._errors['fixed_number'] = self.error_class([
                'fixed_number just number'])
        if economic_code.isdigit() == False :
            self._errors['economic_code'] = self.error_class([
                'economic_code just number'])
        if permission_to_sign.isdigit() == False :
            self._errors['permission_to_sign'] = self.error_class([
                'permission_to_sign just number'])
 
 
        return self.cleaned_data

class CreateSellerAccount(forms.Form):
    choices = (
        ('1' , '1-10'),
        ('2' , '10-100'),
        ('3' , '100-1000'),
    )
    choice = (
        ('hko' , 'خوراکی'),
        ('kha' , 'خانگی'),
        ('b' , 'برقی'),
        ('e' , 'الکترونیکی'),
        ('gh' , 'قیره'),
    )
    shop_name = forms.CharField(max_length=200)
    shaba_number = forms.CharField(max_length=24)
    shop_number = forms.CharField(max_length=200 , widget = forms.Select(choices=choices))
    shop_type = forms.CharField(max_length=200 , widget = forms.Select(choices=choice))
    tax = forms.DateField()
    national_card = forms.ImageField()

    def clean(self):
 
        super(CreateSellerAccount, self).clean()
         
        shop_name = self.cleaned_data.get('shop_name')
        shaba_number = self.cleaned_data.get('shaba_number')

        if len(shop_name) < 5 :
            self._errors['shop_name'] = self.error_class([
                'shop_name minimum 5 characters required'])

        if shop_name.isalpha() == False :
            self._errors['shop_name'] = self.error_class([
                'shop_name just str'])

        if len(shaba_number) < 24 :
            self._errors['shaba_number'] = self.error_class([
                'shaba_number minimum 24 characters required'])
        if shaba_number.isdigit() == False :
            self._errors['shaba_number'] = self.error_class([
                'shaba_number just number'])

        return self.cleaned_data

class UpdateCompanySeller(forms.Form):
    choices = (
        ('d' , 'تجاری'),
        ('s' , 'قیر تجاری'),
        ('n' , 'شخصی'),
    )
    company_name = forms.CharField(max_length=200)
    company_type = forms.CharField(max_length=200 , widget = forms.Select(choices=choices))
    fixed_number = forms.CharField(max_length=11 )
    economic_code = forms.CharField(max_length=11)
    permission_to_sign = forms.CharField(max_length=11)

    def clean(self):
 
        super(UpdateCompanySeller, self).clean()
         
        company_name = self.cleaned_data.get('company_name')
        fixed_number = self.cleaned_data.get('fixed_number')
        economic_code = self.cleaned_data.get('economic_code')
        permission_to_sign = self.cleaned_data.get('permission_to_sign')

 
        if company_name.isalpha() == False :
            self._errors['company_name'] = self.error_class([
                'company_name just str'])

        if len(company_name) < 5 :
            self._errors['company_name'] = self.error_class([
                'company_name minimum 5 characters required'])

        if len(fixed_number) < 11 :
            self._errors['fixed_number'] = self.error_class([
                'fixed_number minimum 11 characters required'])
        if len(economic_code) < 11 :
            self._errors['economic_code'] = self.error_class([
                'economic_code minimum 11 characters required'])
        if len(permission_to_sign) < 11 :
            self._errors['permission_to_sign'] = self.error_class([
                'permission_to_sign minimum 11 characters required'])
        if fixed_number.isdigit() == False :
            self._errors['fixed_number'] = self.error_class([
                'fixed_number just number'])
        if economic_code.isdigit() == False :
            self._errors['economic_code'] = self.error_class([
                'economic_code just number'])
        if permission_to_sign.isdigit() == False :
            self._errors['permission_to_sign'] = self.error_class([
                'permission_to_sign just number'])
 
        return self.cleaned_data

class UpdateSellerAccount(forms.Form):
    choices = (
        ('1' , '1-10'),
        ('2' , '10-100'),
        ('3' , '100-1000'),
    )
    choice = (
        ('hko' , 'خوراکی'),
        ('kha' , 'خانگی'),
        ('b' , 'برقی'),
        ('e' , 'الکترونیکی'),
        ('gh' , 'قیره'),
    )
    shop_name = forms.CharField(max_length=200)
    shaba_number = forms.CharField(max_length=24)
    shop_number = forms.CharField(max_length=200 , widget = forms.Select(choices=choices))
    shop_type = forms.CharField(max_length=200 , widget = forms.Select(choices=choice))
    tax = forms.DateField()
    national_card = forms.ImageField()

    def clean(self):
 
        super(UpdateSellerAccount, self).clean()
         
        shop_name = self.cleaned_data.get('shop_name')
        shaba_number = self.cleaned_data.get('shaba_number')

        if len(shop_name) < 5 :
            self._errors['shop_name'] = self.error_class([
                'shop_name minimum 5 characters required'])
        if shop_name.isalpha() == False :
            self._errors['shop_name'] = self.error_class([
                'shop_name just str'])
                
        if len(shaba_number) < 24 :
            self._errors['shaba_number'] = self.error_class([
                'shaba_number minimum 24 characters required'])

        if shaba_number.isdigit() == False :
            self._errors['shaba_number'] = self.error_class([
                'shaba_number just number'])


        return self.cleaned_data

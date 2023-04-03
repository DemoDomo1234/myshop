from django import forms


class Sellers(forms.Form):
    price = forms.IntegerField(min_value=0)
    discount = forms.IntegerField(min_value=0, max_value=100)
    number = forms.IntegerField(min_value=0)


class ColorNumForm(forms.Form):
    color = forms.CharField(max_length=100, required=False)
    num = forms.IntegerField(min_value=1)
    size = forms.IntegerField(min_value=1, required=False)
    price = forms.IntegerField(min_value=0)
    
    def __init__(self, *args, **kwargs):
        self.blog = kwargs.pop('blog', None)
        super().__init__(*args, **kwargs)

    def clean(self):
 
        super().clean()
         
        color = self.cleaned_data.get('color')
        size = self.cleaned_data.get('size')

        if len(color) < 2 :
            self._errors['color'] = self.error_class([
                'color minimum 2 characters required'])

        if color.isalpha() == False :
            self._errors['color'] = self.error_class([
                'color just charecter'])
        is_color = True
        try :
            mycolor = Color.objects.get(color=color)
        except :
            is_color = False
        if is_color == False :
            self._errors['color'] = self.error_class([
                'color is not true'])
        if is_color and mycolor not in self.blog.color.all() :
            self._errors['color'] = self.error_class([
                'color not in blog color'])  
        is_size = True
        try :
            mysize = size.objects.get(size=size)
        except :
            is_size = False
        if is_size == False :
            self._errors['size'] = self.error_class([
                'size is not true'])
        if is_size and mysize not in self.blog.size.all() :
            self._errors['size'] = self.error_class([
                'size not in blog size']) 




class CreateCompanySeller(forms.Form):
    choices = (
        ('d', 'تجاری'),
        ('s', 'قیر تجاری'),
        ('n', 'شخصی'),
    )
    company_name = forms.CharField(max_length=200)
    company_type = forms.CharField(max_length=200, widget=forms.Select(choices=choices))
    fixed_number = forms.CharField(max_length=11 )
    economic_code = forms.CharField(max_length=11)
    permission_to_sign = forms.CharField(max_length=11)

    def clean(self):
 
        super().clean()
        
        company_name = self.cleaned_data.get('company_name')
        fixed_number = self.cleaned_data.get('fixed_number')
        economic_code = self.cleaned_data.get('economic_code')
        permission_to_sign = self.cleaned_data.get('permission_to_sign')

        if company_name.isalpha() == False:
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
        ('1', '1-10'),
        ('2', '10-100'),
        ('3', '100-1000'),
    )
    choice = (
        ('hko', 'خوراکی'),
        ('kha', 'خانگی'),
        ('b', 'برقی'),
        ('e', 'الکترونیکی'),
        ('gh', 'قیره'),
    )
    shop_name = forms.CharField(max_length=200)
    shaba_number = forms.CharField(max_length=24)
    shop_number = forms.CharField(max_length=200, widget=forms.Select(choices=choices))
    shop_type = forms.CharField(max_length=200, widget=forms.Select(choices=choice))
    tax = forms.DateField()
    national_card = forms.ImageField()

    def clean(self):
 
        super().clean()
         
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
        ('d', 'تجاری'),
        ('s', 'قیر تجاری'),
        ('n', 'شخصی'),
    )
    company_name = forms.CharField(max_length=200)
    company_type = forms.CharField(max_length=200, widget=forms.Select(choices=choices))
    fixed_number = forms.CharField(max_length=11 )
    economic_code = forms.CharField(max_length=11)
    permission_to_sign = forms.CharField(max_length=11)

    def clean(self):
 
        super().clean()
         
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
        ('1', '1-10'),
        ('2', '10-100'),
        ('3', '100-1000'),
    )
    choice = (
        ('hko', 'خوراکی'),
        ('kha', 'خانگی'),
        ('b', 'برقی'),
        ('e', 'الکترونیکی'),
        ('gh', 'قیره'),
    )
    shop_name = forms.CharField(max_length=200)
    shaba_number = forms.CharField(max_length=24)
    shop_number = forms.CharField(max_length=200, widget=forms.Select(choices=choices))
    shop_type = forms.CharField(max_length=200, widget=forms.Select(choices=choice))
    tax = forms.DateField()
    national_card = forms.ImageField()

    def clean(self):
 
        super().clean()
         
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

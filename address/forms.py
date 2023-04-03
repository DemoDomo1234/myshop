from django import forms



class AddressForm(forms.Form):
    name = forms.CharField(max_length=50)
    floor = forms.CharField(max_length=2)
    plaque = forms.CharField(max_length=5)
    number = forms.CharField(max_length=11)
    postal_code = forms.CharField(max_length=10)

    def clean(self):

        floor = self.cleaned_data.get('floor')
        number = self.cleaned_data.get('number')
        plaque = self.cleaned_data.get('plaque')
        name = self.cleaned_data.get('name')
        postal_code = self.cleaned_data.get('postal_code')

        if len(name) < 5 :
            self._errors['name'] = self.error_class([
                'name minimum 5 characters required'])
            
        if len(postal_code) < 10 :
            self._errors['postal_code'] = self.error_class([
                'postal_code minimum 10 characters required'])
            
        if postal_code.isdigit() == False :
            self._errors['postal_code'] = self.error_class([
                'postal_code just number'])
                
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
    postal_code = forms.CharField(max_length=10)

    def clean(self):

        floor = self.cleaned_data.get('floor')
        number = self.cleaned_data.get('number')
        plaque = self.cleaned_data.get('plaque')
        name = self.cleaned_data.get('name')
        postal_code = self.cleaned_data.get('postal_code')


        if len(postal_code) < 10 :
            self._errors['postal_code'] = self.error_class([
                'postal_code minimum 10 characters required'])
            
        if postal_code.isdigit() == False :
            self._errors['postal_code'] = self.error_class([
                'postal_code just number'])
            
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

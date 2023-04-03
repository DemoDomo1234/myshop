from django import forms


class ComentsForm(forms.Form):
    choices = (
        ('y', 'yes'),
        ('i', 'I do not know'),
        ('n', 'no'),
    )
    choice = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    sagestion = forms.CharField(max_length=50, widget=forms.Select(choices=choices))
    score = forms.CharField(max_length=50, widget=forms.Select(choices=choice))
    titel = forms.CharField(max_length=100 )
    body = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
    bad = forms.CharField(widget=forms.Textarea)
    good = forms.CharField(widget=forms.Textarea)

    def clean(self):
 
        super().clean()
         
        titel = self.cleaned_data.get('titel')
        body = self.cleaned_data.get('body')
        bad = self.cleaned_data.get('bad')
        good = self.cleaned_data.get('good')
 
        if len(titel) < 5 :
            self._errors['titel'] = self.error_class([
                'titel minimum 5 characters required'])

        if len(body) < 5 :
            self._errors['body'] = self.error_class([
                'body minimum 5 characters required'])

        if len(bad) < 5 :
            self._errors['bad'] = self.error_class([
                'bad minimum 5 characters required'])

        if len(good) < 5 :
            self._errors['good'] = self.error_class([
                'good minimum 5 characters required'])
 
 
        return self.cleaned_data

class UpdateComentsForm(forms.Form):
    choices = (
        ('y', 'yes'),
        ('i', 'I do not know'),
        ('n', 'no'),
    )
    choice = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    sagestion = forms.CharField(max_length=50, widget=forms.Select(choices=choices))
    score = forms.CharField(max_length=50, widget=forms.Select(choices=choice))
    titel = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
    bad = forms.CharField(widget=forms.Textarea)
    good = forms.CharField(widget=forms.Textarea)

    def clean(self):
 
        super().clean()
         
        titel = self.cleaned_data.get('titel')
        body = self.cleaned_data.get('body')
        bad = self.cleaned_data.get('bad')
        good = self.cleaned_data.get('good')
 
        if len(titel) < 5 :
            self._errors['titel'] = self.error_class([
                'titel minimum 5 characters required'])

        if len(body) < 5 :
            self._errors['body'] = self.error_class([
                'body minimum 5 characters required'])

        if len(bad) < 5 :
            self._errors['bad'] = self.error_class([
                'bad minimum 5 characters required'])

        if len(good) < 5 :
            self._errors['good'] = self.error_class([
                'good minimum 5 characters required'])
 
 
        return self.cleaned_data

class ComentsBlogForm(forms.Form):
    titel = forms.CharField(max_length=100 )
    body = forms.CharField(widget=forms.Textarea)

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
 
        return self.cleaned_data

class UpdateComentsBlogForm(forms.Form):
    titel = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)

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
 
        return self.cleaned_data

class CustionForm(forms.Form):
    custion_body = forms.CharField(widget=forms.Textarea)

    def clean(self):
 
        super().clean()
         
        custion_body = self.cleaned_data.get('custion_body')

        if len(custion_body) < 5 :
            self._errors['custion_body'] = self.error_class([
                'custion_body minimum 5 characters required'])

        return self.cleaned_data

class UpdateCustionForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea)

    def clean(self):
 
        super().clean()
         
        body = self.cleaned_data.get('body')

        if len(body) < 5 :
            self._errors['body'] = self.error_class([
                'body minimum 5 characters required'])

        return self.cleaned_data

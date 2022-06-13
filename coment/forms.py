from django import forms

class ComentsForm(forms.Form):
    choices = (
        ('y' , 'yes'),
        ('i' , 'I do not know'),
        ('n' , 'no'),
    )
    choice = (
        ('0' , '0'),
        ('1' , '1'),
        ('2' , '2'),
        ('3' , '3'),
        ('4' , '4'),
        ('5' , '5'),
    )
    sagestion = forms.CharField(max_length=50 , widget = forms.Select(choices=choices))
    score = forms.CharField(max_length=50 , widget = forms.Select(choices=choice))
    titel = forms.CharField(max_length=100 )
    body = forms.CharField(widget = forms.Textarea)
    image = forms.ImageField()
    bad = forms.CharField(widget = forms.Textarea)
    good = forms.CharField(widget = forms.Textarea)

class UpdateComentsForm(forms.Form):
    choices = (
        ('y' , 'yes'),
        ('i' , 'I do not know'),
        ('n' , 'no'),
    )
    choice = (
        ('0' , '0'),
        ('1' , '1'),
        ('2' , '2'),
        ('3' , '3'),
        ('4' , '4'),
        ('5' , '5'),
    )
    sagestion = forms.CharField(max_length=50 , widget = forms.Select(choices=choices))
    score = forms.CharField(max_length=50 , widget = forms.Select(choices=choice))
    titel = forms.CharField(max_length=100)
    body = forms.CharField(widget = forms.Textarea)
    image = forms.ImageField()
    bad = forms.CharField(widget = forms.Textarea)
    good = forms.CharField(widget = forms.Textarea)


from django import forms

class ComentsBlogForm(forms.Form):
    titel = forms.CharField(max_length=100 )
    body = forms.CharField(widget = forms.Textarea)

class UpdateComentsBlogForm(forms.Form):
    titel = forms.CharField(max_length=100)
    body = forms.CharField(widget = forms.Textarea)

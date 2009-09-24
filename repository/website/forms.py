from repository.winrepo.models import Package
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label=(u'username'),max_length=100)
    password = forms.CharField(label=(u'password'),widget=forms.PasswordInput(render_value=False)) 

class UploadFileForm(forms.Form):
    file  = forms.FileField()
    package = forms.ModelChoiceField(queryset=Package.objects.all())

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label=(u'username'),max_length=100)
    password = forms.CharField(label=(u'password'),widget=forms.PasswordInput(render_value=False)) 

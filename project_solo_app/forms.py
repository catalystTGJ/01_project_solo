from django import forms
class RegisterForm(forms.Form):
    url = forms.CharField(max_length=200)
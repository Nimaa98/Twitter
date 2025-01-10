
from django import forms


class LoginForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_data(self):
        return self.cleaned_data
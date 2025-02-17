
from django import forms


class LoginForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_info(self):
        return self.cleaned_data
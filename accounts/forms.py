from django import forms
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm

class PasswordResetForm(BasePasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)
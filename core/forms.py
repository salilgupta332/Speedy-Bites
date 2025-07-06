# --- Step 3.1: MenuItem Form START ---

from django import forms
from .models import Admin_User
from core.models import MenuItem
from django.core.exceptions import ValidationError

class MenuItemForm(forms.Form):
    name = forms.CharField(label='Dish Name', max_length=100)
    description = forms.CharField(label='Description', max_length=255, widget=forms.Textarea)
    price = forms.FloatField(label='Price (₹)')
    image = forms.ImageField(required=False)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if Admin_User.objects(username=username).first():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if Admin_User.objects(email=email).first():
            raise ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise ValidationError("Passwords do not match")

# --- Step 3.1: MenuItem Form END ---

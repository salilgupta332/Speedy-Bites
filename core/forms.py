# --- Step 3.1: MenuItem Form START ---

from django import forms
from core.models import MenuItem

class MenuItemForm(forms.Form):
    name = forms.CharField(label='Dish Name', max_length=100)
    description = forms.CharField(label='Description', max_length=255, widget=forms.Textarea)
    price = forms.FloatField(label='Price (₹)')

# --- Step 3.1: MenuItem Form END ---

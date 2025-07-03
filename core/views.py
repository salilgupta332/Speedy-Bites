from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import MenuItem

def home(request):
     # Fetch all menu items
    items = MenuItem.objects()

    # Render HTML response manually
    html = "<h1>Speedy Bites Menu</h1><ul>"
    for item in items:
        html += f"<li><strong>{item.name}</strong> - ₹{item.price} <br><small>{item.description}</small></li><br>"
    html += "</ul>"

    return HttpResponse(html)

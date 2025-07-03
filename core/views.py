from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import MenuItem
from .forms import MenuItemForm
from django.shortcuts import render, redirect

def home(request):
    # Fetch all menu items
    items = MenuItem.objects()
    
    # Pass data to the template
    return render(request, 'home.html', {'menu_items': items})

def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            MenuItem(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price']
            ).save()
            return redirect('home')
    else:
        form = MenuItemForm()
    return render(request, 'add_item.html', {'form': form})

def delete_menu_item(request, item_id):
    item = MenuItem.objects.get(id=item_id)
    item.delete()
    return redirect('home')


def edit_menu_item(request, item_id):
    item = MenuItem.objects.get(id=item_id)

    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            item.name = form.cleaned_data['name']
            item.price = form.cleaned_data['price']
            item.description = form.cleaned_data['description']
            item.save()
            return redirect('home')
    else:
        # Pre-fill the form manually
        form = MenuItemForm(initial={
            'name': item.name,
            'price': item.price,
            'description': item.description,
        })

    return render(request, 'edit_item.html', {'form': form})

def delete_menu_item(request, item_id):
    try:
        item = MenuItem.objects.get(id=item_id)
        item.delete()
        return redirect('home')
    except MenuItem.DoesNotExist:
        return HttpResponse("Item not found", status=404)


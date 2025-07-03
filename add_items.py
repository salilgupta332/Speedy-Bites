import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'speedy_bites.settings')
django.setup()

from core.models import MenuItem

MenuItem(name="Veggie Burger", description="Crispy patty with lettuce & tomato", price=149).save()
MenuItem(name="Paneer Wrap", description="Stuffed wrap with spicy paneer tikka", price=179).save()
MenuItem(name="Choco Lava Cake", description="Hot gooey chocolate center", price=99).save()

print("✅ Menu items added to MongoDB!")
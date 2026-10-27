import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inventory.models import MenuCategory, MenuItem
from table.models import Location, Table
from users.models import User
from order.models import Order
from common.models import Restaurant

# Create a Restaurant
rest, _ = Restaurant.objects.get_or_create(name='Test Restaurant')

# Locations
loc1, _ = Location.objects.get_or_create(name='Main Floor', restaurant=rest, defaults={'default_tax': 10.0})
loc2, _ = Location.objects.get_or_create(name='Patio', restaurant=rest, defaults={'default_tax': 10.0})

# Tables
t1, _ = Table.objects.get_or_create(name='Table 1', location=loc1, restaurant=rest, defaults={'capacity': 4})
t2, _ = Table.objects.get_or_create(name='Table 2', location=loc1, restaurant=rest, defaults={'capacity': 2})
t3, _ = Table.objects.get_or_create(name='Patio 1', location=loc2, restaurant=rest, defaults={'capacity': 4})

# Categories
cat1, _ = MenuCategory.objects.get_or_create(name='Starters', restaurant=rest)
cat2, _ = MenuCategory.objects.get_or_create(name='Mains', restaurant=rest)

# Items
m1, _ = MenuItem.objects.get_or_create(name='Garlic Bread', restaurant=rest, defaults={'price': 5.99})
m1.menu_category.add(cat1)
m2, _ = MenuItem.objects.get_or_create(name='Bruschetta', restaurant=rest, defaults={'price': 7.99})
m2.menu_category.add(cat1)
m3, _ = MenuItem.objects.get_or_create(name='Steak Frites', restaurant=rest, defaults={'price': 24.99})
m3.menu_category.add(cat2)
m4, _ = MenuItem.objects.get_or_create(name='Pasta Carbonara', restaurant=rest, defaults={'price': 18.99})
m4.menu_category.add(cat2)

# Waiter (If User model has restaurant field, uncomment it)
from users.models import Role
waiter_role, _ = Role.objects.get_or_create(name='Waiter', slug='waiter')
w1, _ = User.objects.get_or_create(phone_number='1234567890', name='Waiter 1', defaults={'role': waiter_role, 'restaurant': rest, 'pin': 1111})
w2, _ = User.objects.get_or_create(phone_number='0987654321', name='Waiter 2', defaults={'role': waiter_role, 'restaurant': rest, 'pin': 2222})
w1.set_password('password123')
w1.save()
w2.set_password('password123')
w2.save()

print('Test data created successfully!')

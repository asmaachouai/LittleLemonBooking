# tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from restaurant.models import Menu
from restaurant.serializers import MenuItemSerializer
import json

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.menu1 = Menu.objects.create(title="Pizza", price=120, inventory=50)
        self.menu2 = Menu.objects.create(title="Burger", price=60, inventory=30)

    def test_get_all_menu_items(self):
        response = self.client.get(reverse('menu-list'))  # make sure 'menu-list' is in urls
        menu_items = Menu.objects.all()
        serializer_data = MenuItemSerializer(menu_items, many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), serializer_data)

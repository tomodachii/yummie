from django.test import TestCase

from poll.models import Dish, Menu


class DishModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Dish.objects.create(name='Pizza', price=30000, type='f')

    def test_name_label(self):
        dish = Dish.objects.get(id=1)
        field_label = dish._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_price_label(self):
        dish = Dish.objects.get(id=1)
        field_label = dish._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'price')

    def test_name_max_length(self):
        dish = Dish.objects.get(id=1)
        max_length = dish._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_name_type_price(self):
        dish = Dish.objects.get(id=1)
        expected_object_name = f'{dish.name} {dish.type} {dish.price}'
        self.assertEqual(str(dish), expected_object_name)

    def test_absolute_url(self):
        dish = Dish.objects.get(id=1)
        self.assertEqual(dish.get_absolute_url(), '/dish/1')


class MenuModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Dish.objects.create(name='Pizza', price=30000, type='f')
        Dish.objects.create(name='Hotdog', price=20000, type='f')
        Dish.objects.create(name='Coffee', price=5000, type='d')
        dishes = Dish.objects.all()
        # Menu.objects.create(dish=dishes, due="2018-12-19 09:26:03.478039")
        Menu.objects.create(due="2018-12-19 09:26:03.478039").dish.set(dishes)

    def test_dish_label(self):
        menu = Menu.objects.get(id=1)
        field_label = menu._meta.get_field('dish').verbose_name
        self.assertEqual(field_label, 'dish')

    def test_object_name_is_time_seconds(self):
        menu = Menu.objects.get(id=1)
        expected_object_name = f'{menu.time_seconds()}'
        self.assertEqual(str(menu), expected_object_name)

    def test_absolute_url(self):
        menu = Menu.objects.get(id=1)
        self.assertEqual(menu.get_absolute_url(), '/poll/1/')

    def test_display_dish(self):
        menu = Menu.objects.get(id=1)
        dishes = Dish.objects.all()
        expected_result = ', '.join(dish.name for dish in dishes)
        self.assertEqual(menu.display_dish(), expected_result)

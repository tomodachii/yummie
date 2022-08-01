from django.test import TestCase
from django.urls import reverse

from poll.models import Dish


class DishListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_dishes = 13

        for dish_id in range(number_of_dishes):
            Dish.objects.create(
                type=f'f',
                name=f'Dish {dish_id}',
                price=20000,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/dishes/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('dishes'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('dishes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dish/dish_list.html')

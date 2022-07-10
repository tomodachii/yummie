# Used to generate URLs by reversing the URL patterns
from django.urls import reverse
import uuid  # Required for unique book instances
from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Dish(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    DISH_TYPE = (
        ('f', 'Food'),
        ('d', 'Drink'),
    )
    type = models.CharField(max_length=1, choices=DISH_TYPE,
                            blank=False, default='f', help_text='Dish type')

    class Meta:
        ordering = ['name']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name} {self.type} {self.price}'

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('dish-detail', args=[str(self.id)])


class Menu(models.Model):
    dish = models.ManyToManyField(
        Dish, help_text="Select dish for this Menu")
    due = models.DateTimeField()

    STATUS_LIST = (
        ('o', 'open'),
        ('c', 'close'),
    )
    status = models.CharField(
        max_length=1, choices=STATUS_LIST, blank=False, default='o', help_text='Status')

    def display_dish(self):
        """Create a string for the Dish. This is required to display dish in Admin."""
        return ', '.join(dish.name for dish in self.dish.all())

    def list_dish(self):
        return self.dish.all()

    display_dish.short_description = 'dish list'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.due}'

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('poll-detail', args=[str(self.id)])

    class Meta:
        ordering = ['due']


class Vote(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    menu = models.ForeignKey(
        Menu, on_delete=models.SET_NULL, null=True, blank=True)
    user_name = models.CharField(max_length=300)
    DISH_LIST = ((i['name'], i['name'])
                 for i in Dish.objects.all().values('name'))
    dish_name = models.CharField(
        max_length=300, choices=DISH_LIST, blank=True, null=True, help_text='Dish')
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    vote_as = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField()

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('vote-detail', args=[str(self.id)])

    class Meta:
        ordering = ['user_name', 'dish_name']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.user_name} {self.dish_name} {self.created_at}'


def get_user_name(self):
    if self.first_name or self.last_name:
        return self.first_name + " " + self.last_name
    return self.username


User.add_to_class("get_user_name", get_user_name)

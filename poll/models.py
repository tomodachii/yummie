# Used to generate URLs by reversing the URL patterns
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Dish(models.Model):
    DISH_TYPE = (
        ('f', 'Food'),
        ('d', 'Drink'),
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=2)
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

    class Meta:
        ordering = ['-due']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.time_seconds()}'

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('poll-detail', args=[str(self.id)])

    def display_dish(self):
        """Create a string for the Dish. This is required to display dish in Admin."""
        return ', '.join(dish.name for dish in self.dish.all())

    def list_dish(self):
        return self.dish.all()

    display_dish.short_description = 'dish list'

    def time_seconds(self):
        return self.due.strftime("%d/%m/%Y, %H:%M")

    time_seconds.short_description = 'menu due' 


class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
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

    class Meta:
        ordering = ['-created_at', 'dish_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('vote-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.user_name} {self.dish_name} {self.created_at}'

    # def time_seconds(self):
    #     return self.created_at.strftime("%d/%m/%Y, %H:%M")

    # time_seconds.short_description = 'created time' 


USER_GENDER_CHOICES = [
    (0, 'Not declared'),
    (1, 'Male'),
    (2, 'Female'),
]

class User(AbstractUser):
    gender = models.PositiveSmallIntegerField("Gender", choices=USER_GENDER_CHOICES, default=0)
    # add additional fields in here

    def __str__(self):
        return self.username

    def get_user_name(self):
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        return self.username

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('user-detail', args=[str(self.id)])


# User.add_to_class("get_user_name", get_user_name)
# User.add_to_class("get_absolute_url", lambda self: reverse(
#     'user-detail', args=[str(self.id)]))

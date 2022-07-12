from django.contrib import admin
from .models import Dish, Menu, Vote
# Register your models here.


class DishAdmin(admin.ModelAdmin):
    pass


admin.site.register(Dish, DishAdmin)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['due', 'display_dish']


admin.site.register(Vote)

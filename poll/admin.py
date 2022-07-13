from django.contrib import admin
from .models import Dish, Menu, Vote, User
# Register your models here.

from django.contrib.auth.admin import UserAdmin

from .forms import NewUserForm, CustomUserChangeForm

class UserAdmin(UserAdmin):
    add_form = NewUserForm 
    form = CustomUserChangeForm
    model = User
    list_display = ["email", "gender", "username", "first_name", "last_name"]

admin.site.register(User, UserAdmin)

class DishAdmin(admin.ModelAdmin):
    pass


admin.site.register(Dish, DishAdmin)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['due', 'display_dish']


admin.site.register(Vote)

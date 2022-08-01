from django.contrib import admin
from .models import Dish, Menu, Vote, User
# Register your models here.

from django.contrib.auth.admin import UserAdmin

from .forms import NewUserForm, CustomUserChangeForm

class UserAdmin(UserAdmin):
    add_form = NewUserForm 
    form = CustomUserChangeForm
    model = User
    list_display = ["username", "gender", "email", "first_name", "last_name", "is_staff"]
    list_display_links = ('username',)
    list_editable = ["gender"]

admin.site.register(User, UserAdmin)

class DishAdmin(admin.ModelAdmin):
    model = Dish
    # list_display = [field.name for field in Dish._meta.get_fields()]
    list_display = ["name", "price", "type"]

admin.site.register(Dish, DishAdmin)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['time_seconds', 'display_dish']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_name', 'menu', 'cost', 'vote_as', 'time_seconds']

    @admin.display(ordering='vote__created_at')
    def time_seconds(self, obj):
        return obj.created_at.strftime("%d/%m/%Y, %H:%M")
    # fields = (('user', 'user_name'), 'menu', 'dish_name', 'cost', 'vote_as', 'created_at')
    

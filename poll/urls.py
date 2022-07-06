from operator import index
from django.urls import include, path
from . import views

urlpatterns = [
    path('poll/', views.get_vote_view, name='poll'),
    path('accounts/register', views.register_request, name="register"),
    path('poll/<int:menu_id>/<int:dish_id>/vote', views.make_vote, name='vote'),
]

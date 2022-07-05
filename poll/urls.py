from operator import index
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.vote_view, name='index'),
]

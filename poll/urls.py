from operator import index
from django.urls import include, path
from . import views

urlpatterns = [
    path('poll/', views.get_vote_view, name='poll'),
    path('accounts/register', views.register_request, name="register"),
    path('poll/<int:menu_id>/<int:dish_id>/vote',
         views.make_vote, name='poll-vote'),
    path('poll/create/', views.MenuCreate.as_view(), name='poll-create'),
    path('poll/<int:pk>/update/', views.MenuUpdate.as_view(), name='poll-update'),
    path('poll/<int:pk>/delete/', views.MenuDelete.as_view(), name='poll-delete'),
    path('poll/<int:pk>/', views.poll_detail_view, name='poll-detail'),
    path('dishes/', views.DishListView.as_view(), name='dishes'),
    path('dish/<int:pk>', views.DishDetailView.as_view(), name='dish-detail'),
    path('dish/create/', views.DishCreate.as_view(), name='dish-create'),
    path('dish/<int:pk>/update/', views.DishUpdate.as_view(), name='dish-update'),
    path('dish/<int:pk>/delete/', views.DishDelete.as_view(), name='dish-delete'),
    path('votes/', views.VoteListView.as_view(), name='votes'),
    path('vote/<int:pk>/', views.VoteDetailView.as_view(), name="vote-detail"),
    path('vote/<int:pk>/update/', views.VoteUpdate.as_view(), name='vote-update'),
    path('vote/<int:pk>/delete/', views.VoteDelete.as_view(), name='vote-delete'),

]

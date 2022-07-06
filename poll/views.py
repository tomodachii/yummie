from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Dish, Menu, Vote
from django.contrib.auth.models import User
from .forms import NewUserForm, NewVoteForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
import datetime

# Create your views here.
# def store_vote(request):
#   new_vote = UserVote.objects.create(user=request.user, user_name=request.user.username)

HOME_URL = '/poll/'


def index(request):
    context = {'hello': 'hello'}
    return render(request, 'index.html', context=context)

# @login_required


def add_item(a):
    votes = Vote.objects.filter(menu_id=a.id)
    return {'menu': a, 'votes': votes}


def get_vote_view(request):
    menu = Menu.objects.all()
    menu_list = map(add_item, menu)
    # for menu_instance in menu:
    #     votes = Vote.objects.filter(menu_id=menu_instance.id)
    #     menu_instance
    return render(request, 'poll/poll.html', context={
        "menu": menu,
        "menu_list": menu_list,
    })


@login_required
def make_vote(request, menu_id, dish_id):
    menu = Menu.objects.get(pk=menu_id)
    dish = Dish.objects.get(pk=dish_id)
    user = request.user
    message = ''
    try:
        if request.method == 'POST':
            form = NewVoteForm(request.POST)
            if form.is_valid():
                if request.POST.get('vote') == 'on':
                    Vote.objects.create(
                        user_id=user.id, menu_id=menu.id, user_name=user.get_user_name(), dish_name=dish.name, cost=dish.price, created_at=datetime.datetime.now())
                    messages.success(
                        request, 'Vote has been successful created!')
                else:
                    message = 'Vote has been canceled!'
                return HttpResponseRedirect(HOME_URL)
            else:
                messages.warning(request, 'Please correct the error below.')
        else:
            form = NewVoteForm()

        return render(request, 'poll/vote.html', context={
            'form': form,
            'menu': menu,
            'dish': dish,
            'message': message,
        })

    except Exception as e:
        print(e)
        return HttpResponseRedirect(HOME_URL)


# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# def create_poll(request):
#     try:
#         if request.method == 'POST':
#             form = NewVoteForm(request.POST)
#             if form.is_valid():
#                 messages.success(request, 'Poll has successful created!')
#                 return HttpResponseRedirect(HOME_URL)
#             else:
#                 messages.warning(request, 'Please correct the error below.')
#         else:
#             form = NewVoteForm()

#         return render(request, 'poll/create_poll.html', context={

#         })
#     except Exception as e:
#         print(e)
#         return HttpResponseRedirect(HOME_URL)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return HttpResponseRedirect(HOME_URL)
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})


class MenuCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Menu
    fields = ['dish', 'due', 'status']
    initial = {'status': 'o'}

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(HOME_URL)


class MenuUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Menu
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(HOME_URL)


class MenuDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Menu
    success_url = reverse_lazy('poll')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(HOME_URL)

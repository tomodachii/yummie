from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Dish, Menu, Vote
from django.contrib.auth.models import User
from .forms import NewUserForm, NewVoteForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
# def store_vote(request):
#   new_vote = UserVote.objects.create(user=request.user, user_name=request.user.username)


def index(request):
    context = {'hello': 'hello'}
    return render(request, 'index.html', context=context)

# @login_required


def get_vote_view(request):
    menu = Menu.objects.all()
    message = ''
    # NewVoteFormSet = formset_factory(NewVoteForm)
    try:
        if request.method == 'POST':
            form = NewVoteForm(request.POST)
            # formset = NewVoteFormSet(request.POST)

            # print(request.POST)
            if form.is_valid():
                # vote = Vote.objects.create(
                #     user_id=request.POST.get('user')
                # )
                # print(request.POST.get('user'))
                pass
            else:
                messages.warning(request, 'Please correct the error below.')
        else:
            form = NewVoteForm()

        return render(request, 'poll/poll.html', context={
            "menu": menu,
            "message": message
        })

    except Exception as e:
        print(e)


@login_required
def make_vote(request, menu_id, dish_id):
    menu = Menu.objects.get(pk=menu_id)
    dish = Dish.objects.get(pk=dish_id)
    user = request.user
    temp = ''
    try:
        if request.method == 'POST':
            form = NewVoteForm(request.POST)
            if form.is_valid():
                temp = request.POST.get('vote')
                if temp == 'on':
                    temp = 'Vote thành công'
                    Vote.objects.create(
                        user_id=user.id, menu_id=menu.id, user_name=user.get_user_name(), dish_name=dish.name, cost=dish.price, created_at=datetime.datetime.now())
                    messages.success(
                        request, 'Project has successful created!')
                else:
                    temp = 'Hủy vote thành công'
                return HttpResponseRedirect('/poll/')
            else:
                messages.warning(request, 'Please correct the error below.')
        else:
            form = NewVoteForm()

        return render(request, 'poll/vote.html', context={
            'form': form,
            'menu': menu,
            'dish': dish,
            'temp': temp,
        })

    except Exception as e:
        # return HttpResponseRedirect('/poll/')
        print(e)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:homepage")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})

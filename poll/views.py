from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Dish, Menu, Vote
from django.contrib.auth.models import User
from .forms import NewUserForm, NewVoteForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

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
        # temp = request.POST
        return render(request, 'poll/poll.html', context={
            "form": form,
            "menu": menu,
            "message": message
        })

    except Exception as e:
        print(e)


def make_vote(request):
    pass


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

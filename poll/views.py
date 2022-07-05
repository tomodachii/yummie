from django.http import HttpResponse
from django.shortcuts import render
from .models import User, Vote

# Create your views here.
# def store_vote(request):
#   new_vote = UserVote.objects.create(user=request.user, user_name=request.user.username)


def index(request):
    context = {'hello': 'hello'}
    return render(request, 'index.html', context=context)


def vote_view(request):
    context = {'hello': 'hello'}
    return render(request, 'poll/poll.html', context=context)

from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from .models import Dish, Menu, Vote, User
from .forms import MenuForm, NewUserForm, NewVoteForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
import datetime
from django.views import generic
from django.core.paginator import Paginator, EmptyPage
import pytz
from django.utils import timezone

HOME_URL = '/'
DISH_LIST_URL = '/dishes/'


def total_seconds(td):
    # Keep backward compatibility with Python 2.6 which doesn't have
    # this method
    if hasattr(td, 'total_seconds'):
        return td.total_seconds()
    else:
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6


def convert_to_localtime(utc_time):
    utc = utc_time.replace(tzinfo=pytz.UTC)
    return utc.astimezone(timezone.get_current_timezone())


def add_votes_info_to_poll(menu):
    results = {}
    votes = Vote.objects.filter(menu_id=menu.id)
    for item in menu.list_dish():
        arr = []
        for vote in votes:
            if item.name == vote.dish_name:
                arr.append(vote)
        results[item.name] = arr
    return {'menu': menu, 'votes': votes, 'results': results}


def get_index(request):
    today_min = datetime.datetime.combine(
        datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(
        datetime.date.today(), datetime.time.max)
    this_month = datetime.datetime.now().month

    menu_list = Menu.objects.filter(
        due__range=(today_min, today_max)).order_by('due')
    menu_list = map(add_votes_info_to_poll, menu_list)
    user_votes = Vote.objects.filter(user_id=request.user.id)
    user_total_cost = 0
    for vote in user_votes:
        user_total_cost += vote.cost

    return render(request, 'index.html', context={
        "menu_list": menu_list,
        "user_votes": user_votes,
        "this_month": this_month,
        "user_total_cost": user_total_cost,
    })


def get_vote_view(request, page=1):
    menu_list = Menu.objects.all()
    menu_list = map(add_votes_info_to_poll, menu_list)
    paginator = Paginator(list(menu_list), 3)
    try:
        menu_list = paginator.page(page)
    except EmptyPage:
        # if we exceed the page limit we return the last page
        menu_list = paginator.page(paginator.num_pages)
    return render(request, 'poll/polls.html', context={
        "menu_list": menu_list,
    })


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
    form_class = MenuForm

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(HOME_URL)


class MenuUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Menu
    form_class = MenuForm
    # Not recommended (potential security issue if more fields added)
    # fields = '__all__'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(HOME_URL)


class MenuDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Menu
    success_url = reverse_lazy('polls', args=[1])

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(HOME_URL)


class DishCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Dish
    fields = ['name', 'price', 'type']
    template_name = 'dish/dish_form.html'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(HOME_URL)


class DishUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Dish
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    template_name = 'dish/dish_form.html'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(HOME_URL)


class DishDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Dish
    success_url = reverse_lazy('dishes')
    template_name = 'dish/dish_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(HOME_URL)


class DishListView(generic.ListView):
    template_name = 'dish/dish_list.html'
    model = Dish


class DishDetailView(generic.DetailView):
    template_name = 'dish/dish_detail.html'
    model = Dish


def poll_detail_view(request, pk):
    menu = Menu.objects.get(pk=pk)
    votes = Vote.objects.filter(menu_id=pk)
    return render(request, 'poll/poll_detail.html', context={
        "menu": menu,
        "votes": votes,
    })


class VoteDetailView(generic.DetailView):
    template_name = 'vote/vote_detail.html'
    model = Vote


class VoteListView(generic.ListView):
    template_name = 'vote/vote_list.html'
    model = Vote


@login_required
def make_vote(request, menu_id, dish_id):

    try:
        try:
            menu = Menu.objects.get(pk=menu_id)
        except Menu.DoesNotExist:
            raise Http404('Menu does not exist')
        try:
            dish = Dish.objects.get(pk=dish_id, menu=menu_id)
        except Menu.DoesNotExist:
            raise Http404('Dish does not exist')
        user = request.user
        message = ''
        flag = True
        if Vote.objects.filter(menu_id=menu_id, dish_name=dish.name, user_id=user.id).exists():
            flag = False
        if request.method == 'POST':
            form = NewVoteForm(request.POST)
            if form.is_valid():
                val = form.cleaned_data.get("btn")
                # if request.POST.get('btn') == 'vote' and total_seconds(convert_to_localtime(menu.due).replace(tzinfo=None) - datetime.datetime.now().replace(tzinfo=None)) > 0:
                if val == 'vote' and total_seconds(convert_to_localtime(menu.due).replace(tzinfo=None) - datetime.datetime.now().replace(tzinfo=None)) > 0:
                    Vote.objects.create(
                        user_id=user.id, menu_id=menu.id, user_name=user.get_user_name(), dish_name=dish.name, cost=dish.price, created_at=datetime.datetime.now())
                    messages.success(
                        request, 'Vote has been successful created!')
                else:
                    vote = Vote.objects.filter(
                        menu_id=menu_id, dish_name=dish.name, user_id=user.id)
                    vote.delete()
                    message = 'Vote has been canceled!'
                return HttpResponseRedirect(HOME_URL)
            else:
                messages.warning(request, 'Please correct the error below.')
        else:
            form = NewVoteForm()

        return render(request, 'vote/vote_create.html', context={
            'form': form,
            'menu': menu,
            'dish': dish,
            'message': message,
            'flag': flag,
        })

    except Exception as e:
        print(e)
        return HttpResponseRedirect(HOME_URL)


class VoteUpdate(LoginRequiredMixin, UpdateView):
    model = Vote
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    template_name = 'vote/vote_form.html'

    def get_object(self, *args, **kwargs):
        obj = super(VoteUpdate, self).get_object(*args, **kwargs)
        if not self.request.user.is_superuser and not obj.user == self.request.user:
            raise Http404  # maybe you'll need to write a middleware to catch 403's same way
        return obj

    def handle_no_permission(self):
        return HttpResponseRedirect(HOME_URL)


class VoteDelete(LoginRequiredMixin, DeleteView):
    model = Vote
    success_url = reverse_lazy('polls', args=[1])
    template_name = 'vote/vote_confirm_delete.html'

    def get_object(self, *args, **kwargs):
        obj = super(VoteDelete, self).get_object(*args, **kwargs)
        if not self.request.user.is_superuser and not obj.user == self.request.user:
            raise Http404  # maybe you'll need to write a middleware to catch 403's same way
        return obj

    def handle_no_permission(self):
        return HttpResponseRedirect(HOME_URL)


class UserListView(generic.ListView):
    template_name = 'auth/user_list.html'
    model = User


class UserDetailView(generic.DetailView):
    template_name = 'auth/user_detail.html'
    model = User


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    template_name = 'auth/user_form.html'

    def get_object(self, *args, **kwargs):
        obj = super(UserUpdate, self).get_object(*args, **kwargs)
        if not self.request.user.is_superuser and not obj.user == self.request.user:
            raise Http404  # maybe you'll need to write a middleware to catch 403's same way
        return obj

    def handle_no_permission(self):
        return HttpResponseRedirect(HOME_URL)


class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('polls', args=[1])
    template_name = 'auth/user_confirm_delete.html'

    def get_object(self, *args, **kwargs):
        obj = super(UserDelete, self).get_object(*args, **kwargs)
        if not self.request.user.is_superuser and not obj.user == self.request.user:
            raise Http404  # maybe you'll need to write a middleware to catch 403's same way
        return obj

    def handle_no_permission(self):
        return HttpResponseRedirect(HOME_URL)


def add_votes_info_to_financial_manage(menu):
    results = []
    votes = Vote.objects.filter(menu_id=menu.id)
    user_list = User.objects.all()
    for user in user_list:
        sum = 0
        for vote in votes:
            if user.id == vote.user_id:
                sum += vote.cost
        results.append(sum)
    return {'menu': menu, 'votes': votes, 'results': results}


@login_required
def financial_manage(request):
    user_list = User.objects.all()
    menu_list = Menu.objects.all()
    menu_list = map(add_votes_info_to_financial_manage, menu_list)
    return render(request, 'financial_manage.html', context={
        "user_list": user_list,
        "menu_list": menu_list,
    })

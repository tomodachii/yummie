from django import forms
from django.forms import SplitDateTimeWidget, TimeInput, DateInput
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Menu
import datetime


# Create your forms here.


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name",
                  "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewVoteForm(forms.Form):
    vote = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'onclick': 'this.form.submit();',
            }
        ),
        label=False,
    )


class NewPollForm(forms.Form):
    vote = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'onclick': 'this.form.submit();',
            }
        ),
        label=False,
    )


class DateInput(forms.DateInput):
    input_type = 'date'


class MySplitDateTimeWidget(SplitDateTimeWidget):
    def __init__(self, attrs=None, date_format=None, time_format=None):
        # date_class = attrs.pop('date_class')
        # time_class = attrs.pop('time_class')

        widgets = (DateInput(attrs={'class': 'date_class'}, format=date_format),
                   TimeInput(attrs={'class': 'date_class', 'type': 'time'}, format=time_format))
        super(SplitDateTimeWidget, self).__init__(widgets, attrs)


class MenuForm(ModelForm):

    class Meta:
        model = Menu
        fields = ['dish', 'due', 'status']
        widgets = {
            'due': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'picker',
                }
            ),
        }

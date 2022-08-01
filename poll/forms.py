from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import Menu, User


# Create your forms here.


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name",
                  "last_name", "gender", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username", "email")


class NewVoteForm(forms.Form):
    btn = forms.CharField()


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


class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ['dish', 'due']
        widgets = {
            'due': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'picker',
                }
            ),
        }

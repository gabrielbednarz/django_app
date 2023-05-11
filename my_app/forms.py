from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from my_app.models import Employee

from django.core.validators import RegexValidator


# We don't want to match substrings, that's why ^ and $ are used. ^ and $ prevent the situation in which,
# at the beginning or at the end of a string, there is a character not included in square brackets.

username_validator = RegexValidator(
    r'^[\w.@+\-()\s]+$',
    'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/()/space characters.'
)


class CompanyRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Company', max_length=128, required=True, validators=[username_validator])
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CompanyLoginForm(forms.Form):
    username = forms.CharField(label='Company')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


# To make the form field of date_of_birth from models.py display a calendar-like widget
# (date picker), we need to use DateInput:

class DateInput(forms.DateInput):
    input_type = 'date'  # Boilerplate code.


# Then, we assign DateInput() object to date_of_birth:

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        # fields = '__all__'
        exclude = ('company',)

        widgets = {'date_of_birth': DateInput()}  # DateInput() - an instance. DateInput - a class.

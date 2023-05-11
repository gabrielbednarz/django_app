from django.shortcuts import render, redirect, get_object_or_404
from my_project import settings
from my_app.models import *

from my_app.forms import CompanyRegistrationForm, EmployeeForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'my_app/homepage.html')


@login_required
def staff(request):
    workers = Employee.objects.filter(company=request.user)  # company is a foreign key from Employee to User.
    media_url = settings.MEDIA_URL                           # user is an attribute of request.
    context = {'workers': workers, 'MEDIA_URL': media_url}
    return render(request, 'my_app/staff.html', context)


def register(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            company = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=company, password=password)
            if user is not None:
                login(request, user)
                return redirect('staff')
            else:
                return redirect('register')
        else:
            print(form.errors)  # Show form errors in the console
            return render(request, 'my_app/register.html', {'form': form})  # Returns the error message.
    else:
        form = CompanyRegistrationForm()
        return render(request, 'my_app/register.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            company = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=company, password=password)
            if user is not None:
                login(request, user)
                return redirect('staff')
            else:
                form.add_error(None, 'Invalid credentials')
                return render(request, 'my_app/login.html', {'form': form})
        else:
            return render(request, 'my_app/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'my_app/login.html', {'form': form})


@login_required
def log_out(request):
    logout(request)
    return redirect('homepage')


# The CRUD part:

@login_required
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.company = request.user  # That's why in forms.py we have exclude = ('company',).
            employee.save()
            return redirect('staff')
        else:
            return render(request, 'my_app/create_employee.html', {'form': form})
    else:
        form = EmployeeForm()
        return render(request, 'my_app/create_employee.html', {'form': form})


# In both of two next functions, @login_required and company=request.user mean a double check
# to make sure the logged-in user has the right to delete the specific employee.

# In the update_employee function, the instance=employee is provided: (1) in the case of GET method, to pre-populate
# the EmployeeForm with the data from the specified Employee instance (a row in the table); (2) in the case of POST
# method, to tell the EmployeeForm to update the Employee object instead of creating a new one.

@login_required
def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id, company=request.user)
    if request.method == 'POST':
        form = EmployeeForm(data=request.POST, files=request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('staff')
    else:
        form = EmployeeForm(instance=employee)
        return render(request, 'my_app/update_employee.html', {'form': form})


@login_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id, company=request.user)
    employee.delete()
    return redirect('staff')

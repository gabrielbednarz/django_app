from django.test import TestCase
from django.contrib.auth.models import User
from my_app.models import Employee
from my_app.forms import CompanyRegistrationForm, EmployeeForm
from django.urls import reverse

from django.contrib.auth import authenticate


# Test the string representation of an Employee object.

class TestEmployeeModel(TestCase):
    def test_str_representation(self):
        employee = Employee(first_name='John', last_name='Donne', job_title='Developer')
        self.assertEqual(str(employee), 'Donne, John - Developer')


# Test some view functions.

class TestHomeView(TestCase):
    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse('homepage'))  # Simulate user's GET request to the URL. HttpResponse object.
        self.assertEqual(response.status_code, 200)      # reverse() returns the URL.
        self.assertTemplateUsed(response, 'my_app/homepage.html')  # Checks if the response object was generated
        # using the specified template file 'my_app/homepage.html' (not URL).


class TestStaffView(TestCase):
    def setUp(self):

        # The line below simulates creating a User instance (company).

        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_staff_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('staff'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_app/staff.html')

    # For the next test, it is not necessary to create a user in the setUp method. This test case is checking if the
    # user is redirected to the login page when trying to access staff/ without being logged in (there's nothing like
    # self.client.login(username='testuser', password='testpassword')).

    def test_staff_view_no_login(self):
        response = self.client.get(reverse('staff'))
        self.assertRedirects(response, '/login/?next=/staff/')

        # The last line checks if response redirects not logged user to login page.


class RegisterViewTests(TestCase):
    def test_register_view_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)  # A successful GET request returns a status code of 200.
        self.assertTemplateUsed(response, 'my_app/register.html')

    def test_register_view_successful_registration(self):
        form_data = {
            'username': 'testcompany',
            'email': 'testcompany@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 302)  # A successful POST request returns a status code of 302.
        self.assertRedirects(response, '/staff/')  # URL be used instead of reverse('staff').

        user = User.objects.filter(username='testcompany').first()

        # .first() returns exactly ony such User object. No need to handle DoesNotExist or MultipleObjectsReturned
        # exceptions, which could happen in case of using User.objects.get(username='testcompany').

        # try:
        #     user = User.objects.get(username='testcompany')
        # except User.DoesNotExist:
        #     user = None
        # except User.MultipleObjectsReturned:
        #     user = User.objects.filter(username='testcompany').first()

        # We could end up eventually using User.objects.filter(username='testcompany').first().

        self.assertIsNotNone(user)  # User.objects.filter(username='testcompany').first() might return None.
        self.assertTrue(user.is_authenticated)  # It is a User method.

    def test_register_view_registration_with_invalid_data(self):
        form_data = {
            'username': 'testcompany',
            'email': 'testcompany@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword123'
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_app/register.html')


# Test forms.

class TestForm(TestCase):
    def test_company_registration_form(self):
        form_data = {
            'username': 'testcompany',
            'email': 'testcompany@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = CompanyRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        authenticated_user = authenticate(username=form_data['username'], password=form_data['password1'])
        self.assertIsNotNone(authenticated_user)

    def test_employee_form(self):
        # user = User.objects.create_user(username='testuser', password='testpassword')
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'gender': 'M',
            'salary': 50000,
            'job_title': 'Manager',
            'company': 'testuser',
            'email': 'johndoe@example.com',
        }
        form = EmployeeForm(data=form_data)
        self.assertTrue(form.is_valid())

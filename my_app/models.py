from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import User


class Employee(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    salary = models.IntegerField()
    job_title = models.CharField(max_length=128, null=True, blank=True)
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(validators=[EmailValidator], null=True, blank=True)
    image = models.ImageField(upload_to='employee_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} - {self.job_title}"

from django.urls import path
from my_app import views

# app_name = 'my_app'
urlpatterns = [
    path('', views.home, name='homepage'),
    path('staff/', views.staff, name='staff'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('staff/create/', views.create_employee, name='create_employee'),
    path('staff/update/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('staff/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
]

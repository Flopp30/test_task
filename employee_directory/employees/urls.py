from django.urls import path
from employees import views

app_name = "employees"

urlpatterns = [
    path('', views.show_employee, name='employees_dir'),
    path('employees_list/', views.show_employees_list, name='employees_list'),
    path('create/', views.create_employee, name='create_employee'),
    path('delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
]

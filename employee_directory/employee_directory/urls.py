from django.contrib import admin
from django.urls import path
from employees.views import show_employee, show_employees_list
from users.views import login, registration, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_employee),
    path('employees_list/', show_employees_list, name='employees_list'),
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('logout/', logout, name='logout'),
]

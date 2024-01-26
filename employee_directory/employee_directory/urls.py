from django.contrib import admin
from django.urls import path
from employees.views import show_employee, show_employees_list, create_employee, delete_employee, edit_employee
from users.views import login, registration, logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_employee, name='employees_dir'),
    path('employees_list/', show_employees_list, name='employees_list'),
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('logout/', logout, name='logout'),
    path('create/', create_employee, name='create_employee'),
    path('delete/<int:employee_id>/', delete_employee, name='delete_employee'),
    path('edit/<int:employee_id>/', edit_employee, name='edit_employee'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from employees import views

app_name = "employees"

urlpatterns = [
    path('', views.EmployeeTreeView.as_view(), name='employees_dir'),
    path('get_chilndren/', views.EmployeeTreeViewGetChildren.as_view(), name='employees_tree_children'),
    path('employees_list/', views.EmployeeListView.as_view(), name='employees_list'),
    path('create/', views.EmployeeCreateView.as_view(), name='create_employee'),
    path('delete/<int:pk>/', views.EmployeeDeleteView.as_view(), name='delete_employee'),
    path('edit/<int:pk>/', views.EmployeeUpdateView.as_view(), name='edit_employee'),
]

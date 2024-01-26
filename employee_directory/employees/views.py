from django.shortcuts import render, redirect, get_object_or_404
from employees.models import Employee
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from employees.forms import EmployeeCreateForm, EmployeeEditForm


def show_employee(request):
    return render(request, "employees_dir.html", {'employee': Employee.objects.all()})


@login_required
def show_employees_list(request):
    search_query = request.GET.get('search', '')  # Получаем параметр поиска из запроса GET
    sort_by = request.GET.get('sort_by', 'name')  # Получаем параметр сортировки из запроса GET
    employees = Employee.objects.filter(
        Q(name__icontains=search_query) |   # Фильтруем список сотрудников по всем полям
        Q(position__icontains=search_query) |
        Q(date_of_receipt__icontains=search_query) |
        Q(salary__icontains=search_query)
    ).order_by(sort_by)  # Сортируем список сотрудников
    return render(request, 'employees_list.html', {'employees': employees,
                                                   'search_query': search_query, 'sort_by': sort_by})


@login_required
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeeCreateForm()

    return render(request, 'create_employee.html', {'form': form})


@login_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.delete()
        return redirect('employees_list')
    return render(request, 'delete_employee.html', {'employee': employee})


@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeEditForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('edit_employee', employee_id)
    else:
        form = EmployeeEditForm(instance=employee)

    return render(request, 'edit_employee.html', {'form': form})

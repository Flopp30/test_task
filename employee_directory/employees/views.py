from django.shortcuts import render
from employees.models import Employee
from django.db.models import Q
from django.contrib.auth.decorators import login_required


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
        Q(salory__icontains=search_query)
    ).order_by(sort_by)  # Сортируем список сотрудников
    return render(request, 'employees_list.html', {'employees': employees,
                                                   'search_query': search_query, 'sort_by': sort_by})

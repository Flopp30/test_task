from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView

from employees.forms import EmployeeCreateForm, EmployeeEditForm
from employees.models import Employee


# TODO оставил тут твои старые вьюхи, чтобы ты посмотрел разницу. Писать на классах сильно удобнее :)
#   Удалить
# def show_employee(request):
#     return render(request, ".employees/employees_tree.html", {'employee': Employee.objects.all()})
class EmployeeTreeView(TemplateView):
    template_name = ".employees/employees_tree.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"root_employees": Employee.objects.filter(level=0)}


class EmployeeTreeViewGetChildren(TemplateView):
    template_name = ".employees/employees_tree_children.html"

    def get_context_data(self, **kwargs):
        parent_pk = self.request.GET.get("parent_pk")
        return super().get_context_data(**kwargs) | {"children": Employee.objects.filter(parent_id=parent_pk)}


# TODO удалить :)
# @login_required
# def show_employees_list(request):
#     search_query = request.GET.get('search', '')  # Получаем параметр поиска из запроса GET
#     sort_by = request.GET.get('sort_by', 'name')  # Получаем параметр сортировки из запроса GET
#     employees = Employee.objects.filter(
#         Q(name__icontains=search_query) |  # Фильтруем список сотрудников по всем полям
#         Q(position__icontains=search_query) |
#         Q(date_of_receipt__icontains=search_query) |
#         Q(salary__icontains=search_query)
#     ).order_by(sort_by)  # Сортируем список сотрудников
#     return render(request, '.employees/employees_list.html', {'employees': employees,
#                                                               'search_query': search_query, 'sort_by': sort_by})


class EmployeeListView(LoginRequiredMixin, ListView):
    raise_exception = False  # Отключаем ошибку. С этим флагом вместо ошибки будет переадресация на settings.LOGIN_URL
    template_name = '.employees/employees_list.html'  # указываем шаблон
    ordering = '-pk'  # опциональный и работает даже если get_queryset не переопределять
    model = Employee  # указывается для ListView (обязательный)
    per_page: int = 5  # количество объектов на странице
    available_per_page_range = [5, 10, 20, 30, 50]  # доступный per_page

    def get_queryset(self):
        qs = super().get_queryset()  # получаем queryset от родителя (ListView).
        search_query = self.request.GET.get('search')  # Получаем параметр поиска из запроса GET
        if search_query:
            qs = qs.filter(  # Ищем, если есть запрос
                Q(name__icontains=search_query) |
                Q(position__icontains=search_query) |
                Q(date_of_receipt__icontains=search_query) |
                Q(salary__icontains=search_query)
            )
        # Получаем параметр сортировки из запроса GET или используем тот, что по умолчанию
        order_by = self.request.GET.get('sort_by', self.ordering)
        return qs.order_by(order_by)

    def get_context_data(self, *args, **kwargs):
        # вызываем родительский метод, чтоб не потерять контекст от ListView
        context = super().get_context_data(*args, **kwargs)
        request_data = self.request.GET

        # проверяем, не запрашивали ли другой диапазон
        per_page = request_data.get('per_page', self.per_page)
        try:
            per_page = int(per_page)  # валидируем на то, что нам передали число в query параметре
        except ValueError:
            per_page = self.per_page
        if per_page not in self.available_per_page_range: # проверяем, что мы разрешаем столько запрашивать
            per_page = self.per_page
        # получаем список объектов из контекста (get_queryset возвращает как раз object_list
        queryset = context['object_list']
        paginator = Paginator(queryset, per_page)  # инициализируем пагинатор
        page_number = request_data.get('page', 1)  # получаем номер страницы из запроса
        page_object = paginator.get_page(page_number)

        # Скрываем лишние страницы (1, 2, 3 ... 99, 100)
        page_object.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
        return context | {"search_query": request_data.get('search'),  # Добавляем параметры из запроса
                          "sort_by": request_data.get('sort_by'),
                          "page_obj": page_object,  # и объект пагинатора
                          "available_per_page_range": self.available_per_page_range,
                          "per_page_value": per_page}


# TODO удалить
# @login_required
# def create_employee(request):
#     if request.method == 'POST':
#         form = EmployeeCreateForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('employees_list')
#     else:
#         form = EmployeeCreateForm()
#
#     return render(request, '.employees/create_employee.html', {'form': form})


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    template_name = ".employees/create_employee.html"
    form_class = EmployeeCreateForm
    success_url = reverse_lazy('employees:employees_list')  # url для редиректа при успешной обработке формы
    # TODO удалить ниже 3 строки
    # reverse_lazy вместо обычного, потому что здесь не может быть url'a, т.к. будут циклические импорты
    # reverse - собирает сразу url при запуске приложения и валиться с ошибкой. В таким местах используют reverse_lazy
    # TODO если не понял - пингани меня, я слова объясню


# TODO удалить
# @login_required
# def delete_employee(request, employee_id):
#     employee = get_object_or_404(Employee, id=employee_id)
#     if request.method == 'POST':
#         employee.delete()
#         return redirect('employees_list')
#     return render(request, '.employees/delete_employee.html', {'employee': employee})


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = ".employees/delete_employee.html"
    success_url = reverse_lazy('employees:employees_list')  # url для редиректа при успешной обработке формы


# TODO удалить :)
# @login_required
# def edit_employee(request, employee_id):
#     employee = get_object_or_404(Employee, id=employee_id)
#     if request.method == 'POST':
#         form = EmployeeEditForm(request.POST, request.FILES, instance=employee)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('employees:edit_employee', kwargs={"pk": employee_id}))
#     else:
#         form = EmployeeEditForm(instance=employee)
#
#     return render(request, '.employees/edit_employee.html', {'form': form})


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeEditForm
    template_name = '.employees/edit_employee.html'
    success_url = reverse_lazy('employees:employees_list')

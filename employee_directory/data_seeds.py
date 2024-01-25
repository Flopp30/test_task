from django_seed import Seed
from employees.models import Employee
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_directory.settings')
django.setup()


seeder = Seed.seeder()

# Добавляем данные для полей модели
seeder.add_entity(Employee, 50, {
    'name': lambda x: seeder.faker.name(),
    'position': lambda x: seeder.faker.job(),
    'date_of_receipt': lambda x: seeder.faker.date_between(start_date='-10y', end_date='today'),
    'salory': lambda x: seeder.faker.random_int(min=10000, max=200000, step=5000),
})

# Создаем данные
inserted_pks = seeder.execute()

# Создаем иерархию
all_employees = Employee.objects.all()
root = all_employees[0]
current_parent = root
level = 1
for i in range(1, len(all_employees)):
    employee = all_employees[i]
    if level < 5:
        employee.parent = current_parent
        employee.save()
        current_parent = employee
        level += 1
    else:
        employee.parent = root
        employee.save()
        current_parent = employee
        level = 1

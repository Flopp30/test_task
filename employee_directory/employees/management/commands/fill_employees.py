import random
from typing import Callable

from django.conf import settings
from django.core.management import BaseCommand
from django_seed import Seed

from employees.models import Employee


class Command(BaseCommand):
    help = 'Fill employees with random data'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, help='Employees count (default 500)')
        parser.add_argument('--tree_id', type=int, help='Employees tree_id (default create new tree)')
        parser.add_argument('--max_lvl', type=int, help='Employees max level (default 5)')

    def handle(self, *args, **options):
        EmployerSeeder.seed(count=options["count"] or 50_000,
                            tree_id=options["tree_id"],
                            max_lvl=options["max_lvl"] or 5,
                            write_func=self.stdout.write)


class EmployerSeeder:

    @classmethod
    def seed(cls, count: int, tree_id: int | None = None, max_lvl: int = 5, write_func: Callable = None):
        seeder = Seed.seeder()
        default = {
            'name': seeder.faker.name(),
            'position': seeder.faker.job(),
            'date_of_receipt': seeder.faker.date_between(start_date='-10y', end_date='today'),
            'salary': seeder.faker.random_int(min=10000, max=200000, step=5000),
        }

        if not (root := Employee.objects.filter(parent=None, tree_id=tree_id, level=0).first()):
            root = Employee.objects.create(**default, parent=None, level=0, tree_id=tree_id or 1)

        create_count_by_one_step = max(count // max_lvl, 1)
        total_counter = 0
        level = 1
        while total_counter < count:
            prev_level_parents = Employee.objects.filter(level=level - 1, tree_id=root.tree_id)
            seeder.add_entity(Employee, create_count_by_one_step, {
                'name': lambda x: seeder.faker.name(),
                'position': lambda x: seeder.faker.job(),
                'date_of_receipt': lambda x: seeder.faker.date_between(start_date='-10y', end_date='today'),
                'salary': lambda x: seeder.faker.random_int(min=10000, max=200000, step=5000),
                "parent": lambda x: seeder.faker.random_choices(prev_level_parents)[0],
                "lft": None,
                "rght": None,
                "level": level,
                "tree_id": root.tree_id,
                "photo": settings.PATH_TO_DEFAULT_PHOTO,
            })
            res = seeder.execute()
            level += 1
            created_count = len(*res.values())
            total_counter += created_count
            if write_func:
                write_func(f'Created {created_count} employees')
        if write_func:
            write_func(f'Total employees created: {total_counter}')

import random

from django.core.management import BaseCommand
from django_seed import Seed

from employees.models import Employee


class Command(BaseCommand):
    help = 'Fill employees with random data'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, help='Employees count (default 500)')
        parser.add_argument('--tree_id', type=int, help='Employees tree_id (default create new tree)')

    def handle(self, *args, **options):
        EmployerSeeder.seed(count=options["count"] or 500, tree_id=options["tree_id"])


class EmployerSeeder:

    @classmethod
    def seed(cls, count: int, tree_id: int | None = None):
        seeder = Seed.seeder()
        default = {
            'name': seeder.faker.name(),
            'position': seeder.faker.job(),
            'date_of_receipt': seeder.faker.date_between(start_date='-10y', end_date='today'),
            'salary': seeder.faker.random_int(min=10000, max=200000, step=5000),
        }

        if not (root := Employee.objects.filter(parent=None, tree_id=tree_id, level=0).first()):
            root = Employee.objects.create(**default, parent=None, level=0, tree_id=tree_id or 1)

        level = 1
        create_count_by_one_step = max(count // 5, 1)
        total_counter = 0
        while count > 0:
            prev_level_parents = Employee.objects.filter(level=level - 1, tree_id=root.tree_id)
            seeder.add_entity(Employee, create_count_by_one_step, {
                'name': lambda x: seeder.faker.name(),
                'position': lambda x: seeder.faker.job(),
                'date_of_receipt': lambda x: seeder.faker.date_between(start_date='-10y', end_date='today'),
                'salary': lambda x: seeder.faker.random_int(min=10000, max=200000, step=5000),
                "parent": random.choice(prev_level_parents),
                "lft": None,
                "rght": None,
                "level": level,
                "tree_id": root.tree_id,
            })
            res = seeder.execute()
            count -= create_count_by_one_step
            level += 1
            created_count = len(*res.values())
            total_counter += created_count
            print(f'Created {created_count} employees')
        print("Total employees created: ", total_counter)

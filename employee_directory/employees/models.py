from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Employee(MPTTModel):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    date_of_receipt = models.DateField()
    salary = models.FloatField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

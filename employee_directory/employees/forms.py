from django import forms
from .models import Employee


class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position', 'date_of_receipt', 'salary', 'parent']


class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'photo': forms.FileInput(),
        }

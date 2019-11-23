from django import forms
from .models import WhiteHouseSalaries
from django.urls import reverse

class WhiteHouseSalaryForm(forms.ModelForm):
    class Meta:
        model = WhiteHouseSalaries
        fields = (
            "employee_name",
            "employee_status",
            "salary",
            "pay_basis",
            "position_title"
        )

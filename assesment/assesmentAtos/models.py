from django.db import models

class WhiteHouseSalaries(models.Model):
    employee_name=models.CharField(max_length=50)
    employee_status=models.CharField(max_length=50)
    salary=models.FloatField()
    pay_basis=models.CharField(max_length=15)
    position_title=models.CharField(max_length=150)

    def __str__(self):
        return f"{self.employee_name} Function: {self.employee_status} "

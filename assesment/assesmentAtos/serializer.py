from rest_framework import serializers
from .models import WhiteHouseSalaries

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = WhiteHouseSalaries
        fields = (
            "id",
            "employee_name",
            "employee_status",
            "salary",
            "pay_basis",
            "position_title"
        )

# converts to json
# validate data thats passed
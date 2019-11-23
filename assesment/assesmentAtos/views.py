from django.shortcuts import render
import csv, io 
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .models import WhiteHouseSalaries
from .forms import WhiteHouseSalaryForm

def whitehousesalary(request):
    template = "whitehousesalary.html"


    if request.method == "POST":
        form = WhiteHouseSalaryForm(request.POST)

        if form.is_valid():
            form.save()

    else:
        form = WhiteHouseSalaryForm()

    context ={
        'form' : form
    }

    return render(request,template,context)


@permission_required("admin.can_add_log_entry")
def csv_upload(request):
    template = "csvUpload.html"
    
    prompt = {
        "order" : "order must be employee_name , employee_status , salary , pay_basis , position_title"
    }

    if  request.method== "GET":
        return render (request,template,prompt)

    csv_file = request.FILES['file']


    if not csv_file.name.endswith('.csv'):
        messages.error(request,"CSV only")

    data_set = csv_file.read().decode("UTF-8")
    io_string = io.StringIO(data_set)

    next(io_string)

    for column in csv.reader(io_string,delimiter=",",quotechar='"'):
        created = WhiteHouseSalaries.objects.update_or_create(
            employee_name=column[0],
            employee_status=column[1],
            salary=column[2],
            pay_basis=column[3],
            position_title=column[4],
        )

    context={}
    return render(request,template,context)
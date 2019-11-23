from django.shortcuts import render ,redirect ,get_object_or_404
import csv
import io
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
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

    context = {
        'form': form
    }

    return render(request, template, context)


def csv_upload(request):
    template = "csvUpload.html"

    prompt = {
        "order": "order must be employee_name , employee_status , salary , pay_basis , position_title"
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "CSV only")

    data_set = csv_file.read().decode("UTF-8")
    io_string = io.StringIO(data_set)

    next(io_string)

    for column in csv.reader(io_string, delimiter=",", quotechar='"'):
        created = WhiteHouseSalaries.objects.update_or_create(
            employee_name=column[0],
            employee_status=column[1],
            salary=column[2],
            pay_basis=column[3],
            position_title=column[4],
        )

    context = {}
    return render(request, template, context)

# Function that takes a request and displays it on the browser
def salary_list(request, template_name='/home/sargit/assesment/assesment/assesmentAtos/templates/salary_list.html'):
    salary = WhiteHouseSalaries.objects.all()
    data = {}
    data['object_list'] = salary
    return render(request, template_name, data)

# function that displays one row of the database table
def salary_view(request, pk, template_name='/home/sargit/assesment/assesment/assesmentAtos/templates/salary_detail.html'):
    salary = get_object_or_404(WhiteHouseSalaries, pk=pk)
    return render(request, template_name, {'object': salary})

# function that asks for new entry information
def salary_create(request, template_name='/home/sargit/assesment/assesment/assesmentAtos/templates/salary_form.html'):
    form = WhiteHouseSalaryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('salary_list')
    return render(request, template_name, {'form': form})

# function that creates new row in the database
def salary_update(request, pk, template_name='/home/sargit/assesment/assesment/assesmentAtos/templates/salary_form.html'):
    salary = get_object_or_404(WhiteHouseSalaries, pk=pk)
    form = WhiteHouseSalaryForm(request.POST or None, instance=salary)
    if form.is_valid():
        form.save()
        return redirect('salary_list')
    return render(request, template_name, {'form': form})

# function that deletes row from database
def salary_delete(request, pk, template_name='/home/sargit/assesment/assesment/assesmentAtos/templates/salary_confirm_delete.html'):
    salary = get_object_or_404(WhiteHouseSalaries, pk=pk)
    if request.method == 'POST':
        salary.delete()
        return redirect('salary_list')
    return render(request, template_name, {'object': salary})

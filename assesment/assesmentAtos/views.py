from django.shortcuts import render ,redirect ,get_object_or_404
import csv, io ,json
from django.http import HttpResponse
from django.contrib import messages
from .models import WhiteHouseSalaries
from .forms import WhiteHouseSalaryForm
from django_pandas.io import read_frame
from django.views.decorators.csrf import csrf_exempt
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_svg import FigureCanvas
import numpy as np
import pandas as pd

########################################### CSV upload methods ######################################################################
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


########################################### end CSV upload methods ######################################################################



########################################### CRUD methods ######################################################################

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

########################################### end CRUD methods ######################################################################



########################################### API methods ######################################################################

def index(request):
    response = json.dumps({"Usage api getsalary": "example : http://127.0.0.1:8000/api/50", "Usage Post": "use postman witj json body { form } http://127.0.0.1:8000/api/addSalary/"})
    return HttpResponse(response,content_type='text/json')

def get_salary(request,id):
    if request.method =='GET':
        try:
            employee = WhiteHouseSalaries.objects.get(id=id)
            response = json.dumps({'employee_name': employee.employee_name , 'employee_status': employee.employee_status,'salary':employee.salary,'pay_basis':employee.pay_basis,'position_titile': employee.position_title})
        except:
            response = json.dumps([{'Error': "Nothing found"}])
    return HttpResponse(response,content_type='text/json')

@csrf_exempt
def add_salary(request):
    if request.method == 'POST':
        payload = json.loads(json.dumps(request.POST))
        employee_name= payload['employee_name']
        employee_status=payload['employee_status']
        salary=payload['salary']
        pay_basis=payload['pay_basis']
        position_title=payload['position_title']
        entry = WhiteHouseSalaries(
                employee_name=employee_name,
                employee_status=employee_status,
                salary=salary,
                pay_basis=pay_basis,
                position_title=position_title
        )
        try:
            entry.save()
            response = json.dumps([{"succes": 'salary added'}])
        except:
            response = json.dumps([{"Error" : 'Shit went sideways'}])
    return HttpResponse(response,content_type='text/json')

########################################### end API methods ######################################################################


########################################### Statistic methods methods ######################################################################

# Statistic Non graphical
def statistics_salary(request,template_name='/home/sargit/assesment/assesment/assesmentAtos/templates/salary_statistics.html'):
    quaryset = WhiteHouseSalaries.objects.all()
    df = read_frame(quaryset)

    meanSalary=df['salary'].mean()
    maxSalary= df['salary'].max()
    minSalary= df['salary'].min()
    totalSalaryExpenses= df['salary'].sum()
    employeeTypes = df['employee_status'].unique()

    employeeMeanTable = df.groupby('employee_status').salary.mean()
     
    
    employeeMean=[]
    for row in employeeMeanTable:
        employeeMean.append(row)


    data = {}
    data['employeeTypes'] = employeeTypes
    data['employeeMean']= employeeMean
    data['mean'] = meanSalary
    data['max'] =maxSalary
    data['min'] = minSalary
    data['total'] = totalSalaryExpenses

    return render(request, template_name, data)





def plot_corr(df):
    f, ax = plt.subplots(figsize=(10, 8))
    corr = df.corr('pearson')
    sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),square=True, ax=ax)

def pltToSvg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

def correlation_matrix(request):
    quaryset = WhiteHouseSalaries.objects.all()
    df = read_frame(quaryset)
    f, ax = plt.subplots(figsize=(10, 8))
    corr = df.corr('pearson')
    sns.heatmap(corr, cmap=sns.diverging_palette(220, 10, as_cmap=True))
    svg = pltToSvg() # convert plot to SVG
    plt.cla() # clean up plt so it can be re-used
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response


def pychart(request):
    quaryset = WhiteHouseSalaries.objects.all()
    df = read_frame(quaryset)
    df_combined= df.groupby('employee_status').salary.mean()
    pie = df_combined.plot.pie(y='employee_status')
    svg=pltToSvg()
    plt.cla()
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response




def box_plot(request):
    quaryset = WhiteHouseSalaries.objects.all()
    df = read_frame(quaryset)

    boxplot=df.boxplot(['salary'],by=['employee_status'])
    svg=pltToSvg()
    plt.cla()
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response


def getTitle(postition_title):
    position = postition_title.tolist()
    titles=[]
    for title in position:
        title.lower()
        if title=="assistant":
            titles.append(title)
        if title=="director":
            titles.append(title)
        if title=="councel":
            titles.append(title)

    isUnique(titles)
    return pd.Series(titles,name='titles')

def isUnique(list):

    unique=[]
    for item in list:
        if item not in unique:
            unique.append(item)
    return unique


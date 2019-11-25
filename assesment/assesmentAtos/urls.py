from django.urls import path ,include
from . import views


urlpatterns = [
    path('', views.salary_list, name='salary_list'),
    path('view/<int:pk>', views.salary_view, name='salary_view'),
    path('new', views.salary_create, name='salary_new'),
    path('edit/<int:pk>', views.salary_update, name='salary_edit'),
    path('delete/<int:pk>', views.salary_delete, name='salary_delete'),
    path('statistics/',views.statistics_salary,name='salary_statistics'),
    path('correlation/',views.correlation_matrix,name = 'correlation_matrix'),
    path('box/',views.box_plot,name="box_plot"),
    path('pychart/',views.pychart,name='pychart'),
    path('std/',views.std, name='std')
]

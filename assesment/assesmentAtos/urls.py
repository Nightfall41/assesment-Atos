from django.urls import path ,include
from . import views


urlpatterns = [
    path('', views.salary_list, name='salary_list'),
    path('view/<int:pk>', views.salary_view, name='salary_view'),
    path('new', views.salary_create, name='salary_new'),
    path('edit/<int:pk>', views.salary_update, name='salary_edit'),
    path('delete/<int:pk>', views.salary_delete, name='salary_delete'),

]

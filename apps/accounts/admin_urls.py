from django.urls import path
from . import admin_views as v

app_name = 'admin_panel'

urlpatterns = [
    path('', v.admin_dashboard, name='dashboard'),
    path('students/', v.students_list, name='students'),
    path('students/<int:student_id>/', v.student_detail, name='student_detail'),
]

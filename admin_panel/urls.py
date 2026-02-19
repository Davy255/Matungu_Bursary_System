from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('applications/', views.applications_for_review, name='applications_review'),
    path('applications/<str:application_id>/approve/', views.approve_application, name='approve_application'),
    path('applications/<str:application_id>/reject/', views.reject_application, name='reject_application'),
    path('applications/<str:application_id>/details/', views.view_applicant_details, name='applicant_details'),
    path('approved-applicants/', views.approved_applicants_list, name='approved_applicants'),
    path('export-csv/', views.export_approved_csv, name='export_csv'),
    path('manage-admins/', views.manage_admins, name='manage_admins'),
    path('reports/', views.reports_dashboard, name='reports'),
]
